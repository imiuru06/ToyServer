# server.py
from flask import Flask, request, Response, jsonify
from src.file_merger import FileMerger
from src.file_generator import ProjectCreator

import json

app = Flask(__name__)

file_merger = FileMerger()
file_merger.load_config()

@app.route('/merge_files', methods=['POST'])
def merge():
    data = request.json
    source_folder = data.get('source_folder')
    output_file = data.get('output_file')
    
    if not source_folder or not output_file:
        return Response(
            "Source folder and output file are required.", 
            status=400
        )
    
    if file_merger.is_running:
        return Response(
            "Merge is already in progress.", 
            status=400
        )
    
    result = file_merger.merge_files(source_folder, output_file)
    return Response(
        json.dumps(result),
        mimetype='application/json'
    )

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
        project_creator.create_project_structure()
        
        return jsonify({"status": "success", "message": "Project structure and files created successfully."})
    
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    
if __name__ == "__main__":
    app.run(debug=True)