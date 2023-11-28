from abc import ABC, abstractmethod
from argparse import ArgumentParser

from promptducer import helpers


class Responder(ABC):
    """
    An abstract class for responders which are responsible for generating a reply message to the model output.
    The create factory method is used to instantiate the corresponding responder object.

    Attributes
    ----------
    stop_reached : bool
        This indicates whether a stop condition is met and no further responses are required.
    """

    def __init__(self, arguments: ArgumentParser):
        args = arguments.parse_args()

        self.stop_reached = False
        self.responder_name = args.responder_name

    @classmethod
    def create(cls, arguments: ArgumentParser):
        """
        Factory method which returns the corresponding responder object specified in the ArgumentParser.

        Parameters
        ----------
        arguments : ArgumentParser
            An ArgumentParser which contains the responder_name to be used
            and whether the provided name is a module name or a class name.

        Returns
        -------
        An instance of the corresponding responder class.

        Notes
        -----
        By default each specific responder class must be in a separate module in the responders_dir and
        each responder must be referenced by its MODULE NAME in the arguments. e.g. "manual_response".
        Responder class names can be used instead of module names by providing an
        argument "--use_responder_class_names". This way classes do not need to be in separate modules.
        The location of the responder modules must be set in the paths.json file.
        """

        # Parse arguments
        args = arguments.parse_args()
        responder_name = args.responder_name
        if not responder_name:
            return None

        # Find responders
        responders = helpers.import_module(
            args.responder_file,
            args.responder_name
        )(arguments)

        # Instantiate selected responder class
        # responder_class = responders.get(responder_name)
        # if responder_class:
            # return responder_class(arguments)
        if responders:
            return responders
        else:
            raise ValueError(f"Invalid responder name: {responder_name}")

    @abstractmethod
    def respond(self, conversation: str) -> str | None:
        """
        Generates a response based on the given API output string.
        """
        pass
