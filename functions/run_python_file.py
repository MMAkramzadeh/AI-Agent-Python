import os
import subprocess


schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Run a python file (ending in .py) in a specified directory relative to the working directory, providing both STDOUT & STDERR with Exit-code",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "python file (ending in .py) to run the file, path is relative to the working directory (default is the working directory itself)",
                },
                "args": {
                    "type": "array",
                    "description": "the arguments for running the python file who are items and strings",
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
        working_directory_abs = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(working_directory_abs, file_path))
        valid_target_file = (
            os.path.commonpath([working_directory_abs, target_file])
            == working_directory_abs
        )

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if target_file[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file]
        if args is not None:
            command.extend(args)

        completed_run = subprocess.run(
            args=command,
            capture_output=True,
            text=True,
            timeout=30,
            cwd=working_directory_abs,
            check=False,
        )
        output_str = ""
        if completed_run.returncode != 0:
            output_str += f"Process exited with code {completed_run.returncode}\n"
        if not completed_run.stdout and not completed_run.stderr:
            output_str += "No output produced\n"
        else:
            output_str += (
                f"STDOUT: {completed_run.stdout}STDERR: {completed_run.stderr}"
            )
        return output_str
    except Exception as e:
        return f"Error: executing Python file: {e}"
