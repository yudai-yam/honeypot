import uvicorn

from src.utils.logging_config import get_logger, setup_logging


def main():

    # set up the logger
    setup_logging()
    get_logger(__name__)

    uvicorn.run("src.honeypot.route:app", host="0.0.0.0", port=80)


if __name__ == "__main__":
    main()
