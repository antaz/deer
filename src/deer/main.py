import ssl
import sys
import re
import importlib

sys.path.append('..')
import weather
from Socket import Socket
from ud import UrbanDictionary as UD

# NETWORK VARIABLES
HOSTNAME = 'irc.libera.chat'
PORT     = 6667
ADDRESS  = (HOSTNAME, PORT)

# IRC VARIABLES
NICK     = 'deerBOT'
CHANNEL  = '##deerbot'
BUFSIZE  = 1024

#context  = ssl.create_default_context()
#COMMANDS = ['weather']


def first_conn(socket, channel):

    while True:

        data = socket.recv(1024).decode('utf-8')
        print(f"<<< {data}")

        if "PING" in data:
            socket.send('PONG')

        elif "No Ident" in data:
            socket.send(f'NICK {NICK}')
            socket.send(f'USER {NICK} * {NICK} {NICK}')

        elif "376" in data:
            socket.send(f'JOIN {CHANNEL}')

            break



with Socket() as socket:

    socket.connect(ADDRESS)

    first_conn(socket, CHANNEL)
    

    while True:

        data = socket.recv(BUFSIZE).decode('utf-8')
        print(f"<<< {data}")

        if "PING" in data:
            socket.send('PONG')

        elif ":.reload" in data:
            importlib.reload(weather)
            print("Weather module reloaded.")
            importlib.reload(ud)
            print("UD module reloaded.")


        elif ":.weather" in data:

            city = weather.Weather(data)

            try:
                m = re.search(r'(PRIVMSG) (.*) (:)', data)
                channel = m.group(2)

            except Exception as e:
                print('\n', f"{e=}")
                continue


            msg = f'PRIVMSG {channel} :{city}'

            socket.send(msg)

        elif '.ud' in data:

            try:
                m = re.search(r'(PRIVMSG) (.*) (:)', data)
                channel = m.group(2)

            except Exception as e:
                print('\n', f"{e=}")
                continue

            definition = UD(data)

            msg = f'PRIVMSG {channel} :{definition}'
            socket.send(msg)


        elif f"nomn INVITE {NICK} :" in data:

            m = re.search(rf'(nomn INVITE ){NICK}( :)(.*)\b', data)
            try:
                channel = m.group(3).strip()
                socket.send(f'JOIN {channel}')


            except Exception as e:
                print(e)
                print(e)

