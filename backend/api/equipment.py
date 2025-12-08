"""
Compatibility shim to align with task file paths.
Re-exports the v1 equipment router.
"""
from backend.api.v1.endpoints import equipment as v1_equipment

router = v1_equipment.router

__all__ = ["router"]
