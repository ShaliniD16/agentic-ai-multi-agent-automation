# Agentic AI, Multi-Agent Systems & MCP Automation

A hands-on learning repository covering **Agentic AI, LLMs, Multi-Agent Systems, Model Context Protocol (MCP), and Microsoft AutoGen**.

This repository contains the concepts, experiments, and practical workflows I explored while learning how AI agents can interact with tools, external systems, and other agents to perform real-world tasks.

---

## Overview

Traditional LLM applications primarily focus on generating responses based on user prompts.

Agentic AI extends this approach by allowing AI systems to:

* Reason about tasks
* Use external tools
* Interact with applications and systems
* Maintain state
* Collaborate with other specialized agents
* Automate multi-step workflows
* Incorporate human input when required

The core idea explored throughout this repository is:

```text
LLM + Tools + MCP + Context + Agents + State + Workflow
```

---

## Topics Covered

### 1. Introduction to Agentic AI

* What is Agentic AI?
* LLMs vs AI Agents
* Capabilities and limitations of LLMs
* Single-agent systems
* Limitations of single-agent approaches
* Multi-agent systems
* Benefits of specialized multi-agent workflows

---

### 2. Python Asynchronous Programming

AutoGen is asynchronous in nature, so the learning journey also covered Python's `asyncio` programming model.

Example:

```python
import asyncio

async def main():
    print("I am inside function")

asyncio.run(main())
```

---

### 3. AutoGen Framework

The repository contains practical examples using AutoGen components such as:

* `AssistantAgent`
* `UserProxyAgent`
* `RoundRobinGroupChat`
* `SelectorGroupChat`
* `MaxMessageTermination`
* `TextMentionTermination`
* `McpWorkbench`
* Agent state saving and restoration
* Human-in-the-loop workflows

---

## AssistantAgent

Explored how to create an `AssistantAgent` using an LLM model client.

The examples include using **Gemini through AutoGen's OpenAI-compatible model client**.

The basic flow is:

```text
User Task
    ↓
AssistantAgent
    ↓
Model Client
    ↓
Gemini LLM
    ↓
Response
```

---

## Multimodal Agents

Explored how an agent can process multimodal inputs such as images.

Using `MultiModalMessage` and AutoGen's image support, the agent can receive both:

* Text instructions
* Images

and use the vision capabilities of the underlying model to analyze the image.

---

## Multi-Agent Workflows

### RoundRobinGroupChat

Explored `RoundRobinGroupChat` for coordinating multiple agents.

Agents participate in a predefined order.

Example:

```text
Researcher
    ↓
Writer
    ↓
Reviewer
    ↓
Researcher
    ↓
...
```

This approach is useful when each agent has a clearly defined responsibility.

---

### SelectorGroupChat

Explored `SelectorGroupChat` for dynamically selecting which agent should act next.

Instead of always following a fixed order, the team uses a model to determine which agent is most appropriate for the next step.

Example:

```text
                SelectorGroupChat
                       ↓
              "Who should act?"
                       ↓
                    LLM
                       ↓
              Select appropriate agent
```

The workflow included:

```text
Researcher → Writer → Critic
```

where each agent had a specialized role.

---

## Termination Conditions

Explored termination mechanisms to control when a multi-agent workflow should stop.

### MaxMessageTermination

Stops a team after a specified number of messages.

```python
MaxMessageTermination(max_messages=6)
```

### TextMentionTermination

Stops execution when an agent produces a specified text.

Example:

```python
TextMentionTermination("TERMINATE")
```

Termination conditions help prevent unnecessary execution and control model/API usage.

---

## Human-in-the-Loop

Explored the `UserProxyAgent` for incorporating human interaction into an AI workflow.

The human can:

* Provide additional information
* Correct an agent
* Approve a result
* Continue the conversation
* Decide when a task is complete

Example workflow:

```text
User
 ↓
UserProxyAgent
 ↓
AssistantAgent
 ↓
User feedback
 ↓
AssistantAgent
 ↓
Completion
```

---

## State Saving and Restoration

Explored how agent state can be saved and restored to preserve information across workflow execution.

Without state:

```text
Agent 1
   ↓
Information
   ↓
Program ends
   ↓
Agent 2 does not know the previous information
```

With state:

```text
Agent 1
   ↓
Save State
   ↓
Persist State
   ↓
Load State
   ↓
Agent 2
   ↓
Continue with previous information
```

This is useful for long-running workflows, recovery scenarios, and maintaining conversational context.

---

# Model Context Protocol (MCP)

## What is MCP?

**Model Context Protocol (MCP)** provides a standardized way for AI applications to connect with external tools and systems.

Instead of building custom integrations for every tool, an MCP server can expose capabilities that an AI agent can use.

Conceptually:

```text
AssistantAgent
      ↓
    LLM
      ↓
MCP Workbench
      ↓
  MCP Server
      ↓
External Tool/System
```

---

## MCP Workbench

Explored AutoGen's `McpWorkbench` for connecting agents with MCP servers.

The repository includes examples involving:

* Filesystem operations
* Jira
* Playwright/browser automation
* MySQL
* REST APIs
* Excel

---

# Browser Automation with MCP

Explored browser automation using **Playwright MCP** and AutoGen.

The browser automation agent can:

* Navigate webpages
* Inspect webpages
* Click elements
* Enter data
* Verify results
* Capture screenshots
* Report test execution results

