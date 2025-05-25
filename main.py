import uvicorn

from src.utils.logging_config import setup_logging, get_logger


def main():

    # set up the logger
    setup_logging()
    get_logger(__name__)




if __name__ == "__main__":
    uvicorn.run("honeypot:app", host="0.0.0.0", port=80)