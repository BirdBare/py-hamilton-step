import abc
import asyncio
import platform

import serial_asyncio


class VenusConnection(abc.ABC):
    @abc.abstractmethod
    async def connect(self) -> None:
        pass

    @abc.abstractmethod
    async def disconnect(self) -> None:
        pass

    @abc.abstractmethod
    async def send(self, data: str) -> None:
        pass

    @abc.abstractmethod
    async def receive(self) -> str:
        pass

    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.disconnect()


class UnixSocketConnection(VenusConnection):
    """
    Implementation of VenusConnection using Unix domain sockets.
    Meant to be used for communication where python is running on a unix machine and Venus is running in a virtual machine.
    General use is MacOS host with parallels running a windows VM with Venus.
    Venus must be started manually on the windows VM
    """

    def __init__(self, socket_path: str):
        super().__init__()
        if platform.system() not in ["Linux", "Darwin"]:
            raise OSError("UnixSocketConnection can only be used on Unix machines.")
        self.socket_path = socket_path
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        self._reader, self._writer = await asyncio.open_unix_connection(self.socket_path)

    async def disconnect(self) -> None:
        if not self._writer:
            raise ConnectionError("Not connected to socket.")
        self._writer.close()
        await self._writer.wait_closed()
        self._reader = self._writer = None

    async def send(self, data: str) -> None:
        if not data.endswith("\n"):
            raise ValueError("Data must end with a newline character.")
        if not self._writer:
            raise ConnectionError("Not connected to socket.")
        self._writer.write(data.encode())
        await self._writer.drain()

    async def receive(self) -> str:
        if not self._reader:
            raise ConnectionError("Not connected to socket.")
        line = await self._reader.readline()
        return line.decode().strip()


class WindowsVirtualCOMConnection(VenusConnection):
    """
    Implementation of VenusConnection using virtual COM ports.
    Meant to be used for communication where python and Venus are running on the same windows machine.
    Venus will be started automatically as a subprocess.
    """

    def __init__(self, com_port: str):
        super().__init__()
        if platform.system() != "Windows":
            raise OSError("WindowsVirtualCOMConnection can only be used on Windows machines.")
        self.com_port = com_port
        self._reader: asyncio.StreamReader | None = None
        self._writer: asyncio.StreamWriter | None = None

    async def connect(self) -> None:
        self._reader, self._writer = await serial_asyncio.open_serial_connection(
            url=self.com_port,
            baudrate=9600,
        )
        # TODO: launch Venus subprocess

    async def disconnect(self) -> None:
        if not self._writer:
            raise ConnectionError("Not connected to COM port.")
        self._writer.close()
        await self._writer.wait_closed()
        self._reader = self._writer = None
        # TODO: kill Venus subprocess

    async def send(self, data: str) -> None:
        if not data.endswith("\n"):
            raise ValueError("Data must end with a newline character.")
        if not self._writer:
            raise ConnectionError("Not connected to COM port.")
        self._writer.write(data.encode())
        await self._writer.drain()

    async def receive(self) -> str:
        if not self._reader:
            raise ConnectionError("Not connected to COM port.")
        line = await self._reader.readline()
        return line.decode().strip()
