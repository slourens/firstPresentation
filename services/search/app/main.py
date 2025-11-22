from datetime import datetime
from typing import Dict, List

from services.common.compat import BaseModel, FastAPI, Field

app = FastAPI(title="search-service")


class SearchQuery(BaseModel):
    query: str = Field(..., description="Full-text search query")
    limit: int = Field(default=10, ge=1, le=50)


class SearchResult(BaseModel):
    upload_id: str
    score: float
    snippet: str


class SearchResponse(BaseModel):
    results: List[SearchResult]
    generated_at: datetime


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.post("/search", response_model=SearchResponse)
def search(payload: SearchQuery) -> SearchResponse:
    placeholder = SearchResult(upload_id="demo", score=1.0, snippet=f"Echo: {payload.query}")
    return SearchResponse(results=[placeholder], generated_at=datetime.utcnow())
