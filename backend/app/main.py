from contextlib import asynccontextmanager

import httpx
from beanie import init_beanie
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pymongo import AsyncMongoClient

from app.config import settings
from app.models import DOCUMENT_MODELS
from app.routers import conditions, cryptids, sightings, subscribers
from app.services.conditions import LiveConditions


def user_agent() -> str:
    contact = f" (+mailto:{settings.contact_email})" if settings.contact_email else ""
    return f"MSAN/0.1{contact}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = AsyncMongoClient(settings.mongo_uri)
    await init_beanie(database=client[settings.mongo_db], document_models=DOCUMENT_MODELS)
    app.state.http = httpx.AsyncClient(timeout=10, headers={"User-Agent": user_agent()})
    app.state.live = LiveConditions(ttl_seconds=600)
    yield
    await app.state.http.aclose()
    await client.close()


app = FastAPI(title="M.S.A.N. API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(conditions.router)
app.include_router(cryptids.router)
app.include_router(sightings.router)
app.include_router(subscribers.router)


@app.get("/api/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}
