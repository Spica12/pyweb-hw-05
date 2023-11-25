import asyncio
import logging
import sys

from aiopath import AsyncPath

BASE_DIR = AsyncPath()
LOG_FILE_NAME = "logs.txt"


if __name__ == "__main__":
    logger = logging.getLogger("pylog")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)20s(%(lineno)3d) - %(levelname)5s - %(message)s"
    )

    path_logs = BASE_DIR / LOG_FILE_NAME

    fh = logging.FileHandler(filename=path_logs)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info('Start program ""PythonWeb-Homework-05')

    days = sys.argv[1]

    logger.info(f"How many days user want to get data: {days} days")
