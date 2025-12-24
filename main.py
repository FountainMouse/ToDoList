from fastapi import FastAPI
from src.api.v1.routers import projects, tasks 

app = FastAPI(
    title="ToDoList API",
    description="A RESTful API for managing ToDo Projects and Tasks.",
    version="1.0.0",
)

app.include_router(projects.router, prefix="/v1")
app.include_router(tasks.router, prefix="/v1") 

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the ToDoList Web API! Go to /docs for documentation."}
