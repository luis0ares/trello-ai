import logging
import contextvars
from pathlib import Path

from app.config.settings import envs


# context to store request id
request_id_ctx = contextvars.ContextVar("request_id", default=None)

# Custom logger to use throughout the app
logger = logging.getLogger("app")
logger.setLevel(envs.LOG_LEVEL)


# Custom Filter to add request id to logs
class RequestIdFilter(logging.Filter):
    def filter(self, record):
        # default request id for logs out of a http request context
        if not hasattr(record, "request_id"):
            record.request_id = request_id_ctx.get() or "app"
        return True


log_formatter = logging.Formatter(
    envs.LOG_FORMAT,
    datefmt='%Y-%m-%dT%H:%M:%S%z'
)

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
console_handler.setLevel(envs.LOG_LEVEL)
logger.addHandler(console_handler)

file_handler = logging.FileHandler(Path("app.log"))
file_handler.setFormatter(log_formatter)
file_handler.setLevel(envs.LOG_LEVEL)
logger.addHandler(file_handler)

logger.addFilter(RequestIdFilter())

if envs.DATABASE_ECHO:
    sqlalchemy_logger = logging.getLogger('sqlalchemy')
    sqlalchemy_logger.handlers.clear()
    sqlalchemy_logger.propagate = False

    sqlalchemy_logger.addHandler(console_handler)
    sqlalchemy_logger.addHandler(file_handler)
    sqlalchemy_logger.addFilter(RequestIdFilter())

for name in logging.root.manager.loggerDict:
    if name.startswith("uvicorn"):
        logger.info(f"Logger '{name}' disabled")
        logging.getLogger(name).disabled = True
