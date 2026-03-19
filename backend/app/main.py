from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import close_db, init_db
from app.publications.router import router as publications_router
from app.redis import close_redis, init_redis
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await init_redis()
    yield
    await close_redis()
    await close_db()


app = FastAPI(
    title="Publication Feed API",
    description="Лента публикаций с кэшированием и JWT-авторизацией",
    version="1.0.0",
    lifespan=lifespan,
)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(users_router, prefix="/api")
app.include_router(publications_router, prefix="/api")


@app.get("/health")
async def health():
    return {"status": "ok"}
