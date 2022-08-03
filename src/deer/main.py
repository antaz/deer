import sys
import re
import importlib
import weather
import translate
from Socket import Socket
import urbandict

sys.path.append("..")

# NETWORK VARIABLES
HOSTNAME = "irc.libera.chat"
PORT = 6667
ADDRESS = (HOSTNAME, PORT)

# IRC VARIABLES
NICK = "deerBOT"
CHANNEL = "##deerbot"
BUFSIZE = 1024

# context  = ssl.create_default_context()
# COMMANDS = ['weather']


def first_conn(socket, channel):
    while True:
        data = socket.recv(1024).decode("utf-8")
        print(f"<<< {data}")

        if "PING" in data:
            socket.send("PONG")

        elif "Ident" in data:
            socket.send(f"NICK {NICK}")
            socket.send(f"USER {NICK} * {NICK} {NICK}")

        elif "376" in data:
            socket.send(f"JOIN {CHANNEL}")

            break


with Socket() as socket:
    socket.connect(ADDRESS)

    first_conn(socket, CHANNEL)

    while True:
        data = socket.recv(BUFSIZE).decode("utf-8")
        print(f"<<< {data}")

        if "PING" in data:
            socket.send("PONG")

        elif ":.reload" in data:
            importlib.reload(weather)
            print("Weather module reloaded.")
            importlib.reload(urbandict)
            print("UD module reloaded.")
            importlib.reload(translate)
            print("Translation module reloaded.")

        elif ":.weather" in data:
            city = weather.Weather(data)

            try:
                m = re.search(r"(PRIVMSG) (.*) (:)", data)
                channel = m.group(2)

            except Exception as e:
                print("\n", f"{e=}")
                continue

            msg = f"PRIVMSG {channel} :{city}"

            socket.send(msg)

        elif ".ud" in data:
            try:
                m = re.search(r"(PRIVMSG) (.*) (:)", data)
                channel = m.group(2)

            except Exception as e:
                print("\n", f"{e=}")
                continue

            definition = urbandict.UrbanDictionary(data)

            msg = f"PRIVMSG {channel} :{definition}"
            socket.send(msg)

        elif ".tr" in data:
            try:
                m = re.search(r"(PRIVMSG) (.*) (:)", data)
                channel = m.group(2)

            except Exception as e:
                print("\n", f"{e=}")
                continue

            translation = translate.Translate(data, source="any", target="fr")
            msg = f"PRIVMSG {channel} :{translation}"
            socket.send(msg)

        elif ".fr" in data:
            try:
                m = re.search(r"(PRIVMSG) (.*) (:)", data)
                channel = m.group(2)

            except Exception as e:
                print("\n", f"{e=}")
                continue

            translation = translate.Translate(data, source="fr", target="en")
            msg = f"PRIVMSG {channel} :{translation}"
            socket.send(msg)

        elif f"INVITE {NICK} :" in data:
            m = re.search(
                r"(nomn|momentum\@tilde\.team|leonarbro)( INVITE ){NICK}("
                r" :)(.*)\b",
                data,
            )
            try:
                channel = m.group(4).strip()
                socket.send(f"JOIN {channel}")

            except Exception as e:
                print(e)
                print(e)
