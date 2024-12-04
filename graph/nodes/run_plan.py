"Run the plan with available tools"
import os

from graph.state import State
from util.extensions import chat


def run_plan(state: State):
    """Run the plan"""
    steps = state['plan']
    basedir = state['base_dir']
    messages = []
    for step in steps:
        if step.get('completed', False):
            continue
        messages.append(chat(f"{step['description']}"))
        if step['action'] == 'os.system':
            messages.append(chat(f"Running: `{step['content']}`"))
            os.system(f"cd {basedir} && {step['content']}")
            step['completed'] = True
        elif step['action'] == 'create_file':
            with open(f"{basedir}/{step['path']}", 'w', encoding='utf-8') as file:
                file.write(step['content'])
            messages.append(chat(f"Creating {step['path']}"))
            step['completed'] = True
        elif step['action'] == 'ask_pair':
            messages.append(chat(f"Please run: `{step['content']}`"))
            step['completed'] = True
        else:
            messages.append(chat(f"Unknown action: {step['action']}"))

        if step['completed'] and step['action'] != 'ask_pair':
            os.system(f"cd {basedir} && git add .")
            os.system(f"cd {basedir} && git commit -m 'PROTOMAN: {step['description']}'")

    messages.append(chat("Done."))

    return {**state, 'ask': None, 'stage': None, 'plan': [], 'scratchpad': None,
            'chat': messages}
