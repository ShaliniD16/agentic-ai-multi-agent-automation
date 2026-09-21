import asyncio
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
    agent1 = AssistantAgent(name="MoralScienceTeacher", model_client=model_client, system_message="You are a Moral Science teacher. Explain concepts shortly and ask follow-up questions.")
    agent2 = AssistantAgent(name="Student", model_client=model_client, system_message="You are a curious stuent. Ask questions and show your thinking process")
    team = RoundRobinGroupChat(participants=[agent1, agent2], termination_condition=MaxMessageTermination(max_messages=6))
    await Console(team.run_stream(task="Let's discuss about being kind. Keep the conversations short"))
    await model_client.close()
asyncio.run(main())