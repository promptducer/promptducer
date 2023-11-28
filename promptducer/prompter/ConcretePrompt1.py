from promptducer.prompter.prompter import PromptTemplate


class ConcretePrompt1(PromptTemplate):
    """
    A concrete prompt example. Inherits the PromptTemplate interface.

    Attributes
    ----------
    prompt_template : str
        The string that takes place before the code
    """
    def __init__(self):
        self.prompt_template = "Is it C++ or Java or Natural text?"

    def create_prompt(self, src, metadata=None) -> str:
        """
        Creates a prompt by placing the prompt string and the source code together.
        :param src: The source code you want to use in the prompt.
        :return: Returns the actual prompt
        """
        print("src", src)
        return self.prompt_template + " " + src
