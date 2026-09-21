import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import MultiModalMessage
from autogen_agentchat.ui import Console
from autogen_core import Image
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["GEMINI_API_KEY"] = "API key"

async def main():

    model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",
                                              model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                   family="unknown", structured_output=True))
    assistant = AssistantAgent(name="MultiModalAssistant",model_client=model_client)
    image = Image.from_file("D:\\Agentic AI\\shinchan.jpg")
    multimodal_message = MultiModalMessage(
        content=["What do you see in this image", image],
        source="user"
    )
    await Console(assistant.run_stream(task=multimodal_message))
    await model_client.close()

asyncio.run(main())