"""fixm4b errors."""

from __future__ import annotations


class Fixm4bError(Exception):
    """Base package error."""


class ConfigurationError(Fixm4bError):
    """Invalid or conflicting configuration."""
