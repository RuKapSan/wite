import os
import yaml

# Директории, которые исключаются из анализа
EXCLUDE_DIRS = {
    "node_modules",
    "__pycache__",
    "venv",
    ".venv",
    "build",
    "dist",
    ".git",
}

# Функция для проверки нужного расширения файлов
def is_valid_file(filename: str) -> bool:
    valid_extensions = (".js", ".json", ".md", ".html", ".css")
    invalid_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".svg")
    if filename.endswith(invalid_extensions):
        return False
    return filename.endswith(valid_extensions)

def walk_project(root_dir: str):
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for f in filenames:
            if is_valid_file(f):
                files.append(os.path.join(dirpath, f))
    return files

def main():
    root_dir = "."
    output_file = "project_files.yaml"
    files = walk_project(root_dir)
    data = {"files": {}}
    for file_path in files:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        data["files"][file_path] = {"content": content}
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False)
    print(f"Результат анализа сохранён в {output_file}")

if __name__ == "__main__":
    main()
