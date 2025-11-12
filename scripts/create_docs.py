"""
Generate Markdown documentation from Python source code docstrings.

This module provides functionality to extract docstrings from Python files and
generate Markdown documentation suitable for use with documentation systems.
It parses Python source code using AST, extracts module, class, and function
docstrings, and formats them into structured Markdown output.
"""

import ast
import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

from docstring_parser import parse as parse_docstring


@dataclass
class DocumentedItem:
    """
    Represent a documented code item (module, class, function, or method).

    Attributes
    ----------
    name : str
        The name of the documented item.
    doc : Any, optional
        The parsed documentation object or raw docstring text.
    signature : str, optional
        The formatted signature string for functions/methods.
    methods : list[DocumentedItem]
        List of documented methods (for classes).
    """

    name: str
    doc: Optional[Any]
    signature: Optional[str] = None
    methods: list["DocumentedItem"] = field(default_factory=list)


@dataclass
class FileDoc:
    """
    Represent documentation extracted from a single Python file.

    Attributes
    ----------
    path : str
        The file path of the source file.
    module : DocumentedItem
        Documentation for the module itself.
    classes : list[DocumentedItem]
        List of documented classes found in the file.
    functions : list[DocumentedItem]
        List of documented functions found in the file.
    """

    path: str
    module: DocumentedItem
    classes: list[DocumentedItem]
    functions: list[DocumentedItem]


