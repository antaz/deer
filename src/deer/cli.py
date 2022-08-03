from deer.irc import IRC
import click


@click.command()
@click.option("-h", "--host", help="Server address", required=True)
@click.option("-p", "--port", help="Server port", required=True, type=int)
@click.option("-n", "--nick", help="Bot nickname", required=True)
@click.option("-u", "--user", help="Bot user", required=True)
@click.option(
    "-c",
    "--chan",
    help="Channel to join. use multiple options for more than one channel",
    multiple=True,
)
def main(host, port, nick, user, chan):
    irc = IRC(
        {
            "host": host,
            "port": port,
            "nick": nick,
            "user": user,
            "realname": user,
            "channels": chan,
        }
    )
    irc.connect()
