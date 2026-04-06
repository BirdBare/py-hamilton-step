import json
import typing

from .command import HamiltonCommand
from .connection import HamiltonConnection
from .response import HamiltonResponse


class HamiltonDevice:
    def __init__(self, connection: HamiltonConnection):
        self.connection = connection
        self._active_command: HamiltonCommand | None = None

    def _acknowledge_command(self) -> typing.Literal["CommandAccepted", "CommandRejected"]:
        """
        Breaks the agreed communication contract.
        It is only used internally.
        """
        self.connection.send("acknowledge_command\n")
        data = self.connection.receive()

        if data not in ["CommandAccepted", "CommandRejected"]:
            raise RuntimeError(f"Received invalid acknowledge response: {data}")

        return typing.cast("typing.Literal['CommandAccepted', 'CommandRejected']", data)

    def _get_state(self) -> typing.Literal["Busy", "Idle"]:
        """
        Breaks the agreed communication contract.
        It is only used internally.
        """
        self.connection.send("get_state\n")
        data = self.connection.receive()

        if data not in ["Busy", "Idle"]:
            raise RuntimeError(f"Received invalid state response: {data}")

        return typing.cast("typing.Literal['Busy', 'Idle']", data)

    def _get_response(self) -> str:
        """
        Breaks the agreed communication contract.
        It is only used internally.
        """
        self.connection.send("get_response\n")
        data = self.connection.receive()

        return data

    def send_command(self, command: HamiltonCommand):
        if self._active_command is not None:
            raise RuntimeError(f"A command is already executing: {self._active_command.id}")

        # Send the step command
        self.connection.send(f"{json.dumps(command.as_dict())}\n")

        if self._acknowledge_command() != "CommandAccepted":
            raise RuntimeError("Command was not accepted by the device")

        self._active_command = command

    def get_response(self) -> None | HamiltonResponse:
        if self._active_command is None:
            raise RuntimeError("No active command to get response")

        if self._get_state() == "Busy":
            return None

        response = self._active_command.parse_response(json.loads(self._get_response()))

        if response.command_id != self._active_command.id:
            raise RuntimeError(
                f"Received response for command {response.command_id} but expected response for command {self._active_command.id}",
            )

        self._active_command = None

        return response
