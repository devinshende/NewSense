from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import logging
import model  # Import the model.py module

logging.basicConfig(level=logging.INFO)
app = FastAPI()

# Enable CORS so the HTML frontend can call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (for development)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model for text transformation
class TransformRequest(BaseModel):
    text: str
    mode: str = 'brainrot'


@app.get("/")
def read_root():
    return {"message": "Text received from canvas.html", "status": "running"}


@app.post("/transform")
async def transform_text_endpoint(request: TransformRequest):
    """
    Receives text and mode from canvas.html and returns transformed text from model.py
    """
    # Call the transform_text function from model.py
    result = model.transform_text(request.text, request.mode)
    logging.info("/transform called: mode=%s text_len=%d", request.mode, len(request.text or ""))
    return result
    logging.info("/transform result: %s", {k: (v if k != 'transformed_text' else '<omitted>') for k, v in result.items()})


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}