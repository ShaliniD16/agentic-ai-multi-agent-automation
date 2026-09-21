import asyncio
import os

from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["GEMINI_API_KEY"] = "API key"
async def main():
    model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",
                                              model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                   family="unknown", structured_output=True))
    web_surfer_agent = MultimodalWebSurfer(name="WebSurfer",model_client=model_client, headless=False, animate_actions=True)
    team = RoundRobinGroupChat(participants=[web_surfer_agent], max_turns=3)
    await Console(team.run_stream(task="Navigate to Google and search for 'AutoGen framework Python'. Then summarize what "
                                 "you find."))
    await web_surfer_agent.close()
    await model_client.close()


asyncio.run(main())