import os
import random
import requests
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from PIL import Image
from io import BytesIO

# ideally i'd like all of these to be agents to facilitate more interactivity, but chains will do for now..
# also, it's better to use function calling and structured output than PydanticOutputParser (see vid on function calling)

def get_start_story_chain(delimeters: str = "```"):
    llm = ChatOpenAI(model="gpt-4o")  # make sure you setup "OPENAI_API_KEY" env variable
    
    story_template = """You are an expert storyteller and worldbuilder.
    You have written multiple best selling books that cover a wide range of genres,
    such as science fiction, fantasy, detectives, romance, novels, thrillers, and so on.
    
    You will be given a theme from which you need to create an introduction to an engaging story.
    The introduction shouldn't be too long and it should captivate the reader's attention,
    it should pull the reader in and make him interested with the story;
    make sure the the introduction also includes lucid visual descriptions of the setting of the story.
    Importantly, make sure to make the reader a part of the story, let the reader be a character in this story.
    
    The list of themes are provided below, surrounded by the {delimeters} delimeters.
    
    Themes: {delimeters}{theme}{delimeters}
    """
    
    prompt = ChatPromptTemplate.from_template(story_template).partial(delimeters=delimeters)
    
    chain = {"theme": RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    return chain


def get_continue_story_chain(story_context: str, delimeters: str = "```"):
    llm = ChatOpenAI(model="gpt-4o")
    
    story_template = [
        (
            "system",
            """You are an expert storyteller and worldbuilder. 
            You have written multiple best selling books that cover a wide range of genres.
            You will be given a story that has been generated so far, 
            and your task is to continue the story based on the story so far and the user input.
            Do not make decisions for the user in the story.
            The story that has been generated so far is provided below, surrounded by the {delimeters} delimeters.
            
            Story: {delimeters}{story_context}{delimeters}
            """ 
        ),
        (
            "human", "{user_input}"
        ),
        (
            "system", 
            """With this user input, be sure to incorporate it into the story when generating the continuation of the story. 
            The user's actions must have an impact on the story, the user should interact with the story and vice versa.
            Do not make decisions for the user in the story."""
        )
    ]
    
    prompt = ChatPromptTemplate.from_messages(story_template).partial(story_context=story_context, delimeters=delimeters)
    
    chain = {"user_input": RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    return chain


def get_generate_image_chain(delimeters="```"):  # this should be an agent ideally that decides whether or not to generate an image
    llm = ChatOpenAI(model="gpt-4o")
    
    image_template = """You are an expert prompt engineer. 
    Your task is to prompt a stable diffusion image generation model. 
    The prompt for the image generation model is to be based on the input text below.
    The prompt that you generate should vividly describe the content of the input text in a realistic style.
    Be concise.
    Be sure to mention realistic/hyper realistic style in the prompt.
    Do not narrate your outputs in any way, only output the prompt for the stable diffusion image generation model, do not output anything else.
    
    The input text is provided below, and it is enclosed in the {delimeters} delimeters.    
    
    Input text: {delimeters}{input_text}{delimeters}
    """
    
    prompt = ChatPromptTemplate.from_template(image_template).partial(delimeters=delimeters)
    
    chain = {"input_text": RunnablePassthrough()} | prompt | llm | StrOutputParser()
    
    return chain


def generate_image(prompt: str) -> Image.Image | None:
    engine_id = "stable-diffusion-xl-1024-v1-0"
    api_host = os.getenv("API_HOST", "https://api.stability.ai")
    api_key = os.getenv("STABILITY_API_KEY")

    if api_key is None:
        raise Exception("Missing Stability API key.")

    response = requests.post(
        f"{api_host}/v1/generation/{engine_id}/text-to-image",
        headers={
            "Content-Type": "application/json",
            "Accept": "image/png",
            "Authorization": f"Bearer {api_key}"
        },
        json={
            "text_prompts": [
                {
                    "text": f"{prompt}"
                }
            ],
            "cfg_scale": 7,
            "height": 1024,
            "width": 1024,
            "samples": 1,
            "steps": 30,
        },
    )
    
    if response.status_code == 200:
        image_data = response.content
        image = Image.open(BytesIO(image_data))  # ! 
        return image
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None


# for testing
if __name__ == "__main__":
    theme = random.choice([
        "Science fiction", 
        "Fantasy",
        "Thriller",
        "Romance",
        "Horror",
        "Novel",
        "Drama",
    ])
    start_story_result = get_start_story_chain().invoke(theme)
    start_story_image_prompt = get_generate_image_chain().invoke(start_story_result)
    start_story_image = generate_image(start_story_image_prompt)
    start_story_image.save("generated_image_1.png")

    continue_story_result = get_continue_story_chain(story_context=start_story_result).invoke("I want to smoke.")
    continue_story_image_prompt = get_generate_image_chain().invoke(continue_story_result)
    continue_story_image = generate_image(continue_story_image_prompt)
    continue_story_image.save("generated_image_2.png")
    
    test_prompt = ChatPromptTemplate.from_template("test prompt {input}")
    prompt_result = test_prompt.invoke(["list", "of", "strings"])
    
    print("**Theme**:", theme, "\n")
    print(start_story_result)
    print("===================================")
    print(continue_story_result)
    print("===================================")
    print(start_story_image_prompt)
    print("===================================")
    print(continue_story_image_prompt)
    print("===================================")
    print(prompt_result.to_string())
    print("===================================")
    print(prompt_result)
    print("===================================")
    print(repr(prompt_result))
    print("===================================")
