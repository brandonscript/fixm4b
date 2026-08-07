"""Shared metadata planning / apply package (fix_metadata CLI + convert)."""

from fixm4b.metadata.apply import apply_fix
from fixm4b.metadata.models import CliPaths, FixPlan, SourceResolutionError, TagSnapshot
from fixm4b.metadata.ol_attach import (
    _apply_date_consensus,
    _apply_ol_fields_to_desired,
    _attach_open_library,
    resolve_date_consensus,
    _year_consensus,
)
from fixm4b.metadata.pick import resolve_minimalist
from fixm4b.metadata.plan import plan_fix
from fixm4b.metadata.priors import (
    filesystem_extracted,
    folder_narrator_hint,
    folder_title_hint,
    parent_author_hint,
)
from fixm4b.metadata.settings import Fixm4bSettings, get_settings, set_settings, settings_from_cfg
from fixm4b.metadata.sources import (
    map_source_dir,
    resolve_source_dir,
    source_common_filename,
    source_common_title,
    source_files_display,
    filename_gcs_context,
)
from fixm4b.metadata.stem import (
    _looks_like_title,
    _stem_matches_book_title,
    _usable_rename_stem,
    preserve_original_year_in_stem,
    year_suffix_from_stem,
)

__all__ = [
    "CliPaths",
    "FixPlan",
    "Fixm4bSettings",
    "SourceResolutionError",
    "TagSnapshot",
    "apply_fix",
    "filesystem_extracted",
    "folder_narrator_hint",
    "folder_title_hint",
    "get_settings",
    "map_source_dir",
    "parent_author_hint",
    "plan_fix",
    "resolve_minimalist",
    "resolve_source_dir",
    "set_settings",
    "settings_from_cfg",
    "source_common_filename",
    "source_common_title",
    "source_files_display",
    "filename_gcs_context",
    "_apply_date_consensus",
    "_apply_ol_fields_to_desired",
    "_attach_open_library",
    "_looks_like_title",
    "_stem_matches_book_title",
    "_usable_rename_stem",
    "_year_consensus",
    "resolve_date_consensus",
    "preserve_original_year_in_stem",
    "year_suffix_from_stem",
]
