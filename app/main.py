from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import categories, locations, recommendations, reviews
from .database import engine
from . import models
import logging
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Map My World API",
    description="REST API for managing locations and categories, and providing exploration recommendations for 'Map My World'.",
    version="1.0.0"
)

# Configure CORS
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["Locations"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])

@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint that returns a welcome message.

    Returns:
        dict: A dictionary containing a welcome message.
    """
    return {"message": "Welcome to Map My World API"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)