import abc
import importlib
import importlib.util
import json
import os
import sys
from argparse import ArgumentParser

from promptducer import helpers

from promptducer.source_reader.source_reader import SourceReader

# Change this if you want to customize the default separator
NAME_SEPARATOR = "__"


class PromptTemplate(abc.ABC):
    """
    Interface for concrete prompt modules

    Operations
    ----------
    create_prompt
        An abstract method for creating a prompt
    """

    @abc.abstractmethod
    def create_prompt(self, src, metadata=None) -> str:
        raise NotImplementedError("Subclasses must implement create_prompt.")


class Prompter:
    """
    The responsible class for creating actual prompts for LLMs based on templates and the vulnerable source code.

    Parameters
    ----------
    arguments : ArgumentParser
        An ArgumentParser which provides directory paths and other settings.

    Attributes
    ----------
    prompt_template : PromptTemplate
        An actual PromptTemplate for prompt creations

    source_reader : SourceReader
        Source reader.

    """

    def __init__(self, arguments: ArgumentParser):
        self.args = arguments.parse_args()
        self.prompt_template = None

        # module = importlib.import_module("promptducer.prompter." + self.args.prompt_name)
        #
        # dynamic_class = getattr(module, self.args.prompt_name)

        # TODO: Remove this
        # print(self.args.prompt_name, self.args.prompt_file)
        # spec = importlib.util.spec_from_file_location(self.args.prompt_name, self.args.prompt_file)
        # module = importlib.util.module_from_spec(spec)
        # # sys.modules[self.args.prompt_name] = module
        # spec.loader.exec_module(module)
        # dynamic_class = getattr(module, self.args.prompt_name)

        self.source_reader = SourceReader(arguments)
        self.prompt_template = helpers.import_module(self.args.prompt_file, self.args.prompt_name)()
        self.output_folder = self.args.results_base_dir

    def get_prompt(self):
        """
        Creates a string from the concrete one, and saves it, so it can be viewed by anyone.
        :return: created prompt file path
        """

        file_info = self.source_reader.read_next_source()

        if file_info is None:
            return None
        file_path, file_content = file_info
        last_subdirectory = self.get_last_subdirectory(file_path)
        filename = f"{last_subdirectory}_{os.path.basename(file_path)}.prompt"

        # Fetch metadata
        metadata = self.fetch_metadata(file_path)

        # Get timestamped output directory
        actual_dir = os.path.join(self.output_folder,
                                  self.source_reader.file_utility.start_time.strftime("%Y_%m_%d %H_%M_%S"))

        if not os.path.exists(actual_dir):
            os.makedirs(actual_dir)

        if self.output_folder == self.args.results_base_dir:
            self.output_folder = actual_dir

        path = os.path.join(actual_dir, filename)
        print(path)
        # Pass the source and metadata to the create_prompt
        path, _ = self.source_reader.file_utility.write_file(path, self.prompt_template.create_prompt(file_content, metadata))

        return path


    def get_last_subdirectory(self, path):
        # Remove trailing slashes if any
        path = path.rstrip(os.path.sep)

        # Split the path into its components
        components = path.split(os.path.sep)

        # Return the last non-empty component (i.e., the last subdirectory)
        return components[-2] if components[-2] else components[-3]

    def fetch_metadata(self, file):
        """
        Method to fetch the metadata of the corresponding file
        Parameters
        ----------
        file : str
            Path to the source file

        Returns
        -------
            An object that contains the metadata collected from the corresponding JSON

        """
        # Get the base filename without extension
        # But only remove the part after the last dot
        base_filename = ".".join(os.path.basename(file).split('.')[:-1])  # dot in filename
        # base_filename = os.path.basename(file).split('.')[0]

        # Check whether it's a method file or not. If so, we'll check if there isn't a matching JSON file
        if (base_filename.split(NAME_SEPARATOR)[0] != base_filename and
                not os.path.exists(os.path.join(os.path.dirname(file), f"{base_filename}.json"))):
            # No separate JSON file for us, so we must use the class'
            base_filename = base_filename.split(NAME_SEPARATOR)[0]

        # Read the JSON file
        metadata = self.source_reader.file_utility.read_file(os.path.join(os.path.dirname(file), f"{base_filename}.json"))

        return json.loads(metadata)
