import os
from typing import NoReturn
from django.core.files import File
from shared.random_string import random_string


def prepend_random_string_to_filename(
        filename: str,) -> str:
    random_file_name = f"{random_string(20)}_{filename}"
    return random_file_name


def save_uploaded_file(
        absolute_path: str,
        file: File,) -> None|NoReturn:
    # Just due to what I read, assertive programming is for things
    # that we think never ever happen
    assert os.path.isabs(absolute_path),\
        "The passed path is not absolute path!"

    with open(absolute_path, 'wb+') as destination_file:
        """
        Looping over UploadedFile.chunks() instead of using read()
        ensures that large files don’t overwhelm your system’s memory.
        """
        [destination_file.write(chunk) for chunk in file.chunks()]

