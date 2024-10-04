from fastapi import FastAPI
from .routers import categories, locations, recommendations, reviews
from .database import engine
from . import models
from fastapi.middleware.cors import CORSMiddleware
import logging

logging.basicConfig(level=logging.INFO)

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Map My World API",
    description="REST API for managing locations and categories, and providing exploration recommendations for 'Map My World'.",
    version="1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])
app.include_router(locations.router, prefix="/api/v1/locations", tags=["Locations"])
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["Recommendations"])
app.include_router(reviews.router, prefix="/api/v1/reviews", tags=["Reviews"])