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
            name_line, price_line, hour_dynamics_line, day_dynamics_line = tr.contents[1:5]

            name = name_line.span.string
            price = price_line.div.string
            hour_dynamics = hour_dynamics_line.span.string
            day_dynamics = day_dynamics_line.span.string

            scraped_data.append({
                "name": name,
                "price": price,
                "hour_dynamics": hour_dynamics,
                "day_dynamics": day_dynamics
            })

        return scraped_data
