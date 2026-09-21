import asyncio
import os

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.models import ModelInfo
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.tools.mcp import StdioServerParams, McpWorkbench

os.environ["GEMINI_API_KEY"] = "API key"

async def main():
  model_client = OpenAIChatCompletionClient(model="gemini-3.1-pro-preview",
                                            model_info=ModelInfo(vision=True, function_calling=True, json_output=True,
                                                                 family="unknown", structured_output=True))
  jira_server_params = StdioServerParams(command= "uvx",
      args= ["mcp-atlassian"],
      env= {

        "JIRA_URL": "url",
        "JIRA_USERNAME": "username",
        "JIRA_API_TOKEN": "jira token",
        "JIRA_PROJECTS_FILTER":"KAN"
      },
                                         read_timeout_seconds=60)
  jira_workbench = McpWorkbench(jira_server_params)
  playwright_server_params = StdioServerParams(command="npx",
                                               args=[
                                                 "@playwright/mcp@latest"
                                               ],
                                               read_timeout_seconds=60
                                               )
  playwright_workbench = McpWorkbench(playwright_server_params)
  async with jira_workbench as jira_wb, playwright_workbench as playwright_wb:
    bug_analyst = AssistantAgent(name="BugAnalyst", model_client=model_client,
                                 workbench=jira_wb,
                                 system_message=("""
                    1. Search Jira project KAN for the 5 most recently created Bugs.
2. Identify bugs related to the application:
   https://rahulshettyacademy.com/seleniumPractise/#/
3. Summarize the relevant bugs and their expected behavior.
4. Design ONE stable smoke-test flow covering the core shopping journey.
5. Keep the smoke test independent of known defective functionality where possible.
6. Pass the final smoke-test steps to AutomationAgent.
When your analysis is complete, provide exactly one final section:

SMOKE TEST HANDOFF
URL: <exact URL>
Steps:
1. ...
2. ...
3. ...
Expected results:
1. ...
2. ...
3. ...

Then stop and wait for AutomationAgent.
                    """))

    automation_analyst = AssistantAgent(name="AutomationAgent", model_client=model_client,
                                        workbench=playwright_wb,
                                        system_message=(
                                          """
                                          1. Use the exact real URL provided by BugAnalyst.
2. Execute the approved smoke-test flow using Playwright MCP.
3. Use stable locators based on accessible names, labels, roles, or visible text.
4.Before interacting with an element, inspect the current page and use
the locator information exposed by Playwright MCP.

Prefer:
- role + accessible name
- label
- visible text
- stable attributes

Do not guess selectors.
5. After each important action, verify the expected result.
6. Capture screenshots only at important checkpoints.
7. Report PASS/FAIL for every step.
8. If a known Jira bug is encountered, report it as a defect rather than stopping the entire workflow.
9. Do not perform additional exploratory actions unless required to complete the flow.
10. Return a concise execution report.
When execution and reporting are finished, you MUST end your response with exactly:

TESTING COMPLETE
                                          """
                                          ))
    team = RoundRobinGroupChat(participants=[bug_analyst, automation_analyst],
                               termination_condition=TextMentionTermination('TESTING COMPLETE'))

    await Console(team.run_stream(task="""BugAnalyst:
Start the workflow.

1. Search Jira project KAN for the 5 most recently created Bugs.
2. Identify which bugs are relevant to the application:
   https://rahulshettyacademy.com/seleniumPractise/#/
3. Summarize the relevant bugs.
4. Design ONE stable smoke-test flow for the core shopping journey.
5. Avoid known defective functionality where possible.
6. Provide the final smoke-test handoff to AutomationAgent.

AutomationAgent:
After BugAnalyst provides the smoke-test handoff:
1. Execute exactly that flow using Playwright MCP.
2. Use the exact URL provided.
3. Verify every important action.
4. Report PASS/FAIL for every step.
5. If a known Jira defect is encountered, record it as a defect.
"""))
asyncio.run(main())