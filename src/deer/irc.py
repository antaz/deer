import socket
import time
import logging
import re
from queue import Queue
from threading import Thread

logger = logging.getLogger(__name__)


class TCPSocket:
    """
    Queue based TCP socket handler
    """

    def __init__(self, host, port):
        self.recvq = Queue()
        self.sendq = Queue()
        self.socket = socket.socket(socket.AF_INET, socket.TCP_NODELAY)
        self.host = host
        self.port = port

    def connect(self):
        while True:
            try:
                self.socket.connect((self.host, self.port))
            except socket.timeout:
                logger.error("conection timeout")
                time.sleep(60)
            except socket.error as e:
                logger.error(f"conecting to {self.host}:{self.port}: {e}")
            else:
                logger.info(f"connected to {self.host}:{self.port}")
                break
        Thread(target=self.recv_worker, daemon=False).start()
        Thread(target=self.send_worker, daemon=False).start()

    def putq(self, buf):
        self.sendq.put(buf.encode() + b"\r\n")

    def getq(self):
        return self.recvq.get()

    def close(self):
        try:
            self.socket.close()
        except socket.error as e:
            logger.error(f"closing connection: {e}")

    def recv(self, bufsize):
        return self.socket.recv(bufsize)

    def send(self, buf):
        self.socket.send(buf)

    def recv_worker(self):
        while True:
            buf = self.recv(4096)
            self.recvq.put(buf.decode("utf-8"))

    def send_worker(self):
        while True:
            buf = self.sendq.get()
            self.send(buf)


class IRC:
    """
    Implementation of the IRC protocol features
    """

    def __init__(self, conf):
        self.conf = conf
        self.socket = TCPSocket(conf["host"], conf["port"])

    def connect(self):
        self.socket.connect()
        self.ident(self.conf["nick"], self.conf["user"], self.conf["realname"])
        if self.conf["channels"]:
            self.join(self.conf["channels"])
        Thread(target=self.parse_worker, daemon=False).start()

    def ident(self, nick, user, realname):
        # As per IRCv3 spec https://modern.ircdocs.horse/#user-message
        self.cmd("NICK", [nick])
        self.cmd("USER", [user, "0", "*", f":{realname}"])

    def join(self, channels, keys=None):
        if keys:
            self.cmd("JOIN", [",".join(channels), ",".join(keys)])
        else:
            self.cmd("JOIN", [",".join(channels)])

    def msg(self, target, body):
        self.cmd("PRIVMSG", [target, body])

    def cmd(self, cmd, params):
        cmd = f'{cmd} {" ".join(params)}'
        self.send(cmd)

    def parse_worker(self):
        while True:
            msg = self.socket.getq()

            # spec: https://modern.ircdocs.horse/#message-format
            parsed_msg = re.match(
                r"""
                (?P<tag>@\S+\s)?
                (?P<source>:\S+\s)?
                (?P<cmd>\S+\s)
                (?P<params>.*)
                \r\n""",
                msg,
                re.VERBOSE,
            )

            if parsed_msg:
                print(msg)
                if parsed_msg.group("cmd") == "PING":
                    self.send(msg.replace("PING", "PONG"))
                elif parsed_msg.group("cmd") == "PRIVMSG":
                    (chan, msg) = parsed_msg.group("params").split(":", 1)

    def send(self, msg):
        self.socket.putq(msg)

    def quit(self, msg):
        self.cmd("QUIT", [f":{msg}"])
        self.socket.close()