def extract_docstrings_from_file(path: Path) -> FileDoc:
    """
    Parse a single Python file and extract module, class, and function docstrings.

    Parameters
    ----------
    path : Path
        Path to the Python file to parse.

    Returns
    -------
    FileDoc
        A FileDoc containing parsed docstring objects (or raw text when parsing fails).
    """
    text = path.read_text(encoding="utf-8")
    tree = ast.parse(text, filename=str(path))

    def _parse_text(txt: Optional[str]) -> Optional[dict[str, Any]]:
        if not txt:
            return None

        # detect style first and call parse with explicit style when possible
        parsed = parse_docstring(txt)
        # normalize the parsed docstring into a structured dict so callers
        # don't need to know the docstring-parser internals
        out: dict[str, Any] = {}
        desc_parts: list[str] = []
        sd = getattr(parsed, "short_description", None)
        if sd is not None:
            desc_parts.append(str(sd))
        ld = getattr(parsed, "long_description", None)
        if ld is not None:
            # long_description may be a complex object in some docstring-parser
            # versions; convert to string representation.
            desc_parts.append(str(ld))

        deprecation = getattr(parsed, "deprecation", None)
        if deprecation:
            # deprecation may be a complex object in some docstring-parser
            # versions; convert to string representation.
            note = str(getattr(deprecation, "description", None) or deprecation)
            if note:
                desc_parts.append(f"<Danger>**Deprecated.** {note}</Danger>")

        out["description"] = "\n\n".join(p for p in desc_parts if p)

        # parameters
        params = []
        for p in getattr(parsed, "params", []) or []:
            params.append(
                {
                    "name": getattr(p, "arg_name", None) or getattr(p, "args", None) or None,
                    "type": getattr(p, "type_name", None),
                    "description": getattr(p, "description", None),
                }
            )
        out["params"] = params

        # raises / exceptions
        raises = []
        for r in getattr(parsed, "raises", []) or []:
            raises.append(
                {
                    "type": getattr(r, "type_name", None) or getattr(r, "exception", None) or None,
                    "description": getattr(r, "description", None),
                }
            )
        out["raises"] = raises

        # returns
        ret = getattr(parsed, "returns", None)
        if ret:
            out["returns"] = {"type": getattr(ret, "type_name", None), "description": getattr(ret, "description", None)}
        else:
            out["returns"] = None

        examples = []
        for e in getattr(parsed, "examples", []) or []:
            code = ""
            snippet = getattr(e, "snippet", None)
            if snippet:
                snippet = snippet.replace("\n>>> ", "\n")
            description = getattr(e, "description", None)
            if snippet and description:
                if snippet.startswith(">>>"):
                    code = f"{snippet}\n{description.replace('... ', '').replace('>>> ', '')}"
                else:
                    code = f"{snippet}\n{description}"
            elif snippet:
                code = f"{snippet}"
            elif description:
                code = f"{description}"
            if code:
                examples.append({"code": code})
        if examples:
            out["examples"] = examples

        notes = []
        meta = getattr(parsed, "meta", None)
        if meta:
            for m in meta:
                meta_args = getattr(m, "args", [])
                if len(meta_args) == 1 and meta_args[0] == "notes":
                    note = getattr(m, "description", None)
                    if note:
                        notes.append({"note": note})
        if notes:
            out["notes"] = notes

        return out

    module_doc = _parse_text(ast.get_docstring(tree))
    module_item = DocumentedItem(name=path.stem, doc=module_doc)

    classes: list[DocumentedItem] = []
    functions: list[DocumentedItem] = []

    def _make_signature_for_callable(node: Any) -> Optional[str]:
        """
        Return a formatted signature string for a FunctionDef/AsyncFunctionDef node.

        This mirrors the previous inline logic: unparse args and return annotation,
        ensure parentheses, and wrap multi-parameter signatures to multiple lines
        if they exceed ~85 characters.

        Parameters
        ----------
        node : ast.FunctionDef or ast.AsyncFunctionDef
            The AST node representing the function.

        Returns
        -------
        str or None
            The formatted signature string, or None if parsing fails.
        """
        try:
            args_src = ast.unparse(node.args)
            if not args_src.startswith("("):
                args_src = f"({args_src})"
            ret_src = ""
            if getattr(node, "returns", None) is not None:
                try:
                    ret_src = " -> " + ast.unparse(node.returns)
                except Exception:
                    ret_src = ""
                    # Check if this is an async function

            is_async = isinstance(node, ast.AsyncFunctionDef)
            async_prefix = "async " if is_async else ""
            sig = f"{async_prefix}def {node.name}{args_src}{ret_src}"

            # Wrap signature if needed
            if args_src.startswith("(") and len(args_src) > 2:
                params_str = args_src[1:-1]

                # Split on commas not inside brackets or parentheses
                def smart_split(s: str) -> list:
                    parts = []
                    bracket_level = 0
                    paren_level = 0
                    current = []
                    for c in s:
                        if c == "[":
                            bracket_level += 1
                        elif c == "]":
                            bracket_level -= 1
                        elif c == "(":
                            paren_level += 1
                        elif c == ")":
                            paren_level -= 1
                        if c == "," and bracket_level == 0 and paren_level == 0:
                            part = "".join(current).strip()
                            if part:
                                parts.append(part)
                            current = []
                        else:
                            current.append(c)
                    part = "".join(current).strip()
                    if part:
                        parts.append(part)
                    return parts

                params = smart_split(params_str)
            else:
                params = []

            if (not params) or len(sig) <= 85:
                return sig

            indent = " " * (len(f"{async_prefix}def {node.name}("))
            first_param = params[0]
            other_params = params[1:]
            wrapped = [f"{async_prefix}def {node.name}({first_param},"]
            for i, p in enumerate(other_params):
                if i == len(other_params) - 1:
                    wrapped.append(f"{indent}{p}){ret_src}")
                else:
                    wrapped.append(f"{indent}{p},")
            return "\n".join(wrapped)

        except Exception:
            return None

    # Iterate top-level statements: collect module-level functions and classes
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            doc = _parse_text(ast.get_docstring(node))
            # try to produce a class signature
            try:
                sig = f"class {node.name}"
            except Exception:
                sig = None

            # Collect methods defined directly on the class
            methods: list[DocumentedItem] = []
            for child in node.body:
                if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    # skip private methods
                    if child.name.startswith("_"):
                        continue
                    mdoc = _parse_text(ast.get_docstring(child))
                    m_sig = _make_signature_for_callable(child)
                    methods.append(DocumentedItem(name=child.name, doc=mdoc, signature=m_sig))

            classes.append(DocumentedItem(name=node.name, doc=doc, signature=sig, methods=methods))
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # top-level functions only
            if node.name.startswith("_"):
                continue

            doc = _parse_text(ast.get_docstring(node))
            sig = _make_signature_for_callable(node)
            functions.append(DocumentedItem(name=node.name, doc=doc, signature=sig))
    return FileDoc(path=str(path), module=module_item, classes=classes, functions=functions)


