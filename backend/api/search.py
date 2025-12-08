"""
Stub search API.
Placeholder to satisfy task list; actual search implementation pending.
"""
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/search/placeholder")
def search_placeholder():
    """Temporary endpoint indicating search is not yet implemented."""
    raise HTTPException(status_code=501, detail="Search API not implemented")


__all__ = ["router"]
