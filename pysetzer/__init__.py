#  /$$$$$$$           /$$$$$$            /$$
# | $$__  $$         /$$__  $$          | $$
# | $$  \ $$/$$   /$| $$  \__/ /$$$$$$ /$$$$$$ /$$$$$$$$ /$$$$$$  /$$$$$$
# | $$$$$$$| $$  | $|  $$$$$$ /$$__  $|_  $$_/|____ /$$//$$__  $$/$$__  $$
# | $$____/| $$  | $$\____  $| $$$$$$$$ | $$     /$$$$/| $$$$$$$| $$  \__/
# | $$     | $$  | $$/$$  \ $| $$_____/ | $$ /$$/$$__/ | $$_____| $$
# | $$     |  $$$$$$|  $$$$$$|  $$$$$$$ |  $$$$/$$$$$$$|  $$$$$$| $$
# |__/      \____  $$\______/ \_______/  \___/|________/\_______|__/
#           /$$  | $$
#          |  $$$$$$/
#           \______/

"""
PySetzer
~~~~~~~~~~~~~~~~~~~~~

:copyright: (c) 2020 by monolithos
"""

import logging
import datetime
from typing import List

import requests
from decimal import Decimal

logger = logging.getLogger(__name__)


class PySetzer:
    py_setzer_backend_host: str = "http://localhost:8888/"
    timedelta: datetime.timedelta

    def __init__(self, host: str, timedelta=datetime.timedelta(hours=3)):
        self.py_setzer_backend_host = host+"v1/setzer/" if host.endswith("/") else host + "/v1/setzer/"
        self.timedelta = timedelta

    def price(self, first_symbol: str, second_symbol: str,
              round_: int = 10, inverse: bool = False, *args, **kwargs) -> Decimal:
        url = self.py_setzer_backend_host + f"price?first_token={first_symbol}&second_token={second_symbol}&round={round_}"
        response = requests.get(url)

        if response.ok:
            data = response.json()['result']

            if datetime.datetime.utcnow() - datetime.datetime.fromtimestamp(data['date']) > self.timedelta:
                logger.warning(f"the price for {first_symbol}/{second_symbol} update date is too "
                               f"old (date update = {data['date']}). The price ({data['price']}) may not be accurate.")
            return Decimal(data['price']) if not inverse else round(Decimal('1') / Decimal(data['price']), round_)

        else:
            logger.error(
                f"Bad response for url '{url}'. \n response: {response.json()}, status: {response.status_code}")
            response.raise_for_status()

    def pairs(self) -> List[dict]:
        url = self.py_setzer_backend_host + f"pairs"
        response = requests.get(url)

        if response.ok:
            return response.json()['result']

        else:
            logger.error(
                f"Bad response for url '{url}'. \n response: {response.json()}, status: {response.status_code}")
            response.raise_for_status()


__all__ = [
    'PySetzer'
]
