import asyncio
import os

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient

os.environ["GEMINI_API_KEY"] = "API key"

async def main():
    model_client = OpenAIChatCompletionClient(model="gemini-3.6-flash",
                                              model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                   family="unknown", structured_output=True))
    assistant = AssistantAgent(name="MathTutor",model_client=model_client,system_message="You are a Mathematics Tutor who listens to student's queries and answers them with clarity and conciseness. When the student replies like thank you, done or something similar, print 'LESSON COMPLETE' and end the session")
    user_proxy = UserProxyAgent(name="Student")
    team = RoundRobinGroupChat(participants=[assistant,user_proxy],termination_condition=TextMentionTermination("LESSON COMPLETE"))
    await Console(team.run_stream(task="Can you solve this algebraic expression? 3*4+9=?"))


asyncio.run(main())