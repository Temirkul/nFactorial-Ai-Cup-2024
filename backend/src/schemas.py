from pydantic import BaseModel

class StoryInput(BaseModel):
    story_context: str
    user_input: str
    

class StoryResponse(BaseModel):
    story_text: str
