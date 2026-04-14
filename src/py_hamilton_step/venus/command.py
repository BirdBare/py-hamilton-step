import abc
import dataclasses
import typing
import uuid

VenusResponseType = typing.TypeVar("VenusResponseType", bound="VenusResponse")


@dataclasses.dataclass(frozen=True)
class VenusResponse(abc.ABC):
    """
    Base class for all Hamilton responses.
    The communication contract is that all serialized responses will contain the following fields:
    - command_id: the unique identifier of the command that this response is for
    """

    command_id: str


@dataclasses.dataclass(kw_only=True, frozen=True)
class VenusCommand(abc.ABC, typing.Generic[VenusResponseType]):
    """
    Base class for all Hamilton commands.
    The communication contract is that all serialized command will contain the following fields:
    - id: a unique identifier for the command
    - command: the name of the command, which should match the class name of the command
    - args: a dictionary of arguments specific to the command, which should be defined by the subclass
    """

    id: str = dataclasses.field(init=False, default_factory=lambda: str(uuid.uuid4()))
    venus_handle_errors: bool = False

    @abc.abstractmethod
    def as_dict(self) -> dict:
        return {
            "id": str(self.id),
            "command": self.__class__.__name__,
            "args": {"venus_handle_errors": str(self.venus_handle_errors)},
        }

    @staticmethod
    @abc.abstractmethod
    def parse_response(data: dict) -> VenusResponseType:
        pass
