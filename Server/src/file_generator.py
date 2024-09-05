import os
import shutil
import yaml
import json

class ProjectCreator:
    def __init__(self, yaml_content):
        self.data = yaml.safe_load(yaml_content)
        self.project_name = self.data.get('project_name', 'default_project')
        self.project_path = os.path.join(os.getcwd(), self.project_name)

    def create_project_structure(self):
        # Create project directory if it doesn't exist
        if not os.path.exists(self.project_path):
            os.makedirs(self.project_path)
        
        # Create files and folders
        self._create_files(self.data.get('folders', []), self.project_path)
        
        # Compress the project folder and return the path
        zip_file_path = self._compress_project()
        return zip_file_path

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

    def _compress_project(self):
        zip_file_name = f"{self.project_name}.zip"
        zip_file_path = os.path.join(os.getcwd(), zip_file_name)
        
        # Create a zip archive of the project folder
        shutil.make_archive(zip_file_path.replace('.zip', ''), 'zip', self.project_path)
        
        # Clean up the unzipped folder
        shutil.rmtree(self.project_path)
        
        return zip_file_path