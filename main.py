from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from infra.database import engine, Base
from api.routers import user_routes, vehicle_routes, sale_routes

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Vehicle Store API",
    description="API for vehicle dealership management system following Clean Architecture principles",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_routes.router)
app.include_router(vehicle_routes.router)
app.include_router(sale_routes.router)


@app.get("/")
async def root():
    """
    Root endpoint providing basic API information.

    Returns:
        Dict: API welcome message and version information
    """
    return {
        "message": "Welcome to Vehicle Store API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring API status.

    Returns:
        Dict: API health status information
    """
    return {
        "status": "healthy",
        "service": "Vehicle Store API"
    }