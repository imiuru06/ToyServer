import requests
import json
import os

def load_config(file_path):
    """ Read the JSON config file. """
    with open(file_path, 'r') as file:
        return json.load(file)

def download_file(url, dest_folder):
    """ Download a file from a URL to a specified folder. """
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)

    response = requests.get(url, stream=True)
    file_name = url.split('/')[-1]
    file_path = os.path.join(dest_folder, file_name)

    with open(file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)

    return file_path

def create_project(config):
    url = config['create_files']['url']
    data = config['create_files']['data']
    
    # Prompt user for YAML file path or use default content
    file_path = data.get('file_path', '').strip()
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            yaml_content = file.read()
        data = {'yaml_content': yaml_content}
    else:
        yaml_content = data.get('yaml_content', 'default YAML content here')
        data = {'yaml_content': yaml_content}
    
    response = requests.post(url, json=data)
    response_data = response.json()

    if response_data['status'] == 'success':
        file_url = response_data.get('file_url')
        if file_url:
            print(f"Project successfully created. Download the ZIP file from: {file_url}")
            # Download the ZIP file
            zip_file_path = download_file(file_url, './downloads')
            print(f"Downloaded ZIP file to: {zip_file_path}")
        else:
            print("File URL not found in response.")
    else:
        print(f"Create Project failed: {response_data['message']}")
    
    return response_data

def merge_files(config):
    url = config['merge_files']['url']
    data = config['merge_files']['data']
    
    # Prompt user for source folder path
    source_folder = input("Enter the source folder path: ").strip()
    if not source_folder:
        raise ValueError("Source folder path is required.")
    data['source_folder'] = source_folder
    
    response = requests.post(url, json=data)
    response_data = response.json()

    if response_data['status'] == 'success':
        file_url = response_data.get('file_url')
        if file_url:
            print(f"Files successfully merged. Download the YAML file from: {file_url}")
            # Download the YAML file
            yaml_file_path = download_file(file_url, './downloads')
            print(f"Downloaded YAML file to: {yaml_file_path}")
        else:
            print("File URL not found in response.")
    else:
        print(f"Merge failed: {response_data['message']}")
    
    return response_data

def main():
    config = load_config('config_client.json')
    
    print("Select a test to run:")
    print("1. Test Create Project API")
    print("2. Test File Merger API")
    print("Type 'exit' to quit.")
    
    while True:
        choice = input("Enter the number of the test to run: ")
        if choice == 'exit':
            break
        elif choice == '1':
            response_data = create_project(config)
            print("Create Project API Response:", response_data)
        elif choice == '2':
            response_data = merge_files(config)
            print("File Merger API Response:", response_data)
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()