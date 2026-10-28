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
