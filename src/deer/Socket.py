import socket


class Socket(socket.socket):
    def __init__(self, **kwargs):
        super().__init__()

    def send(self, string: str) -> int:
        """
        Add carriage return and convert to bytes before sending.
        :return: nbytes sent
        """
        print(f">>> {string}")

        string += "\r\n"
        msg = bytes(string, "utf-8")

        super().send(msg)

    def connect(self, address):
        super().connect(address)
