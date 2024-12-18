import os
import ast
import yaml
from typing import Dict, Any, List

# Список директорий, которые будут полностью исключены из анализа
EXCLUDE_DIRS = {
    "__pycache__",
    "venv",
    ".venv",
    "build",
    "dist",
    ".git",
}

def is_python_file(filename: str) -> bool:
    return filename.endswith(".py") and not filename.startswith("__")

def walk_project(root_dir: str) -> List[str]:
    files = []
    for dirpath, dirnames, filenames in os.walk(root_dir, topdown=True):
        # Исключаем вспомогательные директории
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]

        for f in filenames:
            if is_python_file(f):
                files.append(os.path.join(dirpath, f))
    return files

class ProjectAnalyzer(ast.NodeVisitor):
    def __init__(self):
        self.current_module = None
        self.data = {"modules": {}}

    def analyze_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        try:
            tree = ast.parse(content, filename=filepath)
            self.current_module = filepath
            self.data["modules"][filepath] = {
                "imports": [],
                "classes": {},
                "functions": {},
            }
            self.visit(tree)
        except SyntaxError:
            pass

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            self.data["modules"][self.current_module]["imports"].append(
                {"module": alias.name, "asname": alias.asname}
            )
        self.generic_visit(node)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        for alias in node.names:
            self.data["modules"][self.current_module]["imports"].append(
                {"module": node.module, "name": alias.name, "asname": alias.asname}
            )
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef):
        cls_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "bases": [
                ast.unparse(b)
                for b in node.bases
                if hasattr(b, "id") or hasattr(b, "attr")
            ],
            "methods": {},
        }
        for body_item in node.body:
            if isinstance(body_item, ast.FunctionDef):
                cls_info["methods"][body_item.name] = {
                    "docstring": ast.get_docstring(body_item),
                    "arguments": [arg.arg for arg in body_item.args.args[1:]],
                }
        self.data["modules"][self.current_module]["classes"][node.name] = cls_info
        self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef):
        func_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "arguments": [arg.arg for arg in node.args.args],
        }
        self.data["modules"][self.current_module]["functions"][node.name] = func_info
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef):
        func_info = {
            "name": node.name,
            "docstring": ast.get_docstring(node),
            "arguments": [arg.arg for arg in node.args.args],
        }
        self.data["modules"][self.current_module]["functions"][node.name] = func_info
        self.generic_visit(node)

def filter_data(data: Dict[str, Any]) -> Dict[str, Any]:
    filtered = {"modules": {}}
    for mod_path, mod_data in data["modules"].items():
        # Оставляем только те файлы, где есть классы или функции
        if mod_data["classes"] or mod_data["functions"]:
            filtered["modules"][mod_path] = mod_data
    return filtered

def main():
    root_dir = "."
    output_file = "project_summary.yaml"

    analyzer = ProjectAnalyzer()
    for file_path in walk_project(root_dir):
        analyzer.analyze_file(file_path)

    filtered = filter_data(analyzer.data)
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(filtered, f, allow_unicode=True, sort_keys=False)

    print(f"Результат анализа сохранён в {output_file}")

if __name__ == "__main__":
    main()
