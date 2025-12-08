"""
Compatibility shim to align with task file paths.
Re-exports the v1 attendance router.
"""
from backend.api.v1.endpoints import attendance as v1_attendance

router = v1_attendance.router

__all__ = ["router"]
