import abc
import dataclasses
import uuid

from .response import HamiltonResponse


@dataclasses.dataclass
class HamiltonCommand(abc.ABC):
    """
    Base class for all Hamilton commands.
    The communication contract is that all serialized command will contain the following fields:
    - id: a unique identifier for the command
    - command: the name of the command, which should match the class name of the command
    - args: a dictionary of arguments specific to the command, which should be defined by the subclass
    """

    id: str = dataclasses.field(init=False, default_factory=lambda: str(uuid.uuid4()))

    @abc.abstractmethod
    def as_dict(self) -> dict:
        return {"id": str(self.id), "command": self.__class__.__name__, "args": {}}

    @abc.abstractmethod
    def parse_response(self, data: dict) -> HamiltonResponse:
        pass
