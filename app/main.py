import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from app.routes.conv_routes import router as conv_router
from app.routes.user_routes import router as user_router
from app.routes.log_routes import router as log_router

app = FastAPI(title="SWP Database API", version="1.0.0")

# Include routers
app.include_router(user_router)
app.include_router(log_router)
app.include_router(conv_router)


@app.get("/")
async def root():
    """Root endpoint - basic API status"""
    return {"message": "SWP Database API is running", "status": "healthy"}


@app.get("/health")
async def health_check():
    """Health check endpoint - doesn't require database access"""
    return {"status": "healthy", "message": "Service is running"}


@app.get("/health/db")
async def database_health_check():
    """Database health check endpoint - tests database connectivity"""
    try:
        from app.db import get_client
        client = get_client()
        # Ping the database to check connectivity
        await client.admin.command('ping')
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Database connection failed: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors"""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "message": str(exc)}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)