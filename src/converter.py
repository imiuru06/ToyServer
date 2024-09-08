import json
import yaml

def json_to_markdown(json_data):
    md_content = "# API Documentation\n\n"
    
    # Overview section
    info = json_data.get("info", {})
    md_content += "## Overview\n\n"
    md_content += f"{info.get('description', 'No description available.')}\n\n"
    
    # Process items
    items = json_data.get("item", [])
    for item in items:
        md_content += f"## {item.get('name', 'Endpoint')}\n\n"
        for sub_item in item.get("item", []):
            md_content += f"### {sub_item.get('name', 'Sub-Endpoint')}\n\n"
            
            # Request details
            request = sub_item.get("request", {})
            method = request.get("method", "GET")
            
            # Handle URL which might be a string or an object
            url = request.get("url", {})
            if isinstance(url, str):
                url_raw = url
            else:
                url_raw = url.get("raw", "No URL available")
                
            description = request.get("description", "No description available.")
            md_content += f"- **Method:** {method}\n"
            md_content += f"- **URL:** [{url_raw}]({url_raw})\n"
            md_content += f"- **Description:** {description}\n\n"
            
            # Request body
            body = request.get("body", {})
            if body:
                mode = body.get("mode", "No mode available")
                raw_content = body.get("raw", "No raw content available")
                md_content += f"- **Body Mode:** {mode}\n"
                md_content += f"- **Body Content:** \n\n```json\n{raw_content}\n```\n\n"
            
            # Response details
            responses = sub_item.get("response", [])
            for response in responses:
                md_content += f"#### {response.get('name', 'Response')}\n\n"
                status_code = response.get('code', 'No code available')
                status = response.get('status', 'No status available')
                md_content += f"- **Status Code:** {status_code} {status}\n"
                
                headers = response.get('header', [])
                if headers:
                    md_content += "##### Headers\n\n"
                    md_content += "| Header | Value |\n"
                    md_content += "| --- | --- |\n"
                    for header in headers:
                        key = header.get("key", "No key")
                        value = header.get("value", "No value")
                        md_content += f"| {key} | {value} |\n"
                    md_content += "\n"
                
                # Response body
                response_body = response.get("body", "No response body available")
                md_content += f"- **Response Body:** \n\n```json\n{response_body}\n```\n\n"
    
    return md_content

def yaml_to_json(yaml_file, json_file):
    with open(yaml_file, 'r', encoding='utf-8') as yf:
        yaml_content = yaml.safe_load(yf)
    
    with open(json_file, 'w', encoding='utf-8') as jf:
        json.dump(yaml_content, jf, indent=4)
        
if __name__ == "__main__":
    # Load JSON data
    with open('C:\\Users\\noah\\Documents\\ToyServer.postman_collection.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)

    # Convert JSON to Markdown
    markdown_content = json_to_markdown(json_data)

    # Save Markdown content to file
    with open('api_documentation.md', 'w', encoding='utf-8') as file:
        file.write(markdown_content)