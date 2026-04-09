import json

from .command import HamiltonCommand, HamiltonResponseType
from .connection import HamiltonConnection


class HamiltonDevice:
    def __init__(self, connection: HamiltonConnection):
        self.connection = connection
        self.busy: bool = False

    def execute_command(self, command: HamiltonCommand[HamiltonResponseType]) -> HamiltonResponseType:
        if self.busy:
            raise RuntimeError("Device is busy executing another command")

        self.connection.send(f"{json.dumps(command.as_dict())}\n")

        if self.connection.receive() != "CommandAccepted":
            raise RuntimeError(f"Command does not exist on the device: {HamiltonDevice.__name__}")

        self.busy = True

        # Wait for state to be idle

        while True:
            self.connection.send("get_state\n")
            data = self.connection.receive()

            if data != "Busy":
                break

        self.busy = False

        response_data = json.loads(self.connection.receive())

        # This is a non recoverable program related error. We do not attempt to recover these. Only recover device errors.
        if response_data["programmatic_error_description"] != "":
            raise RuntimeError(
                f"Error occurred while executing command: {response_data['programmatic_error_description']}",
            )

        del response_data["programmatic_error_description"]

        return command.parse_response(response_data)
