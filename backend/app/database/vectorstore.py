import os
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CHROMA_PATH = "chroma_db"

def get_embeddings():
    api_key = os.getenv("LLM_API_KEY")
    
    model = os.getenv("MODE")
    if model == "gemini":
        text_encoder = os.getenv("ENCODER_MODEL")
        return GoogleGenerativeAIEmbeddings(model=text_encoder, google_api_key=api_key)
    else:
        return OpenAIEmbeddings(openai_api_key=api_key)

def get_vectorstore():
    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=CHROMA_PATH,
        embedding_function=embeddings
    )
    return vectorstore
