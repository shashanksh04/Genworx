from langchain_ollama import ChatOllama
# from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import time
import json

#################################### Setting up JSON Schemas ####################################
character_json_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "Character Name": {"type": "string"},
            "Character Description": {"type": "string"}
        },
        "required": ["Character Name", "Character Description"],
    },
}
character_output_parser = JsonOutputParser(schema=character_json_schema)

chapter_json_schema = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "Chapter Title": {"type": "string"},
            "Chapter Description": {"type": "string"}
        },
        "required": ["Chapter Title", "Chapter Description"],
    },
}
chapter_output_parser = JsonOutputParser(schema=chapter_json_schema)

#################################### Setting up Functions ####################################

def generate_characters(genre:str) -> list:
    character_generation_llm = ChatOllama(model="mistral:7b")
    generate_character_template = PromptTemplate(
    input_variables = [{"genre"}],
    template = """
        You are a helpful AI assistant. Generate a list of characters (around 15) 
        with a description relevant to the genre of {genre}.
        
        Output strictly as a JSON array with objects like this:
        [{{"Character Name": "Character Name 1",
        "Character Description": "Character 1 Description"}},
        {{"Character Name": "Character Name 2",
        "Character Description": "Character 2 Description"}}
        ]
        """
    )
    character_chain = generate_character_template | character_generation_llm | character_output_parser
    characters = character_chain.invoke({"genre": genre})
    characters_list = characters
    return characters_list


def generate_summary(genre:str, characters: list) -> str:
    summary_generation_llm = ChatOllama(model="qwen3:14b", temperature=0.9)
    generate_summary_template = PromptTemplate(
    input_variables= ["genre", "characters"],
    template=""" You are a well experienced story writer that's written several story books over the past several years. 
    Now create a story summary to outline a main story to be written for the genre {genre} with the following characters.
    {characters} 
    
    Write ONLY the story outline in 900 to 1000 words.
    Do NOT include any thinking process, explanations, themes, tone, or any other sections.
    Do NOT use <think> tags or any XML-like tags.
    Output ONLY the story summary paragraphs directly.
    Start immediately with the story content.

    """
    )
    summary_chain = generate_summary_template | summary_generation_llm | StrOutputParser()
    summary = summary_chain.invoke({"genre": genre, "characters": characters})
    summary_text = summary
    return summary_text


def generate_chapter_titles(characters, summary) -> list:
    chapter_title_generation_llm = ChatOllama(model="gemma3:12b")
    generate_chapter_titles_template = PromptTemplate(
    input_variables=["characters", "summary"],
    template=""" You are a well experienced story written that's written several story books over the past several years. 
        Now create a list of chapters along with the chapter description.(Atleast 10 chapters)
        
        CHARACTERS:
        {characters}

        SUMMARY:
        {summary}

        Output strictly as a JSON array with objects like this:
        [
            {{
                "Chapter Title": "",
                "Chapter Description": ""
            }},
            {{
                "Chapter Title": "",
                "Chapter Description": ""
            }},
        ]

    """
    )
    chapter_title_chain = generate_chapter_titles_template | chapter_title_generation_llm | chapter_output_parser
    chapter_titles = chapter_title_chain.invoke({"characters": characters, "summary": summary})
    chapter_titles = chapter_titles
    return chapter_titles


def generate_chapter_content(genre, characters, summary, chapter) -> str:
    chapter_generation_llm = ChatOllama(model="qwen3:14b", temperature=0.8)
    chapter_generation_template = PromptTemplate(
    input_variables=["genre", "characters", "summary", "chapter"],
    template="""
        You are a well experienced story written that's written several story books over the past several years. 
        You are given a genre of {genre}.
        A list of characters with their description:
        {characters}

        A story summary:
        {summary}

        The minimum word count for this chapter should be 3000 words. This chapter should be detailed and must have good flow.
        Now write the content for the chapter:
        {chapter}

        Do NOT include any thinking process, explanations, themes, tone, or any other sections.
        Do NOT use <think> tags or any XML-like tags.
        Output ONLY the story summary paragraphs directly.
        Start immediately with the story content.               
    """
    )
    chapter_generation_chain = chapter_generation_template | chapter_generation_llm | StrOutputParser()
    chapter_content = chapter_generation_chain.invoke({"genre": genre, "characters": characters, "summary": summary, "chapter": chapter})
    return chapter_content