def parse_docstring_text(txt: Optional[str]) -> Optional[dict[str, Any]]:
    """
    Parse and normalize a single docstring text.

    Kept for test compatibility.

    Parameters
    ----------
    txt : str, optional
        The raw docstring text to parse.

    Returns
    -------
    dict[str, Any] or None
        A dictionary containing normalized docstring components, or None if input is empty.
    """
    if not txt:
        return None

    parsed = parse_docstring(txt)
    out: dict[str, Any] = {}
    desc_parts: list[str] = []
    sd = getattr(parsed, "short_description", None)
    if sd is not None:
        desc_parts.append(str(sd))
    ld = getattr(parsed, "long_description", None)
    if ld is not None:
        desc_parts.append(str(ld))
    out["description"] = "\n\n".join(p for p in desc_parts if p)

    params = []
    for p in getattr(parsed, "params", []) or []:
        params.append(
            {
                "name": getattr(p, "arg_name", None) or getattr(p, "args", None) or None,
                "type": getattr(p, "type_name", None),
                "description": getattr(p, "description", None),
            }
        )
    out["params"] = params

    raises = []
    for r in getattr(parsed, "raises", []) or []:
        raises.append(
            {
                "type": getattr(r, "type_name", None) or getattr(r, "exception", None) or None,
                "description": getattr(r, "description", None),
            }
        )
    out["raises"] = raises

    ret = getattr(parsed, "returns", None)
    if ret:
        out["returns"] = {"type": getattr(ret, "type_name", None), "description": getattr(ret, "description", None)}
    else:
        out["returns"] = None

    return out


def parse_source(root: str, to_ignore: Optional[list[str]] = None) -> list[FileDoc]:
    """
    Parse all .py files under `root` and return files_docs.

    Parameters
    ----------
    root : str
        The root directory to search for Python files.
    to_ignore : list[str], optional
        A list of glob patterns matched against the file's path relative to `root`
        (POSIX style). Any file matching any pattern will be skipped.

    Returns
    -------
    list[FileDoc]
        A list of FileDoc objects containing documentation extracted from parsed files.
    """
    rootp = Path(root).resolve()
    files_docs: list[FileDoc] = []

    patterns = [p for p in (to_ignore or []) if p]

    for p in rootp.rglob("*.py"):
        # skip files whose filename starts with an underscore
        if p.name.startswith("_"):
            continue
        # compute posix relative path for matching
        try:
            rel = p.resolve().relative_to(rootp).as_posix()
        except (ValueError, RuntimeError, TypeError):
            # if not relative, skip
            continue

        # check ignore patterns (match against relative posix path and also each path segment)
        skip = False
        for pat in patterns:
            # if pattern contains glob chars, use fnmatch against full path and segments
            if any(c in pat for c in "*?[]"):
                if fnmatch.fnmatch(rel, pat) or any(fnmatch.fnmatch(part, pat) for part in rel.split("/")):
                    skip = True
                    break
            else:
                # exact match only: match full relative path or an exact path segment
                if pat == rel or any(pat == part for part in rel.split("/")):
                    skip = True
                    break
        if skip:
            continue

        try:
            fd = extract_docstrings_from_file(p)
        except (SyntaxError, UnicodeDecodeError):
            # skip files that fail to parse or read
            continue

        files_docs.append(fd)

    return files_docs


