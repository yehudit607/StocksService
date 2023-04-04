from typing import Dict, Any
from bs4 import BeautifulSoup
import requests
from aiohttp import ClientSession


async def scrape_performance_data(stock_symbol: str, session: ClientSession) -> Dict[str, Any]:
    url = f"https://www.marketwatch.com/investing/stock/{stock_symbol}"
    async with session.get(url) as response:
        text = await response.text()
    soup = BeautifulSoup(text, "html.parser")

    performance_div = soup.find("div", class_="element element--table performance")

    if not performance_div:
        return {}

    performance_table = performance_div.find("table", class_="table table--primary no-heading c2")

    if not performance_table:
        return {}

    performance_data = {}
    for row in performance_table.find_all("tr", class_="table__row"):
        cells = row.find_all("td", class_="table__cell")
        key = cells[0].text.strip()
        value_container = cells[1].find("li", class_="content__item value ignore-color")

        if value_container:
            value_text = value_container.text.strip()
            performance_data[key] = value_text

    return performance_data

