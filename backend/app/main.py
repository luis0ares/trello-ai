from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.middleware import register_middleware
from app.config.settings import envs
from app.presentation.api.boards import router as boards_router
from app.presentation.api.tasks import router as tasks_router
from app.presentation.handlers import register_handlers
from app.presentation.socket.tasks import router as ws_tasks_router

app = FastAPI(
    title="Task Board API",
    description=' '.join(
        ["Task Board API for managing tasks with",
         "Discord login and AI integration."]
    ),
    version="0.1.0",
    contact={
        "name": "Luis Eduardo Soares",
        "url": "https://www.linkedin.com/in/luis0ares",
        "email": "luisedu.soares@outlook.com"
    },
    root_path=envs.API_PREFIX,
)


# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=envs.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=envs.CORS_METHODS,
    allow_headers=envs.CORS_HEADERS,
)
# Logging middlewares
register_middleware(app)
# Register exception handlers
register_handlers(app)
# REST Routes
app.include_router(boards_router)
app.include_router(tasks_router)
# Websocket Routes
app.include_router(ws_tasks_router)