def build_docs(files_docs: list[FileDoc], source_root: str, output_root: str) -> None:
    """
    Write Markdown files into output_root mirroring the path structure under source_root.

    For each FileDoc with any docstrings, create a corresponding .md file whose
    path mirrors the source file relative to source_root but with a .mdx extension.
    The file will contain sections for module, classes, and functions and will
    dump the raw/parsed docstring content.

    Parameters
    ----------
    files_docs : list[FileDoc]
        List of FileDoc objects containing extracted documentation.
    source_root : str
        The root directory of the source files.
    output_root : str
        The root directory where output markdown files will be written.

    Returns
    -------
    None
    """
    src_root = Path(source_root).resolve()
    out_root = Path(output_root).resolve()

    for fd in files_docs:
        # Log what file we're processing
        print(f"Processing {fd.path}")

        # fd.path is the full path to the source file
        src_path = Path(fd.path).resolve()
        try:
            rel = src_path.relative_to(src_root)
        except (ValueError, RuntimeError, TypeError):
            # if the file isn't under source_root, skip it
            continue

        # Determine whether there is anything worth writing: module doc,
        # at least one class with a docstring or documented methods, or at least one function with a docstring.
        module_has = bool(fd.module and fd.module.doc)
        # Include classes that have a docstring OR have at least one documented method
        class_docs = [cls for cls in fd.classes if cls.doc or any(m.doc for m in getattr(cls, "methods", []))]
        function_docs = [fn for fn in fd.functions if fn.doc]

        if not (module_has or class_docs or function_docs):
            # nothing documented in this file; skip emitting an output file
            continue

        # build output path: change suffix to .mdx
        out_path = out_root.joinpath(rel).with_suffix(".mdx")
        out_path.parent.mkdir(parents=True, exist_ok=True)

        parts: list[str] = []

        # Header
        parts.append("---")
        parts.append(f"title: {rel.stem}")
        parts.append("---\n")
        parts.append(
            "{/* This page is autogenerated from the Python SDK. Do not edit this file as it will be replaced on the next SDK publish */}\n"
        )

        # Module doc (render structured doc or raw description)
        if module_has:
            write_module(fd, parts)

        # Classes with docstrings only
        if class_docs:
            for cls in class_docs:
                write_class(parts, cls)

        # Functions with docstrings only
        if function_docs:
            for fn in sorted(function_docs, key=lambda f: f.name.lower()):
                write_function(parts, fn, heading_level=2)

        out_text = "\n".join(parts)
        out_path.write_text(out_text, encoding="utf-8")

    print(f"Documentation generation complete. Output written to {out_root}")


