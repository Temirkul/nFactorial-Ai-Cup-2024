from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes import router

app = FastAPI(title="Awesome Interactive Storytelling API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specifies the origins which can send requests.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods.
    allow_headers=["*"],  # Allows all headers.
)

# Include the story routes
app.include_router(router)
