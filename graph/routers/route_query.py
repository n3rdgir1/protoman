"Generic route query class for user questions."
from typing import Literal
from pydantic import BaseModel, Field

ROUTER_FORMAT = """Respond with JSON data that includes the datasource key and the appropriate value of "continue", "greet", or "decline"."""


class RouteQuery(BaseModel):
    """Route the user question to the appropriate node."""

    datasource: Literal["continue", "decline", "greet"] = Field(
        default=...,
        description="Given a user question choose to continue to the next step, end the conversation, or generate a generic response."
    )
