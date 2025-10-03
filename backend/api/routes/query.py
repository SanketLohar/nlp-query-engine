# backend/api/routes/query.py

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from services.query_engine import QueryEngine
from services.schema_discovery import SchemaDiscovery
from services.document_processor import DocumentProcessor

router = APIRouter()

# Initialize services once on startup for efficiency
schema_service = SchemaDiscovery()
doc_processor = DocumentProcessor(doc_folder_path="../documents") # Point to the root documents folder
query_engine = QueryEngine()

class QueryRequest(BaseModel):
    query: str

@router.post("/api/query", tags=["Query"], summary="Process a hybrid natural language query")
async def process_query(request: QueryRequest):
    """
    Takes a natural language query, searches for relevant documents,
    converts it to SQL, executes it, and returns a combined result.
    """
    try:
        # 1. Search documents
        doc_results = doc_processor.search(request.query)

        # 2. Get schema and generate SQL
        schema = schema_service.analyze_database()
        if not schema.get("tables"):
             raise HTTPException(status_code=400, detail="No database tables found.")
        
        generated_sql = query_engine.text_to_sql(request.query, schema)
        sql_results = query_engine.execute_sql_query(generated_sql)

        # 3. Return the combined results
        return {
            "natural_language_query": request.query,
            "document_results": doc_results,
            "sql_results": {
                "generated_sql": generated_sql,
                "results": sql_results
            }
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}"
        )