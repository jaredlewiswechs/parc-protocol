"""
HTTP-PARC Reference Server (Python)
===================================

A minimal, fully working UTF-PARC 1.0 server using FastAPI.

Run locally:

    pip install fastapi uvicorn
    uvicorn server.python.http_server:app --reload

This server implements:

    • POST /v1/parc/vector
    • POST /v1/parc/update
    • POST /v1/parc/batch
    • POST /v1/parc/meta
    • POST /v1/parc/validate
"""

from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

# ---------------------------------------------------------
# Import our local PARC engine
# ---------------------------------------------------------
from ...src.python.parc import (
    encode_text,
    update_state,
    validate_parc
)

app = FastAPI(title="UTF-PARC Reference Server")


# ---------------------------------------------------------
# Request/Response Models
# ---------------------------------------------------------

class VectorRequest(BaseModel):
    text: str
    confidence_hint: Optional[float] = None


class UpdateRequest(BaseModel):
    state: dict
    steps: int = 1
    params: dict


class BatchRequest(BaseModel):
    texts: List[str]


class MetaRequest(BaseModel):
    vector: dict
    meta: dict


class ValidateRequest(BaseModel):
    vector: dict


# ---------------------------------------------------------
# Endpoints
# ---------------------------------------------------------

@app.post("/v1/parc/vector")
def compute_vector(req: VectorRequest):
    state = encode_text(req.text, req.confidence_hint)
    return state


@app.post("/v1/parc/update")
def update_vector(req: UpdateRequest):
    result = update_state(req.state, req.steps, req.params)
    return result


@app.post("/v1/parc/batch")
def batch_vector(req: BatchRequest):
    results = [encode_text(t) for t in req.texts]
    return {"results": results}


@app.post("/v1/parc/meta")
def attach_meta(req: MetaRequest):
    vector = req.vector.copy()
    vector["_parc_meta"] = req.meta
    return vector


@app.post("/v1/parc/validate")
def validate(req: ValidateRequest):
    return validate_parc(req.vector)


# ---------------------------------------------------------
# Root
# ---------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "UTF-PARC Reference Server (Python)"
    }
