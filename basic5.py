import asyncio
import json
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["GEMINI_API_KEY"] = "API key"
async def main():
    model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",
                                              model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                   family="unknown", structured_output=True))
    agent1 = AssistantAgent(name="agent1", model_client=model_client)
    agent2 = AssistantAgent(name="agent2", model_client=model_client)

    await Console(agent1.run_stream(task="My favourite color is Pink"))
    state = await agent1.save_state()
    with open("memory.json", "w") as f:
        json.dump(state, f)
    with open("memory.json", "r") as f:
        saved_state = json.load(f)
    await agent2.load_state(state=saved_state)
    await Console(agent2.run_stream(task="What is my favourite color"))
    await model_client.close()
asyncio.run(main())