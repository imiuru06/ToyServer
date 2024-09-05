import os
import yaml
import json

class ProjectCreator:
    def __init__(self, yaml_content):
        self.data = yaml.safe_load(yaml_content)
        self.project_name = self.data['project_name']

    def create_project_structure(self):
        if not os.path.exists(self.project_name):
            os.makedirs(self.project_name)
        self._create_files(self.data['folders'], self.project_name)

    def _create_files(self, folders, base_path):
        for folder in folders:
            folder_path = os.path.join(base_path, folder['name'])
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            for file in folder.get('files', []):
                file_path = os.path.join(folder_path, file['name'])
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(file['content'])
            if 'subfolders' in folder:
                self._create_files(folder['subfolders'], folder_path)