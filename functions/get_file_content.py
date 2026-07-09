import os
from typing import Any

from config import MAX_CHARS


schema_get_file_content: dict[str, Any] = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Reads the content of a specified file relative to the working directory, returning its content as a string",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read, relative to the working directory",
                },
            },
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:

    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        file_abs_path = os.path.join(work_dir_abs_path, file_path)
        target_file = os.path.normpath(file_abs_path)

        if not (os.path.commonpath([work_dir_abs_path, target_file]) == work_dir_abs_path):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as file:
            content = file.read(MAX_CHARS)

            if file.read(1):
                content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except Exception as e:
        return f'Error: {str(e)}'
