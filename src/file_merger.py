# src/file_merger.py

import os
import json
import yaml

class FileMerger:
    def __init__(self):
        self.extension_list = ['.py', '.json', '.env']  # Default extensions to merge
        self.structure_extensions = ['.json', '.env']  # Extensions for structure info only
        self.output_file = ""
        self.source_folder = ""
        self.is_running = False

    def load_config(self):
        config_file = "config/config.json"
        if os.path.exists(config_file):
            with open(config_file, 'r', encoding='utf-8') as config:
                config_data = json.load(config)
                self.extension_list = config_data.get("extensions", self.extension_list)
                self.structure_extensions = config_data.get("structure_extensions", self.structure_extensions)
        else:
            self.save_config()

    def save_config(self):
        config_data = {
            "extensions": self.extension_list,
            "structure_extensions": self.structure_extensions
        }
        with open("config/config.json", 'w', encoding='utf-8') as config:
            json.dump(config_data, config, ensure_ascii=False, indent=4)

    def merge_files(self, source_folder, output_file):
        self.source_folder = source_folder
        self.output_file = output_file
        self.is_running = True
        try:
            project_data = {"project_name": "test_project", "folders": []}
            
            for root, dirs, files in os.walk(self.source_folder):
                folder_data = {"name": os.path.relpath(root, self.source_folder), "files": []}
                for filename in files:
                    if any(filename.endswith(ext) for ext in self.extension_list):
                        file_path = os.path.join(root, filename)
                        relative_path = os.path.relpath(file_path, self.source_folder)
                        if filename.endswith('.json'):
                            # For JSON files, include structure (keys) and content
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                structure_info = json.load(infile)
                                folder_data["files"].append({
                                    "name": filename,
                                    "content": f"'''구조정보 {relative_path}'''\n내부 구조(키)\n" + "\n".join(structure_info.keys()) + "\n\n" + json.dumps(structure_info, indent=4)
                                })
                        elif filename.endswith('.env'):
                            # For .env files, include only structure (keys)
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                env_content = infile.read()
                                env_keys = [line.split('=')[0] for line in env_content.splitlines() if '=' in line]
                                folder_data["files"].append({
                                    "name": filename,
                                    "content": f"'''구조정보 {relative_path}'''\n내부 구조(키)\n" + "\n".join(env_keys)
                                })
                        else:
                            # For other files (e.g., .py), include file content
                            with open(file_path, 'r', encoding='utf-8') as infile:
                                folder_data["files"].append({
                                    "name": filename,
                                    "content": f"'''{relative_path}'''\n" + infile.read()
                                })
                
                if folder_data["files"]:
                    project_data["folders"].append(folder_data)
            
            with open(self.output_file, 'w', encoding='utf-8') as outfile:
                yaml.dump(project_data, outfile, allow_unicode=True, sort_keys=False)
                
            return {"status": "success", "message": "Merge completed successfully."}
        except Exception as e:
            return {"status": "error", "message": str(e)}
        finally:
            self.is_running = False