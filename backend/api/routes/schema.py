# backend/api/routes/schema.py

from fastapi import APIRouter, HTTPException, status
from services.schema_discovery import SchemaDiscovery

router = APIRouter()

@router.get("/api/schema", tags=["Schema"], summary="Get Auto-Discovered Database Schema")
async def get_current_schema():
    """
    Connects to the database and returns its auto-discovered structure.
    This is used by the frontend to visualize the schema[cite: 31, 139].
    """
    try:
        discovery_service = SchemaDiscovery()
        schema = discovery_service.analyze_database()
        if not schema.get("tables"):
            return {"message": "Successfully connected, but the database has no tables."}
        return schema
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze database schema: {str(e)}"
        )