import asyncio
import datetime
import logging
import sys
from pprint import pprint

import aiohttp
import names
import websockets
from aiopath import AsyncPath
from websockets import WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK

BASE_DIR = AsyncPath()
LOG_FILE_NAME = "logs.txt"
URL = "https://api.privatbank.ua/p24api/exchange_rates"  # example ... ?json&date=01.12.2014"
BASE_CURRENCY = ["EUR", "USD"]


class HttpError(Exception):
    pass


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.lower().startswith("exchange"):
                days, user_currencies = parse_argv(message.split())

                if days:
                    result = await get_exchange_rate(days, user_currencies)
                else:
                    result = await get_exchange_rate(1, user_currencies)

                await self.send_to_clients(f"Server:\n{(result)}")
            else:
                await self.send_to_clients(f"{ws.name}: {message}")


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


def parse_argv(argv):
    logger.debug(argv)

    days = None
    user_currencies = []

    if len(argv) > 1:
        days = int(argv[1])
        logger.info(f"How many days user want to get exchange rates: {days} days")

        if days >= 10:
            logger.info(f"Maximum days is 10 days")
            days = 10
            logger.info(f"User's request changed to {days} days")

    if len(argv) > 2:
        user_currencies = argv[2:]
        logger.info(f"User currencies: {user_currencies}")

    return days, user_currencies


async def run_server():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


async def main():
    days, user_currencies = parse_argv(sys.argv)

    if days:
        exchange_rate = await get_exchange_rate(days, user_currencies)
        pprint(exchange_rate)
    else:
        await run_server()


if __name__ == "__main__":
    logger = logging.getLogger("pylog")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s - %(funcName)20s(%(lineno)3d) - %(levelname)5s - %(message)s"
    )

    path_logs = BASE_DIR / LOG_FILE_NAME

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(formatter)

    logger.addHandler(ch)

    print('----- Start program "PythonWeb-Homework-05" -----')

    asyncio.run(main())

    print("----- Finish -----")
