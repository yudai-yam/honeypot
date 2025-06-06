import os

import uvicorn
from dotenv import dotenv_values, load_dotenv

from src.utils.logging_config import get_logger, setup_logging

load_dotenv()


def main():

    # set up the logger
    setup_logging()
    get_logger(__name__)

    host = os.getenv("HOST")
    port = int(os.getenv("PORT"))

    uvicorn.run("src.honeypot.route:app", host=host, port=port)


if __name__ == "__main__":
    main()
