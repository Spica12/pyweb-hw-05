import asyncio
import logging
import sys
import datetime

import aiohttp
from aiopath import AsyncPath

from pprint import pprint

BASE_DIR = AsyncPath()
LOG_FILE_NAME = "logs.txt"
URL = "https://api.privatbank.ua/p24api/exchange_rates"  # example ... ?json&date=01.12.2014"
BASE_CURRENCY = ["EUR", "USD"]


class HttpError(Exception):
    pass


async def request(url: str):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as resp:
                if resp.status == 200:
                    result = await resp.json()
                    return result
                else:
                    raise HttpError(f"Error status: {resp.status} for {url}")

        except aiohttp.ClientConnectionError as err:
            raise HttpError(f"Connection error: {url}, str(err)")


def normalize_response(response: dict, currencies: list):
    new_response = {}

    date = response["date"]

    exchange_rates = {}
    for rate in response["exchangeRate"]:
        if rate["currency"] not in currencies:
            continue

        currency = rate["currency"]
        exchange_rates[currency] = {}
        exchange_rates[currency]["sale"] = rate["saleRateNB"]
        exchange_rates[currency]["purchase"] = rate["purchaseRateNB"]

    new_response[date] = exchange_rates

    return new_response


async def get_exchange_rate(days: int, user_currencies: list):
    current_day = datetime.datetime.now().date()

    currencies = BASE_CURRENCY + user_currencies
    logger.debug(f"Currencies: {currencies}")

    result = []

    for daydelta in range(days):
        day = current_day - datetime.timedelta(days=daydelta)

        request_day = datetime.datetime.strftime(day, "%d.%m.%Y")
        logger.debug(
            f"Current day: {current_day} -> delta {daydelta} days -> Day for request: {request_day}"
        )

        request_url = f"{URL}?json&date={request_day}"
        logger.debug(f"URL for request: {request_url}")

        try:
            response = normalize_response(await request(request_url), currencies)
            result.append(response)

        except HttpError as err:
            logger.error(err)

    return result


def parse_argv():
    logger.debug(sys.argv)

    days = None
    currencies = []

    if len(sys.argv) > 1:
        days = int(sys.argv[1])
        logger.info(f"How many days user want to get exchange rates: {days} days")

        if days >= 10:
            logger.info(f"Maximum days is 10 days")
            days = 10
            logger.info(f"User's request changed to {days} days")

    if len(sys.argv) > 2:
        user_currencies = sys.argv[2:]
        logger.info(f"User currencies: {user_currencies}")

    return days, user_currencies


async def main():
    days, user_currencies = parse_argv()

    if days:
        exchange_rate = await get_exchange_rate(days, user_currencies)
        pprint(exchange_rate)


if __name__ == "__main__":
    logger = logging.getLogger("pylog")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)20s(%(lineno)3d) - %(levelname)5s - %(message)s"
    )

    path_logs = BASE_DIR / LOG_FILE_NAME

    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    print('----- Start program "PythonWeb-Homework-05" -----')

    asyncio.run(main())

    print('----- Finish -----')
