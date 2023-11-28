import math
import os
from abc import ABC, abstractmethod
from argparse import ArgumentParser

from dotenv import load_dotenv
from tqdm import tqdm

from promptducer import helpers
from promptducer.prompter.prompter import Prompter
from promptducer.query_api.token_counter import TokenCounter
from promptducer.responder.responder import Responder
from promptducer.source_reader.source_reader import FileUtility

SYSTEM_SEPARATOR_TEXT = "\n\n==========\n {0} - SYSTEM:\n==========\n\n"
USER_SEPARATOR_TEXT = "\n\n==========\n {0} - USER:\n==========\n\n"

load_dotenv(verbose=True)


class QueryAPI(ABC):
    """
    An abstract class for query APIs which are responsible for querying an LLM and storing the response.
    The create factory method is used to instantiate the corresponding query API object.

    Attributes
    ----------
    results_base_dir : str
        The path where the query results will be stored.

    api_name : str
        The name of the API that will be instantiated and queried.

    prompter : Prompter
        An object that returns the path to the prompt files.

    query_count : int
        Sum of all prompts to be queried. Used for displaying a progressbar.
    """

    def __init__(self, arguments: ArgumentParser, prompter: Prompter):
        self.args = arguments.parse_args()

        self.results_base_dir = self.args.results_base_dir
        self.api_name = self.args.api_name
        self.prompter = prompter

        # self.api_keys = json.loads(FileUtility.read_file(PATHS.get("api_keys")))
        self.query_count = prompter.source_reader.file_utility.file_count
        self.token_counter = TokenCounter(self.results_base_dir, self.api_name, self.prompter.output_folder)

        self.responder = Responder.create(arguments)
        self.force_stop_response = self.args.force_stop_response
        self.force_stop_token = self.args.force_stop_token

    @classmethod
    def create(cls, arguments: ArgumentParser, prompter: Prompter):
        """
        Factory method which returns the corresponding query API object specified in the ArgumentParser.

        Parameters
        ----------
        arguments : ArgumentParser
            An ArgumentParser which contains the api_name to be used,
            the results_base_dir where the query responses are stored,
            and whether the provided name is a module name or a class name.

        prompter : Prompter
            An object that returns the path to the prompt files.

        Returns
        -------
        An instance of the corresponding query API class.

        Notes
        -----
        By default each specific query API class must be in a separate module in the apis_dir and
        each API must be referenced by its MODULE NAME in the arguments. e.g. "query_chat_gpt".
        API class names can be used instead of module names by providing an argument "--use_api_class_names".
        This way classes do not need to be in separate modules.
        The location of the query API modules must be set in the paths.json file.
        """

        # Parse arguments
        args = arguments.parse_args()
        api_path = args.api_path
        api_name = args.api_name
        api_class = helpers.import_module(api_path, api_name)

        return api_class(arguments, prompter)

    def run_queries(self):
        """
        It queries the API while there are prompts available
        and saves each result in the results base directory.
        """
        prompt_file_path = self.prompter.get_prompt()
        self.token_counter.output_dir = os.path.dirname(prompt_file_path)
        progress = tqdm(total=self.query_count)
        print("\n" + "-" * 10 + "\n")
        while prompt_file_path:
            filename = os.path.basename(prompt_file_path).split(".")[:-1]

            self.token_counter.start_measure()

            conversation = [FileUtility.read_file(prompt_file_path)]

            if self.responder:
                api_response = self.run_query(conversation)
                conversation.append(api_response)
                user_response = self.responder.respond(conversation=conversation)
                counter = 1
                while (
                        not self.responder.stop_reached
                        and (not self.force_stop_response or math.ceil(counter / 2) < self.force_stop_response)
                        and (not self.force_stop_token
                             or (self.token_counter.input_tokens +
                                 self.token_counter.generated_tokens) <= self.force_stop_token)
                ):
                    conversation.append(user_response)
                    api_response = self.run_query(conversation)
                    conversation.append(api_response)
                    user_response = self.responder.respond(conversation)
                    counter += 2

                labelled = [
                    (
                        SYSTEM_SEPARATOR_TEXT.format(idx) if idx % 2 else USER_SEPARATOR_TEXT.format(idx),
                        msg
                    )
                    for idx, msg in enumerate(conversation)
                ]
                conversation = [text for pair in labelled for text in pair]

            else:
                conversation = [self.run_query(conversation)]

            self.token_counter.stop_measure(self.args.prompt_file)

            FileUtility.write_file(
                os.path.join(
                    os.path.dirname(prompt_file_path),
                    f"RES_{self.api_name}_{filename}"
                    f"{('_' + self.responder.responder_name) if self.responder else ''}"
                    f".result"),
                ''.join(conversation)
            )

            progress.update()
            prompt_file_path = self.prompter.get_prompt()

    @abstractmethod
    def run_query(self, conversation: list[str]) -> str:
        """
        Runs one query Expects a string list where even indexes represent the USER messages,
        odd indexes represent the API responses.
        """
        pass
