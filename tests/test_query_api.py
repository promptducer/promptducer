import sys
from argparse import ArgumentParser
from unittest import TestCase

from promptducer.prompter.prompter import Prompter
from promptducer.query_api.apis.query_gpt35 import QueryGPT35
from promptducer.query_api.apis.query_sed_gpt import QuerySEDGPT
from promptducer.query_api.query_api import QueryAPI

BAD_EXAMPLES = '../tests/source_reader_test_files/bad_examples'


class TestQueryAPI(TestCase):
    def setUp(self) -> None:
        self.parser = ArgumentParser()
        self.parser.add_argument('-n', '--api_name')
        self.parser.add_argument('--api_path')
        self.parser.add_argument('-r', '--results_base_dir', default="")
        self.parser.add_argument('-a', '--apis_dir', default="../evaluator/query_api/apis")
        self.parser.add_argument('-s', '--source_code_base_dir', default=BAD_EXAMPLES)
        self.parser.add_argument('-e', '--file_extension', nargs='+')
        self.parser.add_argument('-p', '--prompt_name')
        self.parser.add_argument('--prompt_file', default="../promptducer/prompter/ConcretePrompt1.py")
        self.parser.add_argument('--use_api_class_names', action="store_true")
        self.parser.add_argument('--responder_name')
        self.parser.add_argument('--responder_path')
        self.parser.add_argument('--force_stop_response', type=int)
        self.parser.add_argument('--force_stop_token', type=int)

        self.prompter = Prompter(self.parser)

    def test_create_correct_object_chat_gpt(self):
        sys.argv.extend(['--api_path', '../promptducer/query_api/apis/query_gpt35.py', '--api_name', 'QueryGPT35'])
        query_chat_gpt = QueryAPI.create(self.parser, self.prompter)
        self.assertIsInstance(query_chat_gpt, QueryGPT35)

    def test_create_correct_object_sed_gpt(self):
        sys.argv.extend(['--api_path', '../promptducer/query_api/apis/query_sed_gpt.py', '--api_name', 'QuerySEDGPT'])
        query_sed_gpt = QueryAPI.create(self.parser, self.prompter)
        self.assertIsInstance(query_sed_gpt, QuerySEDGPT)

    def test_use_api_class_names(self):
        sys.argv.extend([
            '--api_path', '../promptducer/query_api/apis/query_gpt35.py', '--use_api_class_names', '-n', 'QueryGPT35'
        ])
        query_chat_gpt = QueryAPI.create(self.parser, self.prompter)
        self.assertIsInstance(query_chat_gpt, QueryGPT35)
