import os
import shutil

def path_exists(path):
    """
    Check if a certain path exists, converting Windows-style paths to WSL paths if necessary.

    :param path: Path to check.
    :return: True if path exists, False otherwise.
    """
    # Convert Windows-style paths to WSL paths
    if path[1:3] == ':\\' or path[1:2] == ':':
        drive = path[0].lower()
        rest_of_path = path[2:].replace('\\', '/')
        path = f"/mnt/{drive}{rest_of_path}"

    absolute_path = os.path.abspath(path)
    return os.path.exists(absolute_path)


def get_abs_path(path):
    """
    Get the absolute path of a given path, converting Windows-style paths to WSL paths if necessary.

    :param path: Path to convert.
    :return: Absolute path.
    """
    # Convert Windows-style paths to WSL paths
    if path[1:3] == ':\\' or path[1:2] == ':':
        drive = path[0].lower()
        rest_of_path = path[2:].replace('\\', '/')
        path = f"/mnt/{drive}{rest_of_path}"

    return os.path.abspath(path)

def copytree_with_skip(src, dst):
    """
    Copy files from src to dst, skipping files that already exist in the destination.

    :param src: Source directory path.
    :param dst: Destination directory path.
    """
    if not os.path.exists(dst):
        os.makedirs(dst)

    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)
        
        if os.path.isdir(src_item):
            copytree_with_skip(src_item, dst_item)
        else:
            if not os.path.exists(dst_item):
                shutil.copy2(src_item, dst_item)
            else:
                print(f"Skipping existing file: {dst_item}")