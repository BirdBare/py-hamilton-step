import abc
import platform
import socket

import serial


class HamiltonConnection(abc.ABC):
    @abc.abstractmethod
    def connect(self) -> None:
        pass

    @abc.abstractmethod
    def disconnect(self) -> None:
        pass

    @abc.abstractmethod
    def send(self, data: str) -> None:
        pass

    @abc.abstractmethod
    def receive(self) -> str:
        pass

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.disconnect()


class UnixSocketConnection(HamiltonConnection):
    """
    Implementation of HamiltonConnection using Unix domain sockets.
    Meant to be used for communication where python is running on a unix machine and Venus is running in a virtual machine.
    General use is MacOS host with parallels running a windows VM with Venus.
    """

    def __init__(self, socket_path: str):
        super().__init__()

        if platform.system() not in ["Linux", "Darwin"]:
            raise OSError("UnixSocketConnection can only be used on Unix machines.")

        self.socket_path = socket_path
        self.sock = None

    def connect(self) -> None:
        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.settimeout(10)
        self.sock.connect(self.socket_path)

    def disconnect(self) -> None:
        if not self.sock:
            raise ConnectionError("Not connected to socket.")

        self.sock.close()
        self.sock = None

    def send(self, data: str) -> None:
        if not data.endswith("\n"):
            raise ValueError("Data must end with a newline character.")

        if not self.sock:
            raise ConnectionError("Not connected to socket.")

        self.sock.sendall(data.encode())

    def receive(self) -> str:
        if not self.sock:
            raise ConnectionError("Not connected to socket.")

        with self.sock.makefile(buffering=1) as f:
            return f.readline().strip()


class WindowsVirtualCOMConnection(HamiltonConnection):
    """
    Implementation of HamiltonConnection using virtual COM ports.
    Meant to be used for communication where python and Venus are running on the same windows machine.
    """

    def __init__(self, com_port: str):
        super().__init__()

        if platform.system() != "Windows":
            raise OSError("WindowsVirtualCOMConnection can only be used on Windows machines.")

        self.com_port = com_port
        self.serial_port = None

    def connect(self) -> None:
        self.serial_port = serial.Serial(self.com_port, baudrate=9600, timeout=10)

        # TODO: use subprocess to start venus software

    def disconnect(self) -> None:
        if not self.serial_port:
            raise ConnectionError("Not connected to COM port.")

        self.serial_port.close()
        self.serial_port = None

        # TODO: kill venus software subprocess

    def send(self, data: str) -> None:
        if not data.endswith("\n"):
            raise ValueError("Data must end with a newline character.")

        if not self.serial_port:
            raise ConnectionError("Not connected to COM port.")

        self.serial_port.write(data.encode())

    def receive(self) -> str:
        if not self.serial_port:
            raise ConnectionError("Not connected to COM port.")

        return self.serial_port.readline().decode().strip()
