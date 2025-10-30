from langchain_ollama.llms import OllamaLLM
from langchain_classic.prompts import PromptTemplate
from langchain_classic.schema.runnable import RunnableMap, RunnableSequence

llm_generator = OllamaLLM(model="mistral:7b", temperature=0.6)
tweet_template = """
    Generate an engaging tweet about the following topic in under 250 characters:
    Topic: {topic}
    Tweet:
    """
prompt_generator = PromptTemplate(input_variables=["topic"], template=tweet_template)
tweet_generator = prompt_generator | llm_generator


llm_verifier = OllamaLLM(model="gemma3:4b", temperature=0.3)
verify_template = """
    You are an expert content verifier. Evaluate this tweet and respond with "Valid" if it is well-written and relevant, otherwise respond "Invalid".
    Tweet: {tweet}
    Verification:
    """
prompt_verifier = PromptTemplate(input_variables=["tweet"], template=verify_template)
tweet_verifier = prompt_verifier | llm_verifier

def generate(inputs):
    return tweet_generator.invoke({"topic": inputs["topic"]})

def verify(inputs):
    return tweet_verifier.invoke({"tweet": inputs["tweet"]})

def generate_and_verify(inputs):
    generated_tweet = generate(inputs)
    verification = verify({"tweet": generated_tweet})
    return {"tweet": generated_tweet, "verification": verification}

tweet_chain = RunnableMap({"run": generate_and_verify})