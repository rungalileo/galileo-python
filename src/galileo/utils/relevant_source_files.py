import os
from typing import Callable, Dict
import inspect
from itertools import chain
from dataclasses import dataclass, field
from collections import defaultdict

@dataclass
class SourceFileMeta:
    linenos: set[int] | None = field(default_factory=set)


@dataclass
class SourceSnippet:
    file_path: str
    start_line: int | None
    end_line: int | None
    content: str | None = field(init=False)

    def __post_init__(self):
        try:
            with open(self.file_path) as f:
                lines = list(f)
            start_line = self.start_line
            
            if start_line is None:
                start_line = 0
    
            end_line = self.end_line
            if end_line is None:
                end_line = len(lines)
            self.content = "".join(lines[start_line:end_line]).strip("\n")
        except FileNotFoundError:
            self.content = None

    def render(self):
        pathspec = os.path.relpath(self.file_path)
        linespec=''
        if self.start_line is not None and self.end_line is not None:
            linespec = f":{self.start_line+1}:{self.end_line+1}"
        return f"""\
`{pathspec}{linespec}`

```python
{self.content}
```
"""
            

def exclude_source_file_name(fn):
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

def get_relevant_source_files(
    f: Callable, 
    fns: dict | None = None,
    always_get_whole_file: bool = True,
):
    if fns is None:
        fns = defaultdict(SourceFileMeta)

    cvs = inspect.getclosurevars(inspect.unwrap(f))
    # print(f"{f}: {cvs}")

    for name, val in chain(cvs.nonlocals.items(), cvs.globals.items()):
        # print(f"handling {name}")
        if inspect.isfunction(val) or inspect.ismodule(val):
            try:
                fn = inspect.getsourcefile(inspect.unwrap(val))
            except TypeError as e:
                # builtins
                # print(f"{name}: {e}")
                continue
            # print(f"have {fn}")
            if not exclude_source_file_name(fn):
                # print(f"handling {name}->{fn}")
                if inspect.isfunction(val):
                    if always_get_whole_file:
                        fns[fn] = SourceFileMeta(linenos=None)
                    elif fns[fn].linenos is not None:
                        lines, startno = inspect.getsourcelines(val)
                        startno -= 1 # zero indexed
                        # print(f"handling {name}->{fn}: {(startno, startno+len(lines))}")
                        fns[fn].linenos.update(range(startno, startno+len(lines)))
                    get_relevant_source_files(val, fns)   
                else:
                    fns[fn] = SourceFileMeta(linenos=None)

    return dict(fns)


def load_relevant_source_snippets(fns: Dict[str, SourceFileMeta]) -> list[str]:
    snippets = []
    
    for name, meta in fns.items():
        if meta.linenos is None:
            # all lines
            snippet = SourceSnippet(file_path=name, start_line=0, end_line=None)
            snippets.append(snippet)
        elif len(meta.linenos) == 0:
            continue
        else:
            i = min(meta.linenos)
            start = i
            last = max(meta.linenos) + 1

            # print((start, last))

            while i <= last:
                # print(i)
                if i not in meta.linenos and start is not None:
                    snippet = SourceSnippet(file_path=name, start_line=start, end_line=i)
                    # print(('flush', start, i))
                    snippets.append(snippet)

                    start = None
                if i in meta.linenos and start is None:
                    # print(('start', i))
                    start = i
                i += 1
    return [
        snippet.render()
        for snippet in snippets
    ]
