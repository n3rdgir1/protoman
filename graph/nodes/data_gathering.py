"Gather information to create a plan"
from typing import List, Optional
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

from graph.state import State
from util.client import client, deployment_name
from .constants import PERSONA
from util.extensions import chat, debug

class Questions(BaseModel):
    """Questions to ask the user"""
    questions: List[str]
    notes: Optional[str] = None

def data_gathering(state: State):
    """Gather data for the plan"""
    formatting = """{"questions": ["question1", "question2", ...], "notes": "notes"}"""
    system = f"""{PERSONA}

        In order to have an effective pairing session, you must first create a plan for your coding tasks.
        Think step by step to determine all steps needed to complete your task, do not worry if there are a large number of tasks.

        Based on the information you have, please generate a list of questions that you need to ask your pair to complete the plan.
        You should only output the questions, not any of your thoughts or answers.
        If you have all the information necessary for your plan, return an empy list.

        Here is the conversation so far:
        {state['chat']}

        Here is your scratchpad:
        {state['scratchpad']}

        Output your questions and any of your notes that might be useful after receiving your answers in the following format:
        {formatting}
    """

    parser = PydanticOutputParser(pydantic_object=Questions)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": state['ask']}
        ],
    )

    parsed = parser.invoke(response.choices[0].message.content)
    messages = debug(state['chat'], f"Response: {parsed}")
    if parsed.questions:
        stage = 'data_gathering'
        messages = chat(messages, "I have some questions for you:")
        for question in parsed.questions:
            messages = chat(messages, question)
    else:
        stage = 'create_plan'
        messages = chat(messages,
                        "I have the information I need, moving on to formulating the plan.")
    return {**state,
            'chat': messages,
            'scratchpad': parsed.notes,
            'stage': stage,
    }