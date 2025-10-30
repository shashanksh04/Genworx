##### Tweet Generatoring with Local Ollama Models using LangChain

### Project Overview
This project is a tweet generation and verification chatbot powered by LangChain and Ollama large language models. Using FastAPI as the web framework, it exposes an API where users can provide a topic, generate a creative tweet about it, and have the tweet verified by a second model for quality and relevance.
The system demonstrates modern AI integration by chaining multiple LLMs together, showcasing the potential of composable AI applications for social media content creation and automated content moderation.

### Features
- Generate engaging, creative tweets about any topic using Ollama LLM.
- Verify generated tweets for quality, relevance, and correctness.
- RESTful API built with FastAPI for easy integration.
- Modular, maintainable Python codebase.
- Uses LangChain framework to orchestrate LLM interaction.
- Environment configuration via .env file.

### Technologies Used
- Python 3.12
- FastAPI for building the API server
- Uvicorn as ASGI server
- LangChain with the langchain_classic and langchain_ollama packages
- Ollama LLM for local large language model inference
- Pydantic for schema and request validation
- Python-dotenv for environment variable management
