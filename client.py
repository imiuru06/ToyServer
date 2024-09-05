import requests
import json
import os

def load_config(file_path):
    """ 주어진 경로의 JSON 파일을 읽어 반환합니다. """
    with open(file_path, 'r') as file:
        return json.load(file)

def read_yaml_content_from_file(file_path):
    """ 파일에서 YAML 콘텐츠를 읽어 반환합니다. """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def create_project(config):
    url = config['url']
    data = config['data']
    
    # file_path가 빈 문자열인 경우, yaml_content를 사용
    if data.get('file_path', '').strip():
        yaml_content = read_yaml_content_from_file(data['file_path'])
        data = {'yaml_content': yaml_content}
    else:
        # file_path가 빈 문자열이면 yaml_content 값을 사용
        yaml_content = data.get('yaml_content', 'default YAML content here')
        data = {'yaml_content': yaml_content}
    
    response = requests.post(url, json=data)
    return response.json()

def merge_files(config):
    url = config['url']
    data = config['data']
    response = requests.post(url, json=data)
    return response.json()

def main():
    print("Select a test to run:")
    print("1. Test Create Project API")
    print("2. Test File Merger API")
    choice = input("Enter the number of the test to run: ")

    if choice == '1':
        config = load_config('create_files_config.json')
        response_data = create_project(config)
        print("Create Project API Response:", response_data)
    elif choice == '2':
        config = load_config('merge_files_config.json')
        response_data = merge_files(config)
        print("File Merger API Response:", response_data)
    else:
        print("Invalid choice.")

if __name__ == "__main__":
    main()