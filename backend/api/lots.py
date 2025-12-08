"""
Compatibility shim to align with task file paths.
Re-exports the v1 lots router.
"""
from backend.api.v1.endpoints import lots as v1_lots

router = v1_lots.router

__all__ = ["router"]
