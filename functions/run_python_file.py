import os
import subprocess
from sys import stdout


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Runs specified files at the working directory only, with the option to extend arguments",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Target files path inside the working directory",
                },
                "args": {
                    "type": "array",
                    "description": "optional list of string arguments to extend the command to run python files. ",
                    "items": {
                        "type":"string"
                    },
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

        working_dir_abs = os.path.abspath(f'{working_directory}') # returns full path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path)) #returns dir path for the file
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs #bool
        if not valid_target_dir:
            return(f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_dir):
            return(f'Error: "{file_path}" does not exist or is not a regular file')
        if not file_path.endswith('.py'):
            return(f'Error: "{file_path}" is not a Python file')
        command = ["python", target_dir]
        if args:
            command.extend(args)

        result = subprocess.run(command, capture_output=True, text=True, cwd=working_dir_abs,timeout=30 )

        output = []

        if result.returncode != 0:
            output.append(f"Process exited with code {result.returncode}")
        if not result.stdout and not result.stderr:
            output.append("No output produced")
        if result.stdout:
            output.append(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            output.append(f"STDERR:\n{result.stderr}")

        return "\n".join(output)
    except Exception as e:
        return f"Error: executing Python file: {e}"
