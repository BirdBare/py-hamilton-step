import asyncio
import json

from .command import VenusCommand, VenusResponseType
from .connection import VenusConnection

POLL_INTERVAL = 0.1  # seconds — tune to your device's typical response time


class VenusExecutor:
    def __init__(self, connection: VenusConnection):
        self.connection = connection
        self.busy: bool = False

    async def _execute_command_json(self, command_json: dict) -> dict:
        if self.busy:
            raise RuntimeError("Device is busy executing another command")

        await self.connection.send(f"{json.dumps(command_json)}\n")

        if await self.connection.receive() != "CommandAccepted":
            raise RuntimeError("Command does not exist")

        self.busy = True

        while True:
            await self.connection.send("get_state\n")
            data = await self.connection.receive()
            if data != "Busy":
                break
            await asyncio.sleep(POLL_INTERVAL)  # yield to event loop instead of spinning

        self.busy = False

        response_data = json.loads(await self.connection.receive())

        if response_data["programmatic_error_description"] != "":
            raise RuntimeError(
                f"Error occurred while executing command: {response_data['programmatic_error_description']}",
            )

        del response_data["programmatic_error_description"]

        return response_data

    async def execute_command(self, command: VenusCommand[VenusResponseType]) -> VenusResponseType:
        response_data = await self._execute_command_json(command.as_dict())

        return command.parse_response(response_data)
