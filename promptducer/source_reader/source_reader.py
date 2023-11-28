import os
from argparse import ArgumentParser
from datetime import datetime


class SourceReader:
    """
    Reads files from a specific directory.
    A SourceReader reads the given files.

    Parameters
    ----------
    arguments : ArgumentParser
        An ArgumentParser which provides directory paths and other settings.

    Attributes
    ----------
    base_dir : str
        The base directory that contains the source files

    file_utility : FileUtility
        A file reader object.
    """

    def __init__(self, arguments: ArgumentParser):
        args = arguments.parse_args()

        self.base_dir = os.path.normpath(args.source_code_base_dir)
        self.file_utility = FileUtility(self.base_dir, args.file_extension)

    def read_next_source(self) -> tuple[str, str] | None:
        """
        Reads the next file in the base_dir and returns its content.
        If there are no more files to read, None is returned.

        Returns
        -------
        file_content : str, None
            The content of the next file, or None if there are no more files to read.
        """

        try:
            return self.file_utility.read_next()
        except StopIteration:
            return None


class FileUtility:
    """
    A helper class that does file operations.

    Parameters
    ----------
    base_dir: str
        The base directory that contains the source files

    file_extension : {str, list[str], None}, default=None
        A str or list[str] of file extensions that will be listed, all other files will be ignored.
        e.g. "java", ["java", "py"]

    Attributes
    ----------
    file_iterator : iterator
        Used for iterating through the source files.
    """

    start_time = datetime.now()

    def __init__(self, base_dir: str, file_extension: str | list[str] | None = None):
        self.base_dir = base_dir
        self.file_extension = file_extension
        self.file_iterator = None
        self.file_count = 0
        self.reset_iterator()

    def list_files(self) -> list[str]:
        """
        Lists all files in the base directory.
        If a file_extension (str or list) is provided, files with matching extensions will be listed only.

        Returns
        -------
        file_list : list[str]
            A list of files below the base_dir.
        """

        # Finding the source files
        file_list = [os.path.join(root, file) for (root, subdir, files) in os.walk(self.base_dir) for file in files]

        # Filtering files by extension
        if self.file_extension:
            return [file for file in file_list if file.split(".")[-1] in self.file_extension]
        else:
            return file_list

    @staticmethod
    def read_file(file_path: str) -> str:
        """Reads a given file and returns its content"""

        # if isinstance(file_path, list):
        #      print("TYPE", file_path)
        #      print(repr(file_path))
        #      exit(0)
        file_path = os.path.abspath(file_path)

        with open(file_path, 'r', encoding="utf-8") as file:
            return file.read()

    @staticmethod
    def write_file(file_path: str, content: str, append_datetime: bool = True) -> tuple[str, int]:
        """
        Writes content into the given file, creates the file if it does not exist.
        By default, the method appends the value of the static start_time (datetime obj)
        at the end of the filename for versioning purposes.
        If append_datetime is False, but there is a file name conflict, datetime will be appended.
        Value of start_time is the datetime of the creation of the class.
        Datetime format: filename_YYmmdd_HHDD.ext
        """
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        if append_datetime or os.path.exists(file_path):
            filename, extension = os.path.splitext(file_path)
            file_path = filename + "_" + FileUtility.start_time.strftime("%y%m%d_%H%M") + extension

        if os.path.exists(file_path):
            raise FileExistsError(f"""
                File name conflict after versioning! 
                File: {file_path}
                Please check files or wait a minute before running the script again!""")

        with open(file_path, 'w', encoding="utf-8") as file:
            return file_path, file.write(content)

    @staticmethod
    def append_file(file_path: str, content: str, append_datetime: bool = True) -> tuple[str, int]:
        """
        Appends content into the given file, creates the file if it does not exist.
        By default, the method appends the value of the static start_time (datetime obj)
        at the end of the filename for versioning purposes.
        If append_datetime is False, but there is a file name conflict, datetime will be appended.
        Value of start_time is the datetime of the creation of the class.
        Datetime format: filename_YYmmdd_HHDD.ext
        """
        if append_datetime or os.path.exists(file_path):
            filename, extension = os.path.splitext(file_path)
            file_path = filename + "_" + FileUtility.start_time.strftime("%y%m%d_%H%M") + extension

        with open(file_path, 'a') as file:
            return file_path, file.write(content + "\n")

    def read_next(self) -> tuple[str, str]:
        """Returns the filename and the content of the next file in the source files"""
        next_available_file = self.file_iterator.__next__()
        return next_available_file, self.read_file(next_available_file)

    def reset_iterator(self):
        """Counts the files and resets the iterator, so it points to the first file in the source files"""
        file_list = self.list_files()
        self.file_iterator = iter(file_list)
        self.file_count = len(file_list)


