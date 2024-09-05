import yaml
import json

def yaml_to_json(yaml_file, json_file):
    with open(yaml_file, 'r', encoding='utf-8') as yf:
        yaml_content = yaml.safe_load(yf)
    
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(yaml_content, jf, indent=4)

if __name__ == "__main__":
    yaml_to_json('config.yaml', 'config.json')