def write_function(parts: list[str], fn: Any, heading_level: int = 3) -> None:
    """
    Append formatted documentation for a function to the provided parts list.

    The documentation includes the function name, signature, description, arguments,
    raised exceptions, and return value, formatted in Markdown suitable for Python
    code blocks.

    Parameters
    ----------
    parts : list
        The list to which the formatted documentation strings will be appended.
    fn : object
        An object representing the function, expected to have the following attributes:
        - name (str): The function's name.
        - signature (str, optional): The function's signature.
        - doc (dict or str): The function's documentation, either as a dictionary with
          keys 'description', 'params', 'raises', 'returns', or as a string.
    heading_level : int, optional
        The markdown heading level to use (default is 3).

    Returns
    -------
    None
        This function modifies the `parts` list in place.
    """
    parts.append(f"{('#' * heading_level)} {fn.name}\n")
    parts.append("```python")
    if getattr(fn, "signature", None):
        parts.append(f"{fn.signature}")
    else:
        parts.append(f"def {fn.name}(...)")
    parts.append("```\n")
    fdoc = fn.doc
    if isinstance(fdoc, dict):
        if fdoc.get("description"):
            parts.append(f"{fdoc.get('description')}\n")
        if fdoc.get("params"):
            parts.append("**Arguments**\n")
            for p in fdoc.get("params", []):
                name = p.get("name") or "<arg>"
                t = p.get("type")
                desc = p.get("description") or ""
                desc = desc.replace("\n", "\n    ")

                # Escape curly braces outside code blocks (triple or single backticks)
                def escape_curly_braces(text: str) -> str:
                    # Split by triple backtick code blocks first
                    triple_segments = re.split(r"(```.*?```)", text, flags=re.DOTALL)
                    for i, triple_seg in enumerate(triple_segments):
                        if triple_seg.startswith("```"):
                            # Inside triple backtick code block, leave as is
                            continue
                        # Now split by single backtick code blocks
                        single_segments = re.split(r"(`[^`]*`)", triple_seg)
                        for j, single_seg in enumerate(single_segments):
                            if not single_seg.startswith("`"):
                                single_seg = single_seg.replace("{", r"\{").replace("}", r"\}")
                            single_segments[j] = single_seg
                        triple_segments[i] = "".join(single_segments)
                    return "".join(triple_segments)

                desc = escape_curly_braces(desc)

                if t:
                    parts.append(f"- `{name}` (`{t}`): {desc}")
                else:
                    parts.append(f"- `{name}`: {desc}")
            parts.append("")
        if fdoc.get("raises"):
            parts.append("**Raises**\n")
            for r in fdoc.get("raises", []):
                typ = r.get("type") or "Exception"
                desc = r.get("description") or ""
                parts.append(f"- `{typ}`: {desc}")
            parts.append("")
        if fdoc.get("returns"):
            parts.append("**Returns**\n")
            ret = fdoc.get("returns")
            if ret:
                rtyp = ret.get("type") or ""
                rdesc = ret.get("description") or ""
                if rtyp:
                    parts.append(f"- `{rtyp}`: {rdesc}\n")
                else:
                    parts.append(f"- {rdesc}\n")
        if fdoc.get("examples"):
            parts.append("**Examples**\n")
            is_in_code_block = False
            for ex in fdoc.get("examples", []):
                code = ex.get("code")
                if code:
                    if not is_in_code_block and code.startswith(">>>"):
                        is_in_code_block = True
                        parts.append("```python")
                    if is_in_code_block and not code.startswith(">>>") and not code.startswith("..."):
                        is_in_code_block = False
                        parts.append("```\n")
                    if not code.startswith(">>>") and not code.startswith("..."):
                        parts.append(code)
                    else:
                        parts.append(code[4:])
            if is_in_code_block:
                parts.append("```\n")
            parts.append("")
        if fdoc.get("notes"):
            parts.append("**Notes**\n")
            for note in fdoc.get("notes", []):
                ntext = note.get("note")
                if ntext:
                    parts.append(f"{ntext}")
            parts.append("")
    else:
        parts.append(f"{fdoc!r}\n")


def write_class(parts: list[str], cls: Any) -> None:
    """
    Append formatted documentation for a class to the provided list of parts.

    The function generates markdown documentation for the given class object `cls`,
    including its name, description, arguments (parameters), and return values,
    based on the structure of its `doc` attribute. The documentation is appended
    to the `parts` list.

    Parameters
    ----------
    parts : list
        A list of strings to which the formatted documentation will be appended.
    cls : object
        The class object containing a `name` attribute and a `doc` attribute.
        The `doc` attribute should be a dictionary with optional keys:
        - "description" (str): Description of the class.
        - "params" (list of dict): List of parameter documentation, each with keys:
            - "name" (str): Name of the parameter.
            - "type" (str, optional): Type of the parameter.
            - "description" (str, optional): Description of the parameter.
        - "returns" (dict, optional): Documentation for the return value, with keys:
            - "type" (str, optional): Type of the return value.
            - "description" (str, optional): Description of the return value.

    Returns
    -------
    None
        The function modifies the `parts` list in place.
    """
    parts.append(f"## {cls.name}\n")
    cdoc = cls.doc
    if isinstance(cdoc, dict):
        if cdoc.get("description"):
            parts.append(f"{cdoc.get('description')}\n")
        if cdoc.get("params"):
            parts.append("**Arguments**\n")
            for p in cdoc.get("params", []):
                name = p.get("name") or "<arg>"
                t = p.get("type")
                desc = p.get("description") or ""
                desc = desc.replace("\n", "\n    ")
                if t:
                    parts.append(f"- `{name}` (`{t}`): {desc}\n")
                else:
                    parts.append(f"- `{name}`: {desc}\n")

        if cdoc.get("examples"):
            parts.append("**Examples**\n")
            is_in_code_block = False
            for ex in cdoc.get("examples", []):
                code = ex.get("code")
                if code:
                    if not is_in_code_block and code.startswith(">>>"):
                        is_in_code_block = True
                        parts.append("```python")
                    if is_in_code_block and not code.startswith(">>>") and not code.startswith("..."):
                        is_in_code_block = False
                        parts.append("```\n")
                    if not code.startswith(">>>") and not code.startswith("..."):
                        parts.append(code)
                    else:
                        parts.append(code[4:])
            if is_in_code_block:
                parts.append("```\n")
            parts.append("")
        if cdoc.get("returns"):
            parts.append("**Returns**\n")
            ret = cdoc.get("returns")
            if ret:
                rtyp = ret.get("type") or ""
                rdesc = ret.get("description") or ""
                if rtyp:
                    parts.append(f"- `{rtyp}`: {rdesc}\n")
                else:
                    parts.append(f"- {rdesc}\n")
        if cdoc.get("notes"):
            parts.append("**Notes**\n")
            for note in cdoc.get("notes", []):
                ntext = note.get("note")
                if ntext:
                    parts.append(f"{ntext}")
            parts.append("")
    elif cdoc:
        parts.append(f"{cdoc!r}\n")
    # Emit methods documented on the class
    if getattr(cls, "methods", None):
        methods = [m for m in cls.methods if m.doc]
        if methods:
            for m in sorted(methods, key=lambda f: f.name.lower()):
                write_function(parts, m, heading_level=3)


