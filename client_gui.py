import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
import requests
import json
import webbrowser
import os

class ClientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Client GUI")
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.config = self.load_config(os.path.join(self.base_path, "config_client.json"))  # config 파일 로드
        self.create_widgets()
        self.show_create_project_frame()

    def create_widgets(self):
        # Create a menu bar
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # Add menu items
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="Create Project", command=self.show_create_project_frame)
        self.file_menu.add_command(label="Merge Files", command=self.show_merge_files_frame)

        # Status Text
        self.status_text = scrolledtext.ScrolledText(self.root, height=5, width=80)
        self.status_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Create Project Page
        self.create_project_frame = tk.Frame(self.root)
        self.create_project_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(self.create_project_frame, text="Create Project", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.create_project_frame, text="Browse YAML File", command=self.browse_yaml_file).pack(pady=5, padx=5, side=tk.LEFT)
        
        self.yaml_content_text = scrolledtext.ScrolledText(self.create_project_frame, height=10, width=50)
        self.yaml_content_text.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)
        
        tk.Button(self.create_project_frame, text="Create Project", command=self.create_project).pack(pady=5, padx=5, side=tk.RIGHT)

        # Merge Files Page
        self.merge_files_frame = tk.Frame(self.root)
        self.merge_files_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(self.merge_files_frame, text="Merge Files", font=("Arial", 14)).pack(pady=10)
        
        tk.Button(self.merge_files_frame, text="Browse Source Folder", command=self.browse_source_folder).pack(pady=5, padx=5, side=tk.LEFT)
        
        self.source_folder_entry = tk.Entry(self.merge_files_frame, width=50)
        self.source_folder_entry.pack(pady=5, padx=5, fill=tk.X, expand=True)
        
        tk.Button(self.merge_files_frame, text="Merge Files", command=self.merge_files).pack(pady=5, padx=5, side=tk.RIGHT)

    def load_config(self, file_path):
        """ JSON 파일에서 config를 로드합니다. """
        with open(file_path, 'r') as file:
            return json.load(file)

    def browse_yaml_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("YAML Files", "*.yaml")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                self.yaml_content_text.delete(1.0, tk.END)
                self.yaml_content_text.insert(tk.END, file.read())

    def create_project(self):
        url = self.config['create_files']['url']
        data = self.config['create_files']['data']

        # Read YAML content from text widget
        yaml_content = self.yaml_content_text.get(1.0, tk.END).strip()
        if not yaml_content:
            messagebox.showerror("Error", "YAML content is empty.")
            return
        
        data['yaml_content'] = yaml_content
        
        response = requests.post(url, json=data)
        response_data = response.json()
        
        if response_data.get('status') == 'success':
            file_url = response_data.get('file_url')
            if file_url:
                webbrowser.open(file_url)  # Open the URL in the default web browser
            else:
                self.status_text.insert(tk.END, "File URL not found in response.\n")
        else:
            self.status_text.insert(tk.END, f"Create Project failed: {response_data.get('message')}\n")

    def browse_source_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.source_folder_entry.delete(0, tk.END)
            self.source_folder_entry.insert(0, folder_path)

    def merge_files(self):
        config = self.config['merge_files']
        url = config['url']
        data = config['data']
        data['source_folder'] = self.source_folder_entry.get().strip()
        
        if not data['source_folder']:
            messagebox.showerror("Error", "Source folder is required.")
            return
        
        response = requests.post(url, json=data)
        response_data = response.json()
        
        if response_data['status'] == 'success':
            file_url = response_data.get('file_url')
            if file_url:
                self.status_text.insert(tk.END, f"File successfully merged. Download the file from: {file_url}\n")
                webbrowser.open(file_url)  # Open the URL in the default web browser
            else:
                self.status_text.insert(tk.END, "File URL not found in response.\n")
        else:
            self.status_text.insert(tk.END, f"Merge failed: {response_data['message']}\n")

    def show_create_project_frame(self):
        self.create_project_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.merge_files_frame.pack_forget()

    def show_merge_files_frame(self):
        self.merge_files_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        self.create_project_frame.pack_forget()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClientApp(root)
    root.mainloop()