import requests
from bs4 import BeautifulSoup
import re
from globals import Globals


class WebScraper:
    def __init__(self):
        self.url = Globals.url

    def scrape(self):
        page = requests.get(self.url).text

        # Deleting HTML comments <!-- -->
        page = re.sub(r'<!.*?->', '', page)

        soup = BeautifulSoup(page, 'html.parser')

        tbody = soup.tbody
        trs = tbody.contents

        scraped_data = []

        for tr in trs:
            parts = tr.contents[1].text.split('(')  # 'Bitcoin(BTC)'
            name = parts[0]  # 'Bitcoin'
            symbol = parts[1].replace(')', '')  # 'BTC'
            price = tr.contents[2].text
            hour_dynamics = tr.contents[3].text
            day_dynamics = tr.contents[4].text
            week_dynamics = tr.contents[5].text
            market_cap = tr.contents[6].text
            day_volume = tr.contents[7].text

            scraped_data.append({
                "name": name,
                "symbol": symbol,
                "price": price,
                "hour_dynamics": hour_dynamics,
                "day_dynamics": day_dynamics,
                "week_dynamics": week_dynamics,
                "market_cap": market_cap,
                "day_volume": day_volume
            })

        return scraped_data
