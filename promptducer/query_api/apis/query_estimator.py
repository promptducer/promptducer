import os
from argparse import ArgumentParser

import openai
import tiktoken

from promptducer.prompter.prompter import Prompter
from promptducer.query_api import TokenCounter
from promptducer.query_api.query_api import QueryAPI

enc = tiktoken.encoding_for_model("gpt-4")

def calculate_length(msg:str)->int:
    prompt_tokens = enc.encode(msg)
    return len(prompt_tokens)

class QueryEstimator(QueryAPI):
    """
    A Query to estimate the total cost of running an actual evaluation.
    """

    def __init__(self, arguments: ArgumentParser, prompter: Prompter, model="gpt-4"):
        super().__init__(arguments, prompter)
        self.multiplier = 1
        self.total_tokens = 0
        self.token_counter = TokenCounter(self.results_base_dir, self.api_name, self.prompter.output_folder)

    def run_query(self, conversation: list[str]) -> str:
        tokens = 0
        for idx, msg in enumerate(conversation):
            tokens += calculate_length(msg)

        self.total_tokens += tokens
        print(f"Total tokens so far {self.total_tokens} input and {self.total_tokens * self.multiplier} output tokens")
        print(f"Current cost would be: {self.total_tokens * (0.01 + 0.03*self.multiplier) / 1_000}") # these are open ai hardcoded values for gpt-4
        return f"Estimation calculated."
