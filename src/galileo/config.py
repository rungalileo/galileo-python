# mypy: disable-error-code=syntax
# We need to ignore syntax errors until https://github.com/python/mypy/issues/17535 is resolved.
from typing import Any, ClassVar, Optional

from pydantic_core import Url

from galileo_core.schemas.base_config import GalileoConfig


class GalileoPythonConfig(GalileoConfig):
    # Config file for this project.
    config_filename: str = "galileo-python-config.json"
    console_url: Url = "https://app.galileo.ai"

    _instance: ClassVar[Optional["GalileoPythonConfig"]] = None

    def reset(self) -> None:
        GalileoPythonConfig._instance = None
        super().reset()

    @classmethod
    def get(cls, **kwargs: Any) -> "GalileoPythonConfig":
        cls._instance = cls._get(cls._instance, **kwargs)
        assert cls._instance is not None, "Failed to initialize GalileoPythonConfig"
        return cls._instance
