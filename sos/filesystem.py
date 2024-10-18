"""
This module contains functions for interacting with the filesystem.
"""


def write_file(file: str, content: str) -> None:
    """
    Write the content to the file.

    :param file: the file to write to
    :param content: the content to write
    :return: None
    """
    with open(file, "w", encoding="utf-8") as f:
        f.write(content)
