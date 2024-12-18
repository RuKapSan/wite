# Python Project Analyzer

## Overview
Python Project Analyzer is a tool designed to analyze the structure of Python projects. It traverses directories, identifies Python files, extracts information about modules, classes, functions, and imports, and provides an easy-to-use interface for working with this data.

## Features

1. **File and Directory Analysis**
   - Automatically traverses a given directory and identifies Python files.
   - Validates file extensions to ensure only Python scripts are analyzed.

2. **Code Analysis**
   - Extracts details about:
     - Imports (`import` and `from ... import ...` statements).
     - Class definitions.
     - Function definitions (both regular and asynchronous).
   
3. **Data Filtering**
   - Allows filtering and processing of extracted data for specific use cases.

4. **YAML Support**
   - Can work with YAML for data export or configuration handling.

5. **Type Annotations**
   - Uses Python type hints (`Dict`, `List`, `Any`) to improve code readability and support static analysis.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/RuKapSan/wite.git
   cd wite
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Command Line
Run the analyzer with the following command:
```bash
wite
```
This will analyze the specified directory and output the structure of the project.

### Example
```python
from wite import ProjectAnalyzer, walk_project

# Initialize the analyzer
analyzer = ProjectAnalyzer()

# Walk through a project directory
project_files = walk_project("/path/to/project")

# Analyze each file
for file in project_files:
    analyzer.analyze_file(file)

# Access the extracted data
print(analyzer.extracted_data)
```

## API Reference

### Classes
#### `ProjectAnalyzer`
- **Methods**:
  - `analyze_file(filepath: str)`: Analyzes a single Python file.
  - `visit_Import(node)`: Processes `import` statements.
  - `visit_ImportFrom(node)`: Processes `from ... import ...` statements.
  - `visit_ClassDef(node)`: Processes class definitions.
  - `visit_FunctionDef(node)`: Processes function definitions.
  - `visit_AsyncFunctionDef(node)`: Processes asynchronous function definitions.

### Functions
#### `is_python_file(filename: str) -> bool`
Determines if a given file is a Python script.

#### `walk_project(root_dir: str) -> List[str]`
Traverses a directory and returns a list of Python files.

#### `filter_data(data: Any) -> Any`
Filters the extracted data based on specific criteria.

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Submit a pull request describing your changes.

## License
This project is licensed under the MIT License. See the `NOPE` file for details.

## Contact
For questions or feedback, please open an issue in the repository or reach out to the maintainer at [mokan.956@gmail.com].

