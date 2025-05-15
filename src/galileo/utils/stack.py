import inspect
import logging
import linecache
import os
from typing import Any, Dict, List, Optional, Tuple

from galileo_core.schemas.logging.code import LoggedStack, LoggedStackFrame

from galileo.utils.relevant_source_files import get_relevant_source_files, load_relevant_source_snippets

import sentry_sdk.utils

_logger = logging.getLogger(__name__)


# sentry modifications

def serialize_frame(
    frame,
    tb_lineno=None,
    include_local_variables=True,
    include_source_context=True,
    max_value_length=None,
    custom_repr=None,
    always_get_whole_function: bool = False,
):
    # type: (FrameType, Optional[int], bool, bool, Optional[int], Optional[Callable[..., Optional[str]]]) -> Dict[str, Any]
    f_code = getattr(frame, "f_code", None)
    if not f_code:
        abs_path = None
        function = None
    else:
        abs_path = frame.f_code.co_filename
        function = frame.f_code.co_name
    try:
        module = frame.f_globals["__name__"]
    except Exception:
        module = None

    if tb_lineno is None:
        tb_lineno = frame.f_lineno

    rv = {
        "filename": sentry_sdk.utils.filename_for_module(module, abs_path) or None,
        # this is a hack to avoid having to update the data model
        "abs_path": os.path.relpath(abs_path) if abs_path else None,
        "function": function or "<unknown>",
        "module": module,
        "lineno": tb_lineno,
    }  # type: Dict[str, Any]

    if include_source_context:
        source_lines, source_lineno = inspect.getsourcelines(frame)
        rv["pre_context"], rv["context_line"], rv["post_context"] = get_source_context(
            frame, 
            tb_lineno, 
            max_value_length,
            source_lines=source_lines if always_get_whole_function else None, 
            source_lineno=source_lineno if always_get_whole_function else None,
        )

    if include_local_variables:
        from sentry_sdk.serializer import serialize

        rv["vars"] = serialize(
            dict(frame.f_locals), is_vars=True, custom_repr=custom_repr
        )

    return rv


def get_source_context(
    frame,  # type: FrameType
    tb_lineno,  # type: Optional[int]
    max_value_length=None,  # type: Optional[int]
    source_lines=None,
    source_lineno=None,
):
    # type: (...) -> Tuple[List[Annotated[str]], Optional[Annotated[str]], List[Annotated[str]]]
    try:
        abs_path = frame.f_code.co_filename  # type: Optional[str]
    except Exception:
        abs_path = None
    try:
        module = frame.f_globals["__name__"]
    except Exception:
        return [], None, []
    try:
        loader = frame.f_globals["__loader__"]
    except Exception:
        loader = None

    if tb_lineno is not None and abs_path:
        lineno = tb_lineno - 1
        return get_lines_from_file(
            abs_path, 
            lineno, 
            max_value_length, 
            loader=loader, 
            module=module,
            source_lines=source_lines,
            source_lineno=source_lineno,
        )

    return [], None, []


def get_lines_from_file(
    filename,  # type: str
    lineno,  # type: int
    max_length=None,  # type: Optional[int]
    loader=None,  # type: Optional[Any]
    module=None,  # type: Optional[str]
    source_lines=None,
    source_lineno=None,
):
    # type: (...) -> Tuple[List[Annotated[str]], Optional[Annotated[str]], List[Annotated[str]]]
    context_lines = 5
    source = None
    if loader is not None and hasattr(loader, "get_source"):
        try:
            source_str = loader.get_source(module)  # type: Optional[str]
        except (ImportError, IOError):
            source_str = None
        if source_str is not None:
            source = source_str.splitlines()

    if source is None:
        try:
            source = linecache.getlines(filename)
        except (OSError, IOError):
            return [], None, []

    if not source:
        return [], None, []

    lower_bound = max(0, lineno - context_lines)
    upper_bound = min(lineno + 1 + context_lines, len(source))

    if source_lines is not None and source_lineno is not None:
        print(
            {
                'n_source_lines': len(source_lines),
                'source_lineno': source_lineno,
                'lineno': lineno,
                'lower_bound_before': lower_bound,
                'upper_bound_before': upper_bound,
            }
        )
        source_lineno_zeroindexed = max(0, source_lineno - 1)
        # neg_distance_to_start = source_lineno_zeroindexed - lineno
        distance_to_end = (source_lineno_zeroindexed + len(source_lines)) - lineno
        
        # lower_bound = max(0, min(lower_bound, neg_distance_to_start))
        lower_bound = max(0, min(lower_bound, source_lineno_zeroindexed))
        upper_bound = min(len(source), max(upper_bound, distance_to_end))
        print(
            {
                'source_lineno_zeroindexed': source_lineno_zeroindexed,
                'distance_to_end': distance_to_end,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
            }
        )

    try:
        pre_context = [
            sentry_sdk.utils.strip_string(line.strip("\r\n"), max_length=max_length)
            for line in source[lower_bound:lineno]
        ]
        context_line = sentry_sdk.utils.strip_string(source[lineno].strip("\r\n"), max_length=max_length)
        post_context = [
            sentry_sdk.utils.strip_string(line.strip("\r\n"), max_length=max_length)
            for line in source[(lineno + 1) : upper_bound]
        ]
        return pre_context, context_line, post_context
    except IndexError:
        # the file may have changed since it was loaded into memory
        return [], None, []



def get_function_from_frameinfo(frame_info):
    # i think this may fail is some edge cases idk
    return frame_info.frame.f_globals[frame_info.function]


def should_exclude_source_file(fn):
    if "site-packages" in fn:
        return True
    if 'lib/python' in fn:
        return True
    if 'ipykernel' in fn:
        return True
    if 'galileo-python/src/galileo' in fn:
        return True
    if 'galileo/src/galileo' in fn:
        return True
    return False


def get_stack_trace() -> Optional[LoggedStack]:
    """
    Get the stack trace for the current function.
    """
    _logger.info("Getting stack trace")
    frames = []
    for frame_info in inspect.stack():
        if should_exclude_source_file(frame_info.filename):
            continue
        try:
            serialized = serialize_frame(frame_info.frame)
            additional_context: list[str] | None = None
            try:
                additional_context = load_relevant_source_snippets(get_relevant_source_files(get_function_from_frameinfo(frame_info)))
            except KeyError as e:
                pass
            serialized["additional_context"] = additional_context
            _logger.info(f"Stack frame: {serialized}")
            frames.append(LoggedStackFrame.model_validate(serialized))
            _logger.info("Stack frame added")
        except Exception as e:
            _logger.error(f"Error while serializing stack frame: {e}", exc_info=True)
            continue
    return LoggedStack(frames=frames)


