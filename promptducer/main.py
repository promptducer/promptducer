import configargparse
import json

from promptducer.prompter import Prompter
from promptducer.query_api import QueryAPI
from promptducer.source_reader import FileUtility


# PATHS = json.loads(FileUtility.read_file("paths.json"))


def main():
    parser = configargparse.ArgumentParser(default_config_files=['../settings.conf'])

    parser.add_argument('-c', '--config_file', is_config_file=True, help='Config file path')

    # SourceReader
    parser.add_argument('-s', '--source_code_base_dir', required=True,
                        help="Base directory of the inputs (will be recursively searched)")
    parser.add_argument('-e', '--file_extension', nargs="+")

    # Prompt-
    parser.add_argument('-p', '--prompt_name', required=True, help="Name of the prompt class")
    parser.add_argument('--prompt_file', required=True, help="Path of the prompt file (which contains a class)")

    # QueryAPI
    parser.add_argument('--api_path', required=True,
                        help="Path of the QueryAPI subclass that is used to communicate with the LLM")
    parser.add_argument('-n', '--api_name', required=True, help="Name of the Query API class")

    parser.add_argument('-r', '--results_base_dir', required=True)
    parser.add_argument('--use_api_class_names', action="store_true")

    # Responder
    parser.add_argument('-i', '--responder_name')
    parser.add_argument('--responder_file')
    parser.add_argument('--use_responder_class_names', action="store_true")
    parser.add_argument('--force_stop_response',
                        type=int,
                        help="Stops the conversation after the Nth api response, even if the responder's stop"
                             "condition is not yet met. First response is number 1, please provide odd numbers.")
    parser.add_argument('--force_stop_token',
                        type=int,
                        help="Stops the conversation after N tokens, , even if the responder's stop"
                             "condition is not yet met.")

    parser.parse_args()

    prompter = Prompter(parser)

    query = QueryAPI.create(parser, prompter)

    query.run_queries()


if __name__ == '__main__':
    main()
