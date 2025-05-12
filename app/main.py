
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from starlette.middleware.gzip import GZipMiddleware
from app.api.routes import users,jobs,resumes
import logging
from fastapi.middleware.cors import CORSMiddleware
from scheduler import start_scheduler
app = FastAPI(title="Job Board API")
# ✅ Add CORS middleware right after app initialization
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # React development server URL
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)
# Add GZIP compression
app.add_middleware(GZipMiddleware, minimum_size=500)  # Only compress responses larger than 500 bytes
start_scheduler()
# Optional global error handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )



class Item(BaseModel):
    name: str
    price: float

@app.post("/items/")
def create_item(item: Item):
    return item



# Include your router
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(jobs.router,prefix="/jobs",tags=["Jobs"])
app.include_router(resumes.router,prefix="/Resumes",tags=["Resumes"])
