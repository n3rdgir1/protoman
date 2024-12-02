"Route user question regarding coding asks"
from typing import Literal
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

from util.client import client, deployment_name
from graph.state import State

ROUTER_FORMAT = """Respond with JSON data that includes the approval key and the appropriate value of "accept", or "decline"."""


class RouteApproval(BaseModel):
    """Route the user approval to the appropriate node."""

    approval: Literal["accept", "decline"] = Field(
        default=...,
        description="Given the user's response to approving the plan, determine if they accepted or declined the plan."
    )

def is_approved(state: State):
    """Determine if the user has approved or declined the plan."""

    system = f"""You are a knowledgable sofware engineer who is acting as a pair programmer with the user.
        You have come up with a plan for your coding tasks and presented this plan to your pair.
        Based on your pair's response, decide if your pair has accepted your plan.
        If the user has accepted your plan, you will next continue with the coding task.
        If the user has declined your plan, you will have the opportunity to create a new plan.

        {ROUTER_FORMAT}"""

    parser = PydanticOutputParser(pydantic_object=RouteApproval)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": state['chat'][-1]['text']},
        ],
    )

    try:
        return parser.invoke(response.choices[0].message.content)
    except Exception:
        print(response)
        return RouteApproval(datasource="decline")
