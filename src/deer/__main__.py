import logging
import cli

if __name__ == "__main__":
    logging.basicConfig(
        filename="deer.log",
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=logging.DEBUG,
    )
    cli.main()
