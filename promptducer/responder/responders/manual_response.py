from argparse import ArgumentParser

from promptducer.responder.responder import Responder


class ManualResponse(Responder):
    """
    A Responder class which takes manual user input as the response message.
    When the user types a single letter 'E', the stop condition is met.
    """

    def __init__(self, arguments: ArgumentParser):
        super().__init__(arguments)

    def respond(self, conversation: str) -> str | None:
        print(conversation[-1])
        print("\n----------\n")
        user_input = input("Type your message! (type 'E' to end session)\n")
        if user_input == 'E':
            self.stop_reached = True
            return None
        else:
            return user_input
