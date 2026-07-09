import os
from typing import Any

schema_write_file: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content to a specified file relative to the working directory, creating directories as needed",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to write to, relative to the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "Content to write to the file",
                },
            },
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.join(work_dir_abs_path, file_path)
        target_file = os.path.normpath(file_abs_path)

        if not (os.path.commonpath([work_dir_abs_path, target_file]) == work_dir_abs_path):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file), exist_ok=True)

        with open(target_file, 'w') as file:
            file.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f'Error: {str(e)}'
