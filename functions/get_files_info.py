import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        working_dir_abs = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))

        valid_target_dir = (
            os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'

    except Exception as e:
        return f"Error: {e}"

    items_of_dir = os.listdir(target_dir)
    list_items_str = []
    try:
        for item in items_of_dir:
            item_path = target_dir + "/" + item
            list_items_str.append(
                f"  - {item}: file_size={os.path.getsize(item_path)} bytes, is_dir={
                    os.path.isdir(item_path)
                }"
            )
    except Exception as e:
        return f"Error: {e}"

    results = "\n".join(list_items_str)
    if directory == ".":
        return f"Result for current directory:\n{results}"
    else:
        return f"Result for '{directory}' directory:\n{results}"
