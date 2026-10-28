import os
import sys

sys.path.append("..")
from config import MAX_CHARS


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )
        valid_dir = os.path.isdir(target_dir)

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not valid_dir:
            return f'Error: "{directory}" is not a directory'

        lines: list[str] = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            lines.append(
                f"- {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={os.path.isdir(item_path)}"
            )
        return "\n".join(lines)
    except Exception as e:
        return f"Error: {e}"


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        valid_file = os.path.isfile(target_file)
        if not valid_file:
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, "r") as f:
            file_content_str = f.read(MAX_CHARS)
            if len(file_content_str) >= MAX_CHARS:
                file_content_str += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )
            return file_content_str
    except Exception as e:
        return f"Error: {e}"
