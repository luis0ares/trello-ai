from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import envs
from app.presentation.api.boards import router as boards_router
from app.presentation.api.tasks import router as tasks_router

app = FastAPI(
    title="Task Board API",
    description=' '.join(
        ["Task Board API for managing tasks with",
         "Discord login and AI integration."]
    ),
    version="0.1.0",
    contact={
        "name": "Luis Eduardo Soares",
        "url": "https://github.com/luis0ares",
        "email": "luisedu.soares@outlook.com"
    },
    root_path=envs.API_PREFIX,
)


origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(boards_router)
app.include_router(tasks_router)
