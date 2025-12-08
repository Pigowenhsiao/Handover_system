"""
Compatibility shim to align with task file paths.
Re-exports the v1 reports router.
"""
from backend.api.v1.endpoints import reports as v1_reports

router = v1_reports.router

__all__ = ["router"]
