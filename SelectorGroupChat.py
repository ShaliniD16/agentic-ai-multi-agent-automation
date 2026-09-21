import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import MaxMessageTermination, TextMentionTermination
from autogen_agentchat.teams import SelectorGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["GEMINI_API_KEY"] = "API key"
async def main():
    model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",
                                              model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                   family="unknown", structured_output=True))
    researcher = AssistantAgent(name="Researcher", model_client=model_client, system_message="You are a researcher. Your role is to gather information and provide research findings ONLY. "
                       "Do not write articles or create content - just provide research data and facts.")
    writer = AssistantAgent(name="Writer", model_client=model_client, system_message="You are a writer. Your role is to take research information and "
                       "create well-written articles. Wait for research to be provided, then write the content.")
    critic = AssistantAgent(name="Critic", model_client=model_client,system_message="You are a critic. Review written content and provide feedback."
                       " Say 'TERMINATE' when satisfied with the final result.")

    termination = MaxMessageTermination(max_messages=15) | TextMentionTermination("TERMINATE")
    team = SelectorGroupChat(participants=[critic, writer, researcher], termination_condition=termination,model_client=model_client, allow_repeated_speaker=True)
    await Console(team.run_stream(task="Research renewable energy trends and write a brief article about the future of solar power"))


asyncio.run(main())