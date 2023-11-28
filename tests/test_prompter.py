import os
import shutil
import sys
from argparse import ArgumentParser
from unittest import TestCase

from promptducer.prompter.prompter import Prompter

BAD_EXAMPLES = '../tests/source_reader_test_files/bad_examples'

TEST_OUTPUT = "test_output"


class TestPrompter(TestCase):

    def setUp(self) -> None:
        self.parser = ArgumentParser()
        self.parser.add_argument('-p', '--prompt_name')
        self.parser.add_argument('-s', '--source_code_base_dir')
        self.parser.add_argument('-f', '--file_extension', nargs="+")
        self.parser.add_argument('-r', '--results_base_dir')

        self.parser.add_argument('--prompt_file')

    def tearDown(self):
        if os.path.exists(TEST_OUTPUT):
            shutil.rmtree(TEST_OUTPUT)

    def test_create_prompt(self):
        sys.argv.extend(['--prompt_file', '../promptducer/prompter/ConcretePrompt1.py', '-s', BAD_EXAMPLES])
        self.parser.parse_args()
        self.prompter = Prompter(self.parser)
        file_path, file_content = self.prompter.source_reader.read_next_source()
        self.prompter.prompt_template.prompt_template = "Valami okosság:"

        self.assertEqual(self.prompter.prompt_template.create_prompt(src=file_content), "Valami okosság: " + file_content)

    def test_get_prompt(self):
        sys.argv.extend(['--prompt_file', '../promptducer/prompter/ConcretePrompt1.py', '-p' 'ConcretePrompt1', '-r', TEST_OUTPUT, '-s', BAD_EXAMPLES])
        self.parser.parse_args()

        self.prompter = Prompter(self.parser)
        self.prompter.prompt_template.prompt_template = "Kérlek javítsd ki ezt a rossz kódot"

        p = self.prompter.get_prompt()
        self.assertNotEqual(self.prompter.get_prompt(), p)  # sourcereader is ok ???
