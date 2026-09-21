import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["GEMINI_API_KEY"] = "API key"

async def main():
    print("I am inside function")
    #model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",api_key=os.environ["GEMINI_API_KEY"],base_url="https://generativelanguage.googleapis.com/v1beta/openai/",model_info=ModelInfo(vision=True, function_calling=True, json_output=True, family="unknown", structured_output=True))
    model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",
                                              model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                   family="unknown", structured_output=True))
    assistant = AssistantAgent(name="assistant",model_client=model_client)
    await Console(assistant.run_stream(task="What is 25 * 8?"))
    await model_client.close()

asyncio.run(main())