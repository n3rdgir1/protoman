"Nodes for initializing the project init"

import os

PROTOMAN_DIR = '.protoman'

def init(root_path):
    """Initialize the project with a .protoman directory"""
    print("Looks like you have not initialized the project yet. Creating the .protoman directory.")
    if not os.path.exists(os.path.join(root_path, '.git')):
        print("Looks like you have not initialized the project with git. Initializing git.")
        os.system(f'cd {root_path} && git init')
        print('<git init>')
    protoman_dir = os.path.join(root_path, PROTOMAN_DIR)
    if not os.path.exists(protoman_dir):
        print("Looks like you have not initialized the project with protoman. Initializing protoman.")
        os.makedirs(protoman_dir)
        print('<makedirs> {root_path}/' + PROTOMAN_DIR)
        print('<listdir> {root_path}')
        output = os.listdir(root_path)
        print(output)
    os.system(f'cd {root_path} && echo ".protoman" > .gitignore')
    os.system(f'cd {root_path} && git add .gitignore')
    os.system(f'cd {root_path} && git commit -m "PROTOMAN: Initialize protoman"')

def should_init(base_dir: str) -> bool:
    """Check if the project should be initialized"""
    protoman = not os.path.exists(os.path.join(base_dir, PROTOMAN_DIR))
    git = not os.path.exists(os.path.join(base_dir, '.git'))
    return protoman or git
