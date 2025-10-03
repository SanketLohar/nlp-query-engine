from dotenv import load_dotenv 
load_dotenv()     



import os
from sqlalchemy import create_engine, inspect
from typing import Dict, Any

class SchemaDiscovery:
    """
    A service to dynamically discover the schema of a SQL database.
    It connects to the database and extracts metadata without hard-coded values.
    """
    def __init__(self, connection_string: str = None):
        if connection_string is None:
            connection_string = os.getenv("DATABASE_URL")

        if not connection_string:
            raise ValueError("Database connection string is not provided or configured.")
        
        self.engine = create_engine(connection_string)
        self.inspector = inspect(self.engine)

    def analyze_database(self) -> Dict[str, Any]:
        """
        Analyzes the database to discover tables, columns, and relationships.

        Returns:
            A dictionary representing the database schema.
        """
        schema_info = {"tables": {}}
        table_names = self.inspector.get_table_names()

        for table_name in table_names:
            columns = self.inspector.get_columns(table_name)
            foreign_keys = self.inspector.get_foreign_keys(table_name)
            
            schema_info["tables"][table_name] = {
                "columns": [
                    {"name": col['name'], "type": str(col['type'])} for col in columns
                ],
                "foreign_keys": [
                    {
                        "constrained_columns": fk['constrained_columns'],
                        "referred_table": fk['referred_table'],
                        "referred_columns": fk['referred_columns'],
                    } for fk in foreign_keys
                ]
            }
        
        return schema_info