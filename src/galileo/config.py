# mypy: disable-error-code=syntax
# We need to ignore syntax errors until https://github.com/python/mypy/issues/17535 is resolved.
from typing import Any, Optional

from galileo_core.schemas.base_config import GalileoConfig


class GalileoSDKConfig(GalileoConfig):
    # Config file for this project.
    config_filename: str = "galileo-config.json"

    def reset(self) -> None:
        global _galileo_config
        _galileo_config = None

        super().reset()

    @classmethod
    def get(cls, **kwargs: Any) -> "GalileoConfig":
        global _galileo_config
        if _galileo_config is None:
            _galileo_config = cls(**kwargs)
        return _galileo_config


_galileo_config: Optional[GalileoSDKConfig] = None
