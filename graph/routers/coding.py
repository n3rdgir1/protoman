"Route user question regarding coding asks"
from langchain_core.output_parsers import PydanticOutputParser

from util.client import client, deployment_name
from graph.state import State
from graph.routers.route_start import RouteStart, ROUTER_FORMAT


def is_coding(state: State):
    """Route the user question to the appropriate node."""

    system = f"""You are a knowledgable sofware engineer who is acting as a pair programmer with the user.
        You can create files, write code, and execute code.
        You can also ask your pair questions to help you figure out your plan.
        If your pair states that they need to do some coding task, go ahead and do this for them.\n
        Given your pair's request, decide whether to continue with a coding task, politely close the topic, or generate a generic response.
        If this is a task that can be completed by writing or executing code, continue.
        When the user is greeting you, greet.
        When the user is asking about a topic that is definitely not coding related, decline.
        {ROUTER_FORMAT}"""

    parser = PydanticOutputParser(pydantic_object=RouteStart)

    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": state.get('ask', state.get('user_input', ''))},
        ],
    )

    try:
        return parser.invoke(response.choices[0].message.content)
    except Exception:
        print(response)
        return RouteStart(datasource="decline")
