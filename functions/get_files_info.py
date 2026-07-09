import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        work_dir_abs_path = os.path.abspath(working_directory)
        dir_abs_path = os.path.join(work_dir_abs_path, directory)
        target_dir = os.path.normpath(dir_abs_path)

        if not (os.path.commonpath([work_dir_abs_path, target_dir]) == work_dir_abs_path):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

        files = os.listdir(target_dir)
        result = ""

        for file in files:
            file_name = os.path.basename(file)
            file_size = os.path.getsize(os.path.join(target_dir, file))
            is_dir = os.path.isdir(os.path.join(target_dir, file))
            result += f"- {file_name}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return result

    except Exception as e:
        return f'Error: {str(e)}'
