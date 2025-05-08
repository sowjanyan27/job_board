# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# from app.api.routes import users
# import logging
# # from app.middleware.request_duration import RequestDurationMiddleware
#
# app = FastAPI(title="Job Board API")
# # app.add_middleware(RequestDurationMiddleware)
#
# # Global error handler (optional)
# @app.exception_handler(Exception)
# async def general_exception_handler(request: Request, exc: Exception):
#     logging.error(f"Unhandled error: {exc}")
#     return JSONResponse(
#         status_code=500,
#         content={"detail": "Internal Server Error"},
#     )
#
# app.include_router(users.router, prefix="/users", tags=["Users"])
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.gzip import GZipMiddleware
from app.api.routes import users,jobs
import logging
from fastapi.middleware.cors import CORSMiddleware
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

# Optional global error handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )
# Include your router
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(jobs.router,prefix="/jobs",tags=["Jobs"])
