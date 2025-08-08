from fastapi import FastAPI

from app.config.settings import envs
from app.presentation.api.boards import router as boards_router


app = FastAPI(
    title="Task Board API",
    description="Task Board API for managing tasks with Discord login and AI integration.",
    version="0.1.0",
    contact={"name": "Luis Eduardo Soares",
             "url": "https://github.com/luis0ares"},
    root_path=envs.API_PREFIX,
)


app.include_router(boards_router)
