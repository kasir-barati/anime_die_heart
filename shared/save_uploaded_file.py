from django.core.files import File
from .random_string import random_string

def save_uploaded_file(file: File):
    """
    'r'   open for reading (default)
    'w'   open for writing, truncating the file first
    'x'   create a new file and open it for writing
    'a'   open for writing, appending to the end of the file if it exists
    'b'   binary mode
    't'   text mode (default)
    '+'   open a disk file for updating (reading and writing)
    'U'   universal newline mode (deprecated)
    """
    random_file_name = f"{random_string(20)}_{file.name}"
    with open(random_file_name, 'wb+') as destination_file:
        """
        Looping over UploadedFile.chunks() instead of using read()
        ensures that large files don’t overwhelm your system’s memory.
        """
        [destination_file.write(chunk) for chunk in file.chunks()]