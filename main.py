from fastapi import FastAPI

import models
from database import engine

from routers import (
    auth,
    candidates,
    interviews,
    feedback,
    reports
)

# Create Database Tables
models.Base.metadata.create_all(bind=engine)

# Create FastAPI App
app = FastAPI(
    title="Interview Scheduling & Candidate Tracking System",
    description="FastAPI Backend Application",
    version="1.0.0"
)

# Include Routers
app.include_router(auth.router)
app.include_router(candidates.router)
app.include_router(interviews.router)
app.include_router(feedback.router)
app.include_router(reports.router)


# Home Endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to Interview Scheduling & Candidate Tracking System"
    }