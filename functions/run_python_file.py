import os, subprocess

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute python file relative to the working directory with optional argument to subprocess and return the function call output",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to run file, relative to working directory",
                },
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "Optional argument to get optional result based on argument command",
                },
            },
            "required": ["file_path"],
        },
    },
}


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        valid_file = os.path.isfile(target_file)
        if not valid_file:
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not target_file.endswith("py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)
        running_output = subprocess.run(
            command, text=True, timeout=30, capture_output=True
        )

        output_string = []
        if running_output.returncode != 0:
            output_string.append(
                f"Process exited with code {running_output.returncode}"
            )
        if len(running_output.stdout) == 0 and len(running_output.stderr) == 0:
            output_string.append("No output produced")
        if running_output.stdout:
            output_string.append(f"STDOUT:\n{running_output.stdout}")
        if running_output.stderr:
            output_string.append(f"STDERR:\n{running_output.stderr}")

        return "\n".join(output_string)
    except Exception as e:
        return f"Error: executing Python file: {e}"
