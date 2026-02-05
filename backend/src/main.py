from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.auth_endpoints import router as auth_router
from .core.config import settings


def create_app():
    app = FastAPI(
        title="Authentication API",
        description="API for user authentication including registration, login, logout, and password reset",
        version="1.0.0"
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, replace with specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth_router)

    @app.get("/")
    def read_root():
        return {"message": "Authentication API is running"}

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)