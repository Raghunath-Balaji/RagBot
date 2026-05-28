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
        if apikey.startswith("AIza"):
            self.provider = "gemini"
            from langchain_google_genai import ChatGoogleGenerativeAI
            self.llm = ChatGoogleGenerativeAI(
                model = "gemini-2.5-flash",
                google_api_key = apikey,
                streaming = True
            )
        else:
            self.provider = "openai"
            from langchain_openai import ChatOpenAI
            self.llm = ChatOpenAI(
                model = "gpt-3.5-turbo",
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
