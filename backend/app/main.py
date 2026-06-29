"""
app/main.py — FastAPI application entrypoint.

Run with:
    uvicorn app.main:app --reload --port 8000
"""

from __future__ import annotations

import logging
import math
import json


from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.responses import JSONResponse

from .config import app_config
from .routers import (
    congestion, copilot, economic, evidence, forecast, hotspots,
    overview, patrol, scenarios, system,
    impact_scores, intelligence, events, executive,
)
from .services.artifact_loader import ArtifactError

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("parksight.api")

class SafeJSONResponse(JSONResponse):
    def render(self, content) -> bytes:
        def sanitize(obj):
            if isinstance(obj, float) and not math.isfinite(obj):
                return None
            if isinstance(obj, dict):
                return {k: sanitize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [sanitize(v) for v in obj]
            return obj
        return json.dumps(sanitize(content)).encode("utf-8")

app = FastAPI(
    title="ParkSight AI API",
    description="Backend integration layer serving real ParkSight pipeline outputs to the React dashboard.",
    version="1.0.0",
    default_response_class=SafeJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=app_config.frontend_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=app_config.gzip_min_size_bytes)


@app.exception_handler(ArtifactError)
async def artifact_error_handler(request: Request, exc: ArtifactError) -> JSONResponse:
    status_code = 422 if exc.code == "MALFORMED_ARTIFACT" else 404
    return JSONResponse(status_code=status_code, content={"error": exc.to_dict()})


for router in (
    system.router, overview.router, hotspots.router, hotspots.nonjunction_router,
    congestion.router, patrol.router, forecast.router, economic.router,
    evidence.router, scenarios.router, copilot.router,
    impact_scores.router, intelligence.router, events.router, executive.router,
):
    app.include_router(router)


@app.get("/")
def root() -> dict:
    return {"service": "ParkSight AI API", "docs": "/docs", "health": "/api/health"}