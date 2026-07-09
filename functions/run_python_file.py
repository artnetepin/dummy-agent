import subprocess
import os
from typing import Any

schema_run_python_file: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Executes a specified Python file relative to the working directory, optionally with command-line arguments, and returns its output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the Python file to execute, relative to the working directory",
                },
                "args": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Optional list of command-line arguments to pass to the Python script",
                },
            },
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.join(work_dir_abs_path, file_path)
        target_file = os.path.normpath(file_abs_path)

        if not (os.path.commonpath([work_dir_abs_path, target_file]) == work_dir_abs_path):
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not target_file.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file] + (args if args else [])
        result = subprocess.run(
            command, cwd=work_dir_abs_path, capture_output=True, text=True, timeout=30)

        output_string = ''

        if result.returncode != 0:
            output_string += f'Process exited with code {result.returncode}\n'

        if len(result.stdout) == 0 and len(result.stderr) == 0:
            output_string += 'No output produced.\n'

        output_string += f'STDOUT: {result.stdout}\nSTDERR: {result.stderr}'

        return output_string

    except Exception as e:
        return f'Error: {str(e)}'
