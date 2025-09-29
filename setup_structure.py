import os

# Define the folder structure
structure = {
    "angelsuccess-cybersecurity": {
        "files": [
            "app.py",
            "requirements.txt",
            "runtime.txt",
            "Procfile",
            "railway.json",
            ".env.example",
            "DEPLOYMENT_GUIDE.md",
            "test_deployment.py",
            "DEPLOYMENT_CHECKLIST.md",
            ".gitignore",
        ],
        "folders": {
            "templates": {
                "files": [
                    "index.html",
                    "auth.html",
                    "dashboard.html",
                    "network_monitor.html",
                    "ai_analysis.html",
                    "threat_intelligence.html",
                    "optimization_center.html",
                    "system_settings.html",
                ]
            }
        }
    }
}

def create_structure(base_path, structure_dict):
    for folder, content in structure_dict.items():
        folder_path = os.path.join(base_path, folder)
        os.makedirs(folder_path, exist_ok=True)

        # Create files in the folder
        for file in content.get("files", []):
            file_path = os.path.join(folder_path, file)
            if not os.path.exists(file_path):
                with open(file_path, "w") as f:
                    f.write("")  # Empty file
                print(f"✅ Created file: {file_path}")

        # Recursively create subfolders
        if "folders" in content:
            create_structure(folder_path, content["folders"])

if __name__ == "__main__":
    base_dir = "."  # current directory
    create_structure(base_dir, structure)
    print("\n🚀 Project structure created successfully!")
