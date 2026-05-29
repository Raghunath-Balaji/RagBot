import os
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class LLMService:
    def __init__(self):
        api_key=os.getenv("LLM_API_KEY")
        if not api_key:
            raise ValueError("No API key found")
        self.provider_config(api_key)


    def provider_config(self, apikey):
        llm_mode = os.getenv("MODE")
        if llm_mode.lower() == "gemini":
            self.provider = llm_mode
            from langchain_google_genai import ChatGoogleGenerativeAI
            model_name = os.getenv("LLM_MODEL")
            self.llm = ChatGoogleGenerativeAI(
                model = model_name,
                google_api_key = apikey,
                streaming = True
            )
        else:
            self.provider = llm_mode
            from langchain_openai import ChatOpenAI
            model_name = os.getenv("LLM_MODEL")
            self.llm = ChatOpenAI(
                model = model_name,
                openai_api_key = apikey,
                streaming  = True
            )

        print (f"LOG : LLM service used is {self.provider}")



    def get_provider(self):
        return self.provider

    async def get_streaming_response(self, message: str, history: list = None):
        messages = [
            SystemMessage(content="You are a helpful assistant.")
        ]
        
        messages.append(HumanMessage(content=message))
        
        async for chunk in self.llm.astream(messages):
            yield chunk.content
