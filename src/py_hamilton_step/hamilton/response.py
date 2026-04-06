import abc
import dataclasses


@dataclasses.dataclass
class HamiltonResponse(abc.ABC):
    """
    Base class for all Hamilton responses.
    The communication contract is that all serialized responses will contain the following fields:
    - command_id: the unique identifier of the command that this response is for
    """

    command_id: str
