import os

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Get contents of a file in a the specified directory relative to the working directory, providing the contents of the file",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "File path to get the contents of the file from, relative to the working directory (default is the working directory itself)",
                },
            },
            "required": ["file_path"],
        },
    },
}


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_path = target_file == working_dir_abs or target_file.startswith(
            working_dir_abs + os.sep
        )

        if not valid_target_path:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        MAX_CHARS = 10_000

        with open(target_file, "r", encoding="utf-8") as f:
            file_content_string = f.read(MAX_CHARS + 1)
            if len(file_content_string) > MAX_CHARS:
                file_content_string = (
                    file_content_string[:MAX_CHARS]
                    + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return file_content_string
    except Exception as e:
        return f"Error: {e}"
