from fastapi import FastAPI


app = FastAPI(
    title="Task Board API",
    description="Task Board API for managing tasks with Discord login and AI integration.",
    version="0.1.0",
    contact={"name": "Luis Eduardo Soares",
             "url": "https://github.com/luis0ares"},
)


@app.get("/", include_in_schema=False)
def root():
    return {
        "docs": "/docs",
        "redoc": "/redoc",
        "openapi.json": "/openapi.json"
    }
