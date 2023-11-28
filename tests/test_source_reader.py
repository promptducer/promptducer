import sys
from argparse import ArgumentParser
from unittest import TestCase

from promptducer.source_reader.source_reader import SourceReader

BAD_EXAMPLES = '../tests/source_reader_test_files/bad_examples'
GOOD_EXAMPLES = '../tests/source_reader_test_files/good_examples'


class TestSourceReader(TestCase):
    def setUp(self) -> None:
        self.parser = ArgumentParser()
        self.parser.add_argument('-s', '--source_code_base_dir')
        self.parser.add_argument('-f', '--file_extension', nargs="+")

    def test_reads_according_to_kind(self):
        sys.argv.extend(['-s', BAD_EXAMPLES])
        self.parser.parse_args()
        self.source_reader = SourceReader(self.parser)
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// BAD JAVA 1 this is the content\n")

    def test_all_files_bad(self):
        sys.argv.extend(['-s', BAD_EXAMPLES])
        self.parser.parse_args()
        self.source_reader = SourceReader(self.parser)
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// BAD JAVA 1 this is the content\n")
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, '{\n  "nothing": "Hello"\n}')
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// BAD JAVA 2")
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "# BAD PYTHON 3")
        self.assertIsNone(self.source_reader.read_next_source())

    def test_one_file_extension_bad(self):
        sys.argv.extend(['-s', BAD_EXAMPLES, "-f", "java"])
        self.parser.parse_args()
        self.source_reader = SourceReader(self.parser)
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// BAD JAVA 1 this is the content\n")

        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// BAD JAVA 2")
        self.assertIsNone(self.source_reader.read_next_source())

    def test_multiple_file_extension_good(self):
        sys.argv.extend(['-s', GOOD_EXAMPLES, "-f", "java", "py"])
        self.parser.parse_args()
        self.source_reader = SourceReader(self.parser)
        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// GOOD JAVA 1")

        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// GOOD JAVA 2")

        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "# GOOD PYTHON 3")

        file_path, file_content = self.source_reader.read_next_source()
        self.assertEqual(file_content, "// GOOD JAVA 4")

        self.assertIsNone(self.source_reader.read_next_source())
