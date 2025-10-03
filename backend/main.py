# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware # <--- This is the missing import
from api.routes import schema, query

app = FastAPI(
    title="NLP Query Engine API",
    description="API for querying employee data using natural language.",
    version="0.1.0"
)

# --- ADD THIS MIDDLEWARE CONFIGURATION ---
origins = [
    "http://localhost:3000", # The address of your React frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], # Allow all methods
    allow_headers=["*"], # Allow all headers
)
# -----------------------------------------


@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok", "message": "Welcome to the NLP Query Engine API!"}

# Include the routers
app.include_router(schema.router)
app.include_router(query.router)