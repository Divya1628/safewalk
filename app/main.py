from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.routers import adaptive_shield, auth, history, risk, safewalk

app = FastAPI(
    title="SafeWalk API with Adaptive Safety Shield",
    version="2.0.0",
    description="Backend with user authentication, AI-driven risk assessment, multi-signal fusion, and adaptive covert duress alerts.",
)

# Enable CORS for mobile apps
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(risk.router, prefix="/api/risk", tags=["Risk"])
app.include_router(safewalk.router, prefix="/api/safewalk", tags=["SafeWalk"])
app.include_router(history.router, prefix="/api/history", tags=["History"])
app.include_router(
    adaptive_shield.router,
    prefix="/api/shield",
    tags=["Adaptive Safety Shield"],
)


@app.get("/")
async def root():
    return FileResponse("templates/index.html")


@app.get("/dashboard")
async def dashboard():
    return FileResponse("templates/index.html")


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "SafeWalk API",
        "version": "2.0.0",
        "authentication": "JWT",
        "adaptive_shield": "enabled",
        "covert_alerts": "active",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
