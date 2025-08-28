import uuid
import logging
import contextvars
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.config.settings import envs


uvicorn_error = logging.getLogger('uvicorn.error')
uvicorn_error.disabled = False
uvicorn_access = logging.getLogger('uvicorn.access')
uvicorn_access.disabled = True

# context to store request id
request_id_ctx = contextvars.ContextVar("request_id", default=None)

# Custom logger to use throughout the app
logger = logging.getLogger("app")
logger.setLevel(envs.LOG_LEVEL)


# configuration
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        # default request id for logs out of a http request context
        if not hasattr(record, "request_id"):
            record.request_id = request_id_ctx.get() or "app"
        return True


handler = logging.StreamHandler()
formatter = logging.Formatter(
    envs.LOG_FORMAT,
    datefmt='%Y-%m-%dT%H:%M:%S%z'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.addFilter(RequestIdFilter())

if envs.DATABASE_ECHO:
    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    sqlalchemy_logger.handlers.clear()
    sqlalchemy_logger.propagate = False

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter(
        envs.LOG_FORMAT, datefmt='%Y-%m-%dT%H:%M:%S%z',
    )
    ch.setFormatter(formatter)
    sqlalchemy_logger.addHandler(ch)
    sqlalchemy_logger.addFilter(RequestIdFilter())


class RequestTrackingMiddleware(BaseHTTPMiddleware):
    # Middleware to intercept every request and gerenare a request_id
    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request_id_ctx.set(request_id)

        # Forward client ip
        client_ip = request.headers.get(
            "X-Forwarded-For", request.client.host).split(",")[0].strip()

        response = await call_next(request)

        # request logging
        logger.info(f"[{client_ip}][{request.method}] " +
                    f"{request.url}[{response.status_code}]")

        response.headers["X-Request-ID"] = request_id
        return response


logger.info("Logger configured successfully.")
