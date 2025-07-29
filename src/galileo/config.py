# mypy: disable-error-code=syntax
# We need to ignore syntax errors until https://github.com/python/mypy/issues/17535 is resolved.
from typing import Any, Optional

from galileo_core.schemas.base_config import GalileoConfig


class GalileoPythonConfig(GalileoConfig):
    # Config file for this project.
    config_filename: str = "galileo-python-config.json"

    def reset(self) -> None:
        global _galileo_config
        _galileo_config = None

        super().reset()

    @classmethod
    def get(cls, **kwargs: Any) -> "GalileoPythonConfig":
        global _galileo_config
        _galileo_config = cls._get(_galileo_config, **kwargs)  # type: ignore[arg-type]
        return _galileo_config


_galileo_config: Optional[GalileoPythonConfig] = None
