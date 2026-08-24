import os

schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Writes content inside the the file, if file/path does not exist creates file/path inside working directory. Returns a success message at file path with length of text.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Target files path inside the working directory",
                },
                "content": {
                    "type": "string",
                    "description": "The text to write inside inside the given file paths.",
                },
            },
        "required": ["file_path", "content"],
        },
    },
}


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        working_dir_abs = os.path.abspath(f'{working_directory}')
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        parent_dirs = os.makedirs(os.path.dirname(target_dir),exist_ok=True)
        if not valid_target_dir:
            return(f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory')
        if os.path.isdir(target_dir):
            return(f'Error: Cannot write to "{file_path}" as it is a directory')

        with open(target_dir, "w") as f:
            file_write = f.write(content)
        return(f'Successfully wrote to "{file_path}" ({len(content)} characters written)')

    except Exception as e:
        return f"Error: {e}"
