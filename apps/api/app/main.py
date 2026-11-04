from fastapi import FastAPI

from app.routers.analyses import router as analyses_router
from app.routers.health import router as health_router
from app.routers.recordings import router as recordings_router
from app.routers.vocab import router as vocab_router

app = FastAPI(title="Speaking Coach API", version="0.1.0")

app.include_router(health_router)
app.include_router(recordings_router)
app.include_router(analyses_router)
app.include_router(vocab_router)


@app.get("/")
async def root() -> dict:
    return {"message": "Speaking Coach API is running."}
