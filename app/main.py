from fastapi import FastAPI

from app.routers import history, risk, safewalk

app = FastAPI(
    title="SafeWalk API",
    version="1.0.0",
    description="Backend service for SafeWalk risk assessment, check-ins, and safe-trip history.",
)

app.include_router(risk.router, prefix="/api/risk", tags=["Risk"])
app.include_router(safewalk.router, prefix="/api/safewalk", tags=["SafeWalk"])
app.include_router(history.router, prefix="/api/history", tags=["History"])


@app.get("/")
def root():
    return {
        "message": "SafeWalk backend is running",
        "version": "1.0.0",
        "service": "SafeWalk API",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
