from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ResourseNotFound


async def _resource_not_found_handler(request: Request, exc: ResourseNotFound):
    return JSONResponse(status_code=404, content={"detail": exc.message})


def register_handlers(app: FastAPI):
    """Register all errors handlers for the app"""
    app.add_exception_handler(ResourseNotFound, _resource_not_found_handler)
