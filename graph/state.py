"LangGraph state"

from typing import TypedDict, List

class Step(TypedDict):
    """Step in the plan"""
    action: str
    path: str
    content: str
    completed: bool

class Plan(TypedDict):
    """Plan for building application"""
    steps: List[Step]
    formulated: bool

class PlanResponse(TypedDict):
    """Response to the plan"""
    ready: bool
    feedback: str
    tries: int

class State(TypedDict):
    """State of the LangGraph"""
    base_dir: str
    user_input: str
    chat: List[str]

    ask: str
    plan: List[Step]

    git_sha: str

    scratchpad: str
