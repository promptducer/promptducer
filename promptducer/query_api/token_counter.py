import json
import os

from promptducer.source_reader.source_reader import FileUtility


class TokenCounter:
    def __init__(self, base_dir, api_name, output_dir):
        self.input_tokens = 0
        self.generated_tokens = 0
        self.chat_object = []
        self.is_measuring = False

        # saved for the output
        self.base_dir = base_dir
        self.api_name = api_name
        self.output_dir = os.path.dirname(output_dir)

    def start_measure(self):
        self.is_measuring = True

    def stop_measure(self, measured_prompt_file_path):
        json_obj = {
            "total_input_tokens": self.input_tokens,
            "total_generated_tokens": self.generated_tokens,
            "measured_prompt_file_path": measured_prompt_file_path,
            "chats": self.chat_object
        }

        json_obj = json.dumps(json_obj, indent=2)

        # Bugfix
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

        FileUtility.append_file(os.path.join(
            self.output_dir,
            f"RES_COST_{self.api_name}.token"), json_obj)

        self.input_tokens = 0
        self.generated_tokens = 0
        self.chat_object.clear()
        self.is_measuring = False

    def count_token(self, res):
        if not self.is_measuring:
            raise Exception("You can't count the tokens unless you call start_measure() beforehand.")

        self.input_tokens += res.usage.prompt_tokens
        self.generated_tokens += res.usage.completion_tokens
        self.chat_object.append({
            "id": res.id,
            "object": res.object,
            "created": res.created,
            "model": res.model,
            "choices": [
                {
                    "index": res.choices[-1].index,
                    "message": {
                        "role": res.choices[-1].message.role,
                        "content": res.choices[-1].message.content
                    },
                    "finish_reason": res.choices[-1].finish_reason
                }
            ],
            "usage": {
                "prompt_tokens": res.usage.prompt_tokens,
                "completion_tokens": res.usage.completion_tokens,
                "total_tokens": res.usage.total_tokens
            }
            })

        return res
