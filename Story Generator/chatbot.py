import os
import time
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.vectorstores import FAISS
from langchain_classic.schema import Document

def load_files():
    files = []
    directory = "./data/raw"
    for filename in os.listdir(directory):
        if filename.endswith(".txt"):
            path = os.path.join(directory, filename)
            with open(path, 'r', encoding='utf-8') as f:
                text = f.read()
            files.append(Document(page_content=text, metadata={"source": filename}))
    return files



def split_files(files):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    split_files = []
    for file in files:
        chunks = text_splitter.split_text(file.page_content)
        for chunk in chunks:
            split_files.append(chunk)

    return split_files

def create_vector_store(chunks, embedding_model):
    vector_store = FAISS.from_texts(texts=chunks, embedding=embedding_model)
    return vector_store

def create_rag_chain(llm):
    prompt = PromptTemplate(
        input_variables = ["content", "question"],
        template="""
            ## 📜 Your Role: The Lore Master

            You are a specialized AI assistant acting as a "Lore Master." Your entire knowledge base consists *only* of the story excerpts provided to you. Your purpose is to help a user understand this story by answering their questions based *exclusively* on the text given.

            You are not a general AI; you are an expert on *this* specific text and nothing else.

            ## 🎯 Your Primary Task

            You will be given **[Story Excerpts]** and a **[User's Question]**. Your mission is to carefully analyze the excerpts and provide a clear, accurate, and direct answer to the question.

            ## 📖 Strict Rules of Engagement

            1.  **Strictly Grounded:** Your answer **must** be 100% based on the information within the **[Story Excerpts]**. Do not infer, guess, or use any outside knowledge.
            2.  **No Hallucination:** Do not invent details, character motivations, or plot points that are not explicitly mentioned in the provided text.
            3.  **Handling Missing Information (Critical):** If the answer to the question is not present in the **[Story Excerpts]**, you **must** state this clearly.
                * **Do not** say: "I don't know."
                * **Do** say: "Based on the provided story excerpts, there is no information about [topic of the question]."
            4.  **Quoting:** You may use brief, relevant quotes from the text to support your answer, but the answer should primarily be in your own words.
            5.  **Tone:** Your tone should be helpful, knowledgeable, and slightly formal, like a dedicated guide or scholar of this specific narrative.

            ---

            ## 📚 Provided Information

            **[Story Excerpts]:**
            {context}

            ---

            ## ❓ User's Question

            {question}

            ---

            ## 💡 Your Answer (Based *only* on the excerpts above):
        """
    )
    return prompt | llm | StrOutputParser()
    

def chat_loop():
    files = load_files()
    chunks = split_files(files)
    print("Files Loaded")

    # llm = ChatOllama(model="phi3:14b")
    llm = ChatOllama(model="mistral:7b")
    embeddings = OllamaEmbeddings(model="nomic-embed-text")

    vector_store = create_vector_store(chunks, embeddings)
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    rag_chain = create_rag_chain(llm)

    while True:
        query = input("\nYour question: ")
        if query.lower() in ["exit", "quit", "q"]:
            print("Exiting chat. Goodbye!")
            break

        relevant_docs = retriever.invoke(query)
        
        # Prepare context string by joining
        context = "\n".join([doc.page_content for doc in relevant_docs])
        
        answer = rag_chain.invoke({
            "context": context,
            "question": query
        })
        print("\nAnswer:")
        print(answer)   



chat_loop()