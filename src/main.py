import sys
import yaml
from langchain_setup import setup_langchain

def run_project_creation(yaml_content):
    tool_chain = setup_langchain()
    result = tool_chain(yaml_content)
    print(result)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <yaml_file>")
        sys.exit(1)

    yaml_file_path = sys.argv[1]

    with open(yaml_file_path, 'r', encoding='utf-8') as yaml_file:
        yaml_content = yaml_file.read()

    run_project_creation(yaml_content)