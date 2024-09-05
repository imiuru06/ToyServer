from flask import Flask, request, Response, jsonify, send_from_directory
from src.file_merger import FileMerger
from src.file_generator import ProjectCreator
import yaml
import json
import os
import uuid
import shutil

app = Flask(__name__)

base_path = os.path.dirname(os.path.abspath(__file__))
file_merger = FileMerger()
file_merger.load_config(base_path)

# Define the directories
UPLOAD_FOLDER = 'uploads'
PROJECT_FOLDER = 'projects'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROJECT_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROJECT_FOLDER'] = PROJECT_FOLDER

@app.route('/merge_files', methods=['POST'])
def merge():
    data = request.json
    source_folder = data.get('source_folder')
    output_file_name = f"merged_{uuid.uuid4()}.yaml"
    output_file_path = os.path.join(app.config['UPLOAD_FOLDER'], output_file_name)
    
    if not source_folder:
        return Response(
            "Source folder is required.", 
            status=400
        )
    
    if file_merger.is_running:
        return Response(
            "Merge is already in progress.", 
            status=400
        )
    
    result = file_merger.merge_files(source_folder, output_file_path)
    
    if result['status'] == 'success':
        # Return the URL to download the file
        file_url = request.host_url + 'uploads/' + output_file_name
        return jsonify({"status": "success", "file_url": file_url})
    else:
        return jsonify(result), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/create_files', methods=['POST'])
def create_files():
    try:
        # Read YAML content from the request
        data = request.json
        yaml_content = data.get('yaml_content')

        if not yaml_content:
            return jsonify({"status": "error", "message": "YAML content is required."}), 400

        # Create ProjectCreator instance and run the project creation
        project_creator = ProjectCreator(yaml_content)
        zip_file_path = project_creator.create_project_structure()
        
        # Create a URL for the zip file
        zip_file_url = request.host_url + 'uploads/' + os.path.basename(zip_file_path)
        
        # Move the zip file to the uploads directory
        shutil.move(zip_file_path, os.path.join(app.config['UPLOAD_FOLDER'], os.path.basename(zip_file_path)))

        return jsonify({"status": "success", "file_url": zip_file_url})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
