import importlib
import inspect
import re
import typing
from pathlib import Path

from jinja2 import Template

MODEL_LOCATION_PREFIX = "src/galileo/resources/models/"

imports_template = Template("""# flake: noqa: F401, F811
# ruff: noqa: F401, F811
from typing import Any
from pydantic import BaseModel

""")

class_import_template = Template("""
from {{mod}} import {{item}}
from {{mod}} import {{item}} as GalileoCore{{item}}Class
""")

other_import_template = Template("""
from {{mod}} import {{item}}
""")

redef_template = Template("""

if issubclass(GalileoCore{{item}}Class, BaseModel):
    class {{item}}(GalileoCore{{item}}Class):
        def to_dict(self) -> dict[str, Any]:
            return self.model_dump(exclude_none=True)

        @classmethod
        def from_dict(cls, src_dict: dict[str, Any]) -> "{{item}}":
            return cls.model_validate(src_dict)

    {{item}}.model_rebuild()
else:
    {{item}} = GalileoCore{{item}}Class

""")

basemodel_dict_template = Template("""# flake: noqa: F401
# ruff: noqa: F401
from ..models.{{unified_file_name}} import {{item}}

""")


def camel_to_snake(name):
    """Converts a string from camel case to snake case."""
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()
    return name


def get_module(mod_path):
    return ".".join(mod_path[1:].split("/"))


def main():
    import galileo_core

    root = Path(galileo_core.__file__).parent

    print("Package", root)

    class_files = [path for path in root.glob("**/*.py") if path.name != "__init__.py"]

    unified_file_name = "all_galileo_core_models"
    mod_import_list = []
    mod_other_list = []

    # Individual model files to allow the API client to function
    for f in class_files:
        mod_path = str(f.with_suffix("")).removeprefix(str(root.parent))
        mod = get_module(mod_path)
        if mod.startswith("galileo_core.testing"):
            continue
        module = importlib.import_module(mod)

        print(">>", mod)
        for item in dir(module):
            ic = getattr(module, item)
            if not item.startswith("__") and inspect.isclass(ic) and ic.__module__.startswith("galileo"):
                print("    >>", item, camel_to_snake(item))
                with open(f"{MODEL_LOCATION_PREFIX}/{camel_to_snake(item)}.py", "w") as f:
                    f.write(basemodel_dict_template.render({"unified_file_name": unified_file_name, "item": item}))
                mod_import_list.append((mod, item))
            elif (
                not item.startswith("__")
                and "__class__" in dir(ic)
                and ic.__class__ == typing._AnnotatedAlias
                and item not in {"UUID4"}
            ):
                mod_other_list.append((mod, item))
        print()

    with open(f"{MODEL_LOCATION_PREFIX}/{unified_file_name}.py", "w") as f:
        # Ignores
        f.write(imports_template.render({}))
        # Class imports
        for mod, item in mod_import_list:
            f.write(class_import_template.render({"mod": mod, "item": item}))
        f.write("\n\n############################################################\n")
        for mod, item in mod_other_list:
            f.write(other_import_template.render({"mod": mod, "item": item}))
        # Class redefinitions
        for _, item in mod_import_list:
            f.write(redef_template.render({"item": item}))


if __name__ == "__main__":
    main()
