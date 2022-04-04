import socket
import ssl
import sys
import re

sys.path.append('..')
import weather


hostname = 'irc.libera.chat'
port = 6667
CHANNEL = '##deerbot'
context = ssl.create_default_context()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

    s.connect((hostname, port))

    while True:

        data = s.recv(1024).decode('utf-8')
        print(f"{data=}")

        if "PING" in data:
            s.send(b'PONG\r\n')

        elif ".weather" in data:

            m = re.search(r'(weather) (.*)\b', data)

            try:
                print(m.group(2).strip())

            except Exception:
                s.send(b'PRIVMSG {CHANNEL} :Which city bitch?\r\n')
                continue

            city = weather.Weather(m.group(2).strip())
            msg = bytes(f'PRIVMSG {CHANNEL} :{city}\r\n', 'utf-8')
            s.send(msg)
            print(f"{msg=}")


        elif "No Ident" in str(data):
            s.send(b'NICK deerBOT\r\n')
            s.send(b'USER deerBOT * deerBOT deerBOT\r\n')

        elif "376" in str(data):
            msg = bytes(f'JOIN {CHANNEL} \r\n', 'utf-8')
            s.send(msg)