def write_module(fd: FileDoc, parts: list[str]) -> None:
    """
    Append formatted Markdown documentation for a module to the provided parts list.

    The function extracts documentation from the `fd.module.doc` attribute, which is
    expected to be a dictionary containing keys such as 'description', 'params',
    'raises', and 'returns'. It formats each section appropriately for Markdown output,
    including argument lists, raised exceptions, and return values. If the documentation
    is not a dictionary, it appends its string representation as a fallback.

    Parameters
    ----------
    fd : object
        An object with a `module.doc` attribute containing module documentation.
    parts : list
        A list of strings to which the formatted Markdown documentation will be appended.

    Returns
    -------
    None
        The function modifies the `parts` list in place.
    """
    parts.append("## Module\n")
    md = fd.module.doc
    if isinstance(md, dict):
        if md.get("description"):
            parts.append(f"{md.get('description')}\n")
        if md.get("params"):
            parts.append("**Arguments**\n")
            for p in md.get("params", []):
                name = p.get("name") or "<arg>"
                t = p.get("type")
                desc = p.get("description") or ""

                # If description is multi-line, indent subsequent lines for better Markdown rendering
                desc = desc.replace("\n", "\n    ")

                if t:
                    parts.append(f"- `{name}` (`{t}`): {desc}\n")
                else:
                    parts.append(f"- `{name}`: {desc}\n")
        if md.get("raises"):
            parts.append("**Raises**\n")
            for r in md.get("raises", []):
                typ = r.get("type") or "Exception"
                desc = r.get("description") or ""
                parts.append(f"- `{typ}`: {desc}\n")
        if md.get("returns"):
            parts.append("**Returns**\n")
            ret = md.get("returns")
            if ret:
                rtyp = ret.get("type") or ""
                rdesc = ret.get("description") or ""
                if rtyp:
                    parts.append(f"- `{rtyp}`: {rdesc}\n")
                else:
                    parts.append(f"- {rdesc}\n")
        if md.get("notes"):
            parts.append("**Notes**\n")
            for note in md.get("notes", []):
                ntext = note.get("note")
                if ntext:
                    parts.append(f"{ntext}")
            parts.append("")
    else:
        # fallback: raw string or other
        parts.append(f"{md!r}\n")


if __name__ == "__main__":
    SOURCE = "./src/galileo"
    ignore = ["__pycache__", "constants", "resources", "schema", "__future__"]

    details = parse_source(SOURCE, to_ignore=ignore)
    build_docs(details, SOURCE, "./.generated_docs/reference")
