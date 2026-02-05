from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
import time
import asyncio

from src.database.session import get_db_session

router = APIRouter()


@router.get("/health")
async def health_check():
    """
    Basic health check endpoint
    """
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "todo-backend"
    }


@router.get("/health/db")
async def database_health_check(db: AsyncSession = Depends(get_db_session)):
    """
    Database health check endpoint
    Tests connectivity to the database
    """
    try:
        # Execute a simple query to test database connectivity
        start_time = time.time()

        # Using raw SQL to test connection
        result = await db.execute("SELECT 1")
        db_result = result.fetchone()

        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds

        if db_result:
            return {
                "status": "healthy",
                "timestamp": time.time(),
                "database": "reachable",
                "response_time_ms": round(response_time, 2)
            }
        else:
            raise HTTPException(status_code=503, detail="Database test query failed")

    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@router.get("/health/ready")
async def readiness_check(db: AsyncSession = Depends(get_db_session)):
    """
    Readiness check - confirms that the service is ready to accept traffic
    Checks both basic health and database connectivity
    """
    try:
        # Test database connectivity
        result = await db.execute("SELECT 1")
        db_result = result.fetchone()

        if not db_result:
            return {
                "status": "not_ready",
                "reason": "Database not accessible",
                "timestamp": time.time()
            }

        # Additional checks could be added here
        # e.g., checking if required services are available

        return {
            "status": "ready",
            "timestamp": time.time(),
            "checks": {
                "database": "ok"
            }
        }

    except Exception as e:
        return {
            "status": "not_ready",
            "reason": f"Database connection failed: {str(e)}",
            "timestamp": time.time()
        }


@router.get("/health/live")
async def liveness_check():
    """
    Liveness check - confirms that the service itself is alive and functioning
    This is a basic check that the service is responding to requests
    """
    # Perform any internal health checks here
    # For now, just return healthy if we reach this point

    return {
        "status": "alive",
        "timestamp": time.time(),
        "service": "running"
    }