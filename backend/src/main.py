import langchain
from fastapi import FastAPI
from .routes import router

app = FastAPI(title="Awesome Interactive Storytelling API")

# Include the story routes
app.include_router(router)
