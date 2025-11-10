from langchain_ollama import ChatOllama
# from langchain.agents import create_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
import time
import json

import os
os.makedirs("data", exist_ok=True)
os.makedirs("data/chapters", exist_ok=True)
os.makedirs("data/raw", exist_ok=True)           

#################################### Timer Setup ####################################

start = time.time()

#################################### Misc Function ####################################
def save_json(filename, data):
    with open(f"data/raw/{filename}.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

def save_txt(filename, data):
    with open(f"data/raw/{filename}.txt", "w", encoding="utf-8") as file:
        file.write(data)
#################################### LLM Setup ####################################
# main_llm = ChatOllama(model="mistral:7b")

character_generation_llm = ChatOllama(model="mistral:7b")
summary_generation_llm = ChatOllama(model="qwen3:14b", temperature=0.9)
chapter_title_generation_llm = ChatOllama(model="gemma3:12b")
chapter_generation_llm = ChatOllama(model="qwen3:14b", temperature=0.8)

genre_list = [
    "Thriller", 
    "Romance", 
    "Crime",
    "Comedy",
    "Action",
    "Adventure",
    "Science Fiction",
    "Fantasy",
    "Horror",
    "Drama",
    "Young Adult"
]

print("Choose a Genre to generate a story")
for g in genre_list:
    print(g)
genre = input("> ")
# genre = "Action"


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


#################################### Prompt Templates ####################################
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
    
    

#################################### Invoking Character Chain ####################################
character_chain = generate_character_template | character_generation_llm | character_output_parser
characters = character_chain.invoke({"genre": genre})
character_list = characters
print(character_list)
save_json("character_list", character_list)

print("/n")
print(f"Character Generation {time.time() - start:.2f} seconds")


print("\n\n\n\n\n\n\n\n\n")

#################################### Invoking Summary Chain ####################################
summary_chain = generate_summary_template | summary_generation_llm | StrOutputParser()
summary = summary_chain.invoke({"genre": genre, "characters": character_list})
summary_text = summary
print(summary_text)
save_txt("summary", summary_text)

print("/n")
print(f"Summary Generation {time.time() - start:.2f} seconds")


print("\n\n\n\n\n\n\n\n\n")

#################################### Invoking Chapter Title Generation Chain ####################################
chapter_title_chain = generate_chapter_titles_template | chapter_title_generation_llm | chapter_output_parser
chapter_titles = chapter_title_chain.invoke({"characters": character_list, "summary": summary_text})
chapter_titles = chapter_titles
print(chapter_titles)
save_json("chapter_title_list", chapter_titles)

print("/n")
print(f"Chapter Title Generation {time.time() - start:.2f} seconds")


print("\n\n\n\n\n\n\n\n\n")

#################################### Chapter Content Generation Chain ####################################
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
    """
)

i = 1
for chapter in chapter_titles:
    chapter_title = chapter["Chapter Title"]
    chapter_desc = chapter["Chapter Description"]

    chapter_generation_chain = chapter_generation_template | chapter_generation_llm | StrOutputParser()
    chapter_content = chapter_generation_chain.invoke({"genre": genre, "characters": characters, "summary": summary_text, "chapter": chapter})
    # chapter_content = chapter_content
    print(chapter_content)
    with open(f"data/chapters/{i}) {chapter_title}.txt", "w", encoding="utf-8") as f:
        f.write(chapter_content)
    i = i + 1
    print(f"Chapter Generation {time.time() - start:.2f} seconds")
    print("\n\n\n\n\n\n\n\n\n")

print(f"Chapter Generation {time.time() - start:.2f} seconds")