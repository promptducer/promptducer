import html
import os
from argparse import ArgumentParser

import requests

from promptducer.prompter.prompter import Prompter
from promptducer.query_api.query_api import QueryAPI
from promptducer.query_api.token_counter import TokenCounter
from promptducer.source_reader.source_reader import FileUtility

SEDGPT_URL = 'http://193.225.251.173:8080/instruct'


class QuerySEDGPT(QueryAPI):
    """
    A QueryAPI class for SED-hosted LLM model.
    Requires "SEDGPT_TOKEN" environment variable (or in the .env file)
    """

    def __init__(self, arguments: ArgumentParser, prompter: Prompter):
        super().__init__(arguments, prompter)
        if os.getenv("SEDGPT_TOKEN") is None:
            raise ValueError('API key missing! Please provide "SEDGPT_TOKEN" in environment variables!')
        else:
            self.api_key = os.getenv("SEDGPT_TOKEN")
        self.model = "sedgpt"
        self.token_counter = TokenCounter(self.results_base_dir, self.api_name)

    def run_query(self, conversation: list[str]) -> str:
        self.token_counter.start_measure()
        response_obj = self.token_counter.count_token(
            requests.post(
                SEDGPT_URL,
                json={
                    'prompt': FileUtility.read_file(conversation[0]),
                    'password': self.api_key
                }
            ).json())

        if response_obj.get("history"):
            self.token_counter.stop_measure(self.args.prompt_file)
            return html.unescape(response_obj["history"][-1])
        else:
            raise ValueError("There was an error getting the response string: no 'history' field!")
