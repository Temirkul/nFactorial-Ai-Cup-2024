import langchain
from fastapi import FastAPI
from .routes import router as story_router

app = FastAPI(title="Awesome Interactive Storytelling API")

# Include the story routes
app.include_router(story_router)
