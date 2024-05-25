import random
from fastapi import APIRouter, Depends
from .schemas import StoryResponse, StoryInput
from .genai import get_start_story_chain, get_continue_story_chain

router = APIRouter()

# it is better to use Depends from fastapi, but i don't have the time to figure that out right now
# i don't fully understand how Depends works and why it's needed, which is why i'll omit it.

# also, for now i'm simply injecting the whole context into the story which is obviously not scalable,
# but it will do for now. Ideally i'd like to use RAG and a vector database (mongodb) to extract the relevant parts of the story,
# and it is not difficult to implement this, but i need to really focus on the frontend right now.

@router.post("/start-story", response_model=StoryResponse)
async def start_story(
    themes: list[str] = [
        "Science fiction", 
        "Fantasy",
        "Thriller",
        "Romance",
        "Horror",
        "Novel",
        "Drama",
    ]
) -> StoryResponse:
    start_story_chain = get_start_story_chain()
    response = await start_story_chain.ainvoke(random.choice(themes))    
    return StoryResponse(story_text=response)


@router.post("/continue-story", response_model=StoryResponse)
async def continue_story(story_input: StoryInput) -> StoryResponse:
    continue_story_chain = get_continue_story_chain(story_context=story_input.story_context)
    response = await continue_story_chain.ainvoke(story_input.user_input)
    return StoryResponse(story_text=response)


@router.get("/generate-image")
async def generate_image(context):  # not sure about this for now. Do i need a response model? 
    pass 