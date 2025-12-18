from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from app.orchestrator import Orchestrator

app = FastAPI()
orchestrator = Orchestrator()


class QueryRequest(BaseModel):
    query: str
    propertyId: Optional[str] = None


@app.post("/query")
def handle_query(request: QueryRequest):
    response = orchestrator.handle_query(
        query=request.query,
        property_id=request.propertyId
    )
    return response
