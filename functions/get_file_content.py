import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Shows the contents of a file with the limit of max 10000 characters. ",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Target files path inside the working directory",
                },
            },
        },
        "required": ["file_path"],
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    MAX_CHARS = 10000

    try:
        working_dir_abs = os.path.abspath(f'{working_directory}')
        target_dir = os.path.normpath(os.path.join(working_dir_abs, file_path))
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        if not valid_target_dir:
            return(f'Error: Cannot read "{file_path}" as it is outside the permitted working directory')
        if not os.path.isfile(target_dir):
            return(f'Error: File not found or is not a regular file: "{file_path}"')

        with open(target_dir, "r") as f:
            file_content_string = f.read(MAX_CHARS)
            if f.read(1):
                file_content_string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
            return file_content_string

    except Exception as e:
        return f"Error: {e}"
