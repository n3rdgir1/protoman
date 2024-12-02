"create a coding plan"
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from graph.state import State
from util.client import client, deployment_name
from util.extensions import chat, debug
from .constants import PERSONA

class Step(BaseModel):
    """Step in the plan"""
    action: str
    path: str
    content: str
    description: str
    completed: bool = Field(default=False)

class Plan(BaseModel):
    """Plan for building application"""
    steps: list[Step]

def create_plan(state: State):
    """Create a coding plan"""
    formatting = """Return a JSON string in the format of {"steps": [{"action": string, "path": string "content": string}, ...], formulated: "True|False", reason: str}.
    steps: list - A list of steps to take to complete the plan.
    action: string - The action to take such as "ask_pair", "create_file", or the string argument to python's `os.system` call.
    path: string - The path to the file or directory to create or modify.
    content: string - The content necessary to complete the action.
    description: string - A description of the step to tell your pair. It should be concise, 1-2 sentences max."""

    system = f"""{PERSONA}

        In order to have an effective pairing session, you must first create a plan for your coding tasks.
        You have alredy gathered questions and have received answers from your pair in your conversation.
        Think step by step with your conversation history and your notes to determine all steps needed to complete your task, do not worry if there are a large number of tasks.
        You will have access to perform actions that you can complete with a python `os.system` command.
        Formulate your actions as inputs to `os.system` commands.
        In addition, you can ask your pair to perform actions by using the "ask_pair" action. You can utilize this for things like starting servers or checking outputs.
        Just output the JSON in the format specified below, not any of your thoughts or notes.

        Here is the conversation so far:
        {state['chat']}

        Here is your  notes from your data gathering:
        {state['scratchpad']}

        Output your plan in the following format:
        {formatting}
    """
    parser = PydanticOutputParser(pydantic_object=Plan)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": state['ask']}
        ],
    )
    messages = []
    parsed = parser.invoke(response.choices[0].message.content)
    messages.append(debug(f"Plan: {parsed}"))
    messages.append(chat("Here is the plan I have formulated:"))
    for i, step in enumerate(parsed.steps):
        messages.append(chat(f"{i + 1}. {step.description}"))
        messages.append(debug(f"Action: {step.action}"))
        if step.path:
            messages.append(debug(f"Path: {step.path}"))
        if step.content:
            messages.append(debug(f"Content: {step.content}"))
    messages.append(chat("Would you like me to execute this plan?"))
    steps = [
        {
            'action': step.action,
            'path': step.path,
            'content': step.content,
            'description': step.description
        } for step in parsed.steps
    ]
    return {**state, 'plan': steps, 'chat': state['chat'] + messages}
