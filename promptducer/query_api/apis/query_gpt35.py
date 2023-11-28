import os
from argparse import ArgumentParser

import openai

from promptducer.prompter.prompter import Prompter
from promptducer.query_api import TokenCounter
from promptducer.query_api.query_api import QueryAPI


class QueryGPT35(QueryAPI):
    """
    A QueryAPI class for OpenAI's gpt-3.5-turbo model.
    Requires "openai" field with API key in the api_keys.json file.
    """

    def __init__(self, arguments: ArgumentParser, prompter: Prompter, model="gpt-3.5-turbo-16k-0613"):
        super().__init__(arguments, prompter)
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                'API key missing! Please provide "OPENAI_API_KEY" in either .env or environment variables!'
            )
        else:
            openai.api_key = os.getenv("OPENAI_API_KEY")
        self.model = model
        self.token_counter = TokenCounter(self.results_base_dir, self.api_name, self.prompter.output_folder)

    def run_query(self, conversation: list[str]) -> str:

        messages = [
            {
                "role": "assistant" if idx % 2 else "user",
                "content": msg
            }
            for idx, msg in enumerate(conversation)
        ]

        response_obj = self.token_counter.count_token(openai.ChatCompletion.create(model=self.model, messages=messages))

        if response_obj.choices:
            return response_obj.choices[0].message.content
        else:
            raise ValueError("There was an error getting the response string: no 'choices' field!")
