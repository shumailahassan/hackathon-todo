from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api import auth, users, data, health
from src.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="0.1.0",
    description="Todo Web Application API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(data.router, prefix="/data", tags=["data"])
app.include_router(health.router, prefix="", tags=["health"])  # Health endpoints at root level

@app.get("/")
def read_root():
    return {"message": "Todo Web Application API"}