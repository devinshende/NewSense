"""FastAPI server for key-phrase extraction."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import uvicorn

from keyphrase_extractor import extract_keyphrases


class TextRequest(BaseModel):
    """Text input with optional sampling parameters."""
    text: str = Field(..., min_length=1)
    p: float = Field(default=1.0, ge=0.0, le=1.0)


class ExtractionResponse(BaseModel):
    """Extraction response with keyphrases."""
    keyphrases: List[List[int]]


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    message: str


app = FastAPI(
    title="Key-Phrase Extraction API",
    description="Extract key phrases from text and return their indices",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Health check."""
    return {"status": "ok", "message": "API running. Visit /docs for documentation."}


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check."""
    return {"status": "ok", "message": "healthy"}


@app.post("/extract", response_model=ExtractionResponse)
async def extract_phrases(request: TextRequest):
    """Extract key phrases from text and return indices as [[start, end], ...]."""
    try:
        keyphrases = extract_keyphrases(
            text=request.text,
            p=request.p,
        )
        return ExtractionResponse(keyphrases=keyphrases)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)

