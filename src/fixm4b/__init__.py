"""fixm4b — retag converted audiobooks without re-encoding."""

from fixm4b.config import Fixm4bConfig, default_config_path, write_default_config
from fixm4b.errors import ConfigurationError, Fixm4bError
from fixm4b.metadata import FixPlan, apply_fix, plan_fix
from fixm4b.settings import Fixm4bSettings, get_settings, set_settings, settings_from_cfg

__version__ = "0.1.0"

__all__ = [
    "ConfigurationError",
    "FixPlan",
    "Fixm4bConfig",
    "Fixm4bError",
    "Fixm4bSettings",
    "apply_fix",
    "default_config_path",
    "get_settings",
    "plan_fix",
    "set_settings",
    "settings_from_cfg",
    "write_default_config",
    "__version__",
]
