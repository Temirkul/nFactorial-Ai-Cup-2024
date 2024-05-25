import random
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

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

    continue_story_result = get_continue_story_chain(story_context=start_story_result).invoke("I want to smoke.")
    
    test_prompt = ChatPromptTemplate.from_template("test prompt {input}")
    prompt_result = test_prompt.invoke(["list", "of", "strings"])
    
    print("**Theme**:", theme, "\n")
    print(start_story_result)
    print("===================================")
    print(continue_story_result)
    print("===================================")
    print(prompt_result.to_string())
    print("===================================")
    print(prompt_result)
    print("===================================")
    print(repr(prompt_result))
    print("===================================")