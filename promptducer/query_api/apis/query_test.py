import os
from argparse import ArgumentParser

import openai

from promptducer.prompter.prompter import Prompter
from promptducer.query_api.query_api import QueryAPI


class QueryTest(QueryAPI):
    """
    A QueryAPI class for OpenAI's gpt-3.5-turbo model.
    Requires "openai" field with API key in the api_keys.json file.
    """

    def __init__(self, arguments: ArgumentParser, prompter: Prompter):
        super().__init__(arguments, prompter)
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError('API key missing! Please provide "OPENAI_API_KEY" in either .env or environment variables!')
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-3.5-turbo"

    def run_query(self, conversation: list[str]) -> str:
        return "conversation: " + "\n\n".join(conversation)
