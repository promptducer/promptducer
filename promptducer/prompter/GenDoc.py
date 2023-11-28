from promptducer.prompter.prompter import PromptTemplate


class GenDoc(PromptTemplate):

    def __init__(self):
        self.prompt_template = "You are a professional Python developer. " \
                               "You will get a Python method which lacks of documentation. " \
                               "Your task is to create a documentation in the beginning of the method which summarizes the method. " \
                               "You will also have access to the description of the project."
        self.prompt_postfix = "It is very important for me, please create the documentation based on your best knowledge based on the given descriptions. " \
                              "Provide the full, documented method and write detailed comments explaining your way of thinking."

    def create_prompt(self, src, metadata=None) -> str:
        additional_data = f"The method comes from a project with the following brief description: {metadata.get('project_description', 'None')}"
        return self.prompt_template + additional_data + "\n\n" + src + "\n\n" + self.prompt_postfix
