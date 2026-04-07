import json
import os


def load_products():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir)

    file_path = os.path.join(project_root, "data", "products.json")

    print("Loading from:", file_path)  # debug

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)