The workflow combines LLM reasoning with browser automation tools.

```text
User Task
    ↓
Automation Agent
    ↓
Gemini
    ↓
Playwright MCP
    ↓
Browser
    ↓
Test Result
```

---

# Jira + Browser Automation Multi-Agent Workflow

One of the major practical workflows explored in this repository combines **Jira MCP** with **Playwright MCP**.

## Workflow

```text
User Task
     ↓
BugAnalyst
     ↓
Jira MCP
     ↓
Analyze Recent Bugs
     ↓
Create Smoke-Test Plan
     ↓
AutomationAgent
     ↓
Playwright MCP
     ↓
Execute Smoke Test
     ↓
PASS / FAIL Report
```

### BugAnalyst

The Jira agent is responsible for:

* Searching the Jira project for recent bugs
* Identifying bugs relevant to the application
* Understanding expected and actual behavior
* Designing a stable smoke-test flow
* Passing the smoke-test steps to the automation agent

### AutomationAgent

The browser automation agent is responsible for:

* Receiving the approved smoke-test flow
* Executing the test using Playwright MCP
* Inspecting the page before interacting with elements
* Using stable locators
* Verifying important actions
* Reporting PASS/FAIL results
* Identifying known defects encountered during execution

This workflow demonstrates how specialized agents can collaborate instead of requiring one agent to handle the entire process.

---

# Agent Factory Pattern

Another major concept explored was the **Agent Factory Pattern**.

An `AgentFactory` centralizes the creation and configuration of agents.

Instead of creating and configuring every agent directly inside the workflow, the factory manages:

* Agent creation
* Model configuration
* MCP workbench assignment
* System instructions
* Tool isolation

Example:

```text
                  AgentFactory
                       │
          ┌────────────┼────────────┐
          ↓            ↓            ↓
   DatabaseAgent   APIAgent    ExcelAgent
          │            │            │
        MySQL       REST API      Excel
         MCP           MCP          MCP
```

The important principle is **separation of responsibilities**.

For example:

* DatabaseAgent → Database tools
* APIAgent → REST API and filesystem tools
* ExcelAgent → Excel tools

An agent receives only the tools required for its responsibility.

---

# Database → API → Excel Workflow

A complete multi-agent workflow was developed around sequential user registration and validation.

## Workflow

```text
User Task
    ↓
DatabaseAgent
    ↓
Retrieve Registration Data
    ↓
APIAgent
    ↓
Registration API
    ↓
Login API
    ↓
ExcelAgent
    ↓
Save Successful Registration Details
```

### DatabaseAgent

Responsible for:

1. Connecting to the MySQL database
2. Retrieving registration information
3. Combining information from multiple tables
4. Ensuring the email is unique
5. Passing structured registration data to the next agent

---

### APIAgent

Responsible for:

1. Receiving registration data from DatabaseAgent
2. Reading the API contract
3. Constructing the registration request
4. Calling the registration API
5. Calling the login API
6. Validating the login response
7. Reporting the actual success/failure status

---

### ExcelAgent

Responsible for:

1. Waiting for API testing to complete
2. Checking the actual login result
3. Saving data only after successful login
4. Recording registration information
5. Adding a timestamp
6. Saving and verifying the Excel data

---

# Project Structure

The repository contains the learning examples and framework components developed during the course.

```text
AgenticAIAutoGen/
│
├── .gitignore
│
├── basic1.py
├── basic2.py
├── basic3.py
├── basic4.py
├── basic5.py
├── basic6.py
│
├── main.py
├── scenario1.py
├── SelectorGroupChat.py
├── web_surfer.py
│
├── framework/
│   ├── agentFactory.py
│   └── mcp_config.py
│
├── algebra_solution.txt
│
└── README.md
```

> Local virtual environments, API keys, credentials, generated files, and other sensitive or machine-specific files should not be committed to the repository.

---

# Technologies & Tools

The learning journey involved:

* Python
* AutoGen
* Gemini
* Large Language Models (LLMs)
* Model Context Protocol (MCP)
* MCP Workbench
* Playwright MCP
* Jira MCP
* MySQL MCP
* REST API MCP
* Excel MCP
* AsyncIO
* Multi-Agent Systems
* Human-in-the-Loop
* Context Engineering

---

# Key Learning

The biggest takeaway from this journey was that **Agentic AI is not simply about using an LLM**.

A useful agentic system requires multiple components working together:

```text
             ┌─────────────┐
             │     LLM     │
             └──────┬──────┘
                    │
             ┌──────▼──────┐
             │    Agent    │
             └──────┬──────┘
                    │
       ┌────────────┼────────────┐
       ↓            ↓            ↓
     Tools         MCP         Context
       │            │            │
       └────────────┼────────────┘
                    ↓
                  State
                    ↓
                Workflow
                    ↓
             Real-world Task
```

The practical workflows helped demonstrate how specialized AI agents can collaborate with external tools and systems to automate multi-step processes.

---

## Acknowledgement

This repository was created as part of my hands-on learning journey in **Agentic AI, MCP, AutoGen, and multi-agent automation**, with practical guidance and structured learning from **Rahul Shetty**.

The hands-on approach helped me connect theoretical concepts with practical automation and testing scenarios.

---

## Disclaimer

This repository contains learning exercises, experiments, and course-based implementations created for educational purposes. Some examples may require external services, API keys, local applications, databases, or MCP servers to run.
