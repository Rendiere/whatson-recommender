from urllib.request import Request, urlopen
import pandas as pd

from bs4 import BeautifulSoup
from selenium import webdriver


class EventScraper():

    def __init__(self):
        self.events_df = pd.DataFrame(
            columns=['title', 'date_range', 'price', 'content-text', 'venue', 'time', 'three_words'])
        self.base_url = 'https://www.whatsonincapetown.com/category/2018'
        self.id = 1

    def run(self):

        for month in ['january', 'february']:
            # Construct the page url
            page_url = f'{self.base_url}/events-in-{month}-2018/'

            req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})
            # Gather the page content
            content = urlopen(req).read()

            # Use BS to parse the page content
            soup = BeautifulSoup(content, 'html.parser')

            events = soup.findAll('article')

            idx = 0
            for event in events:

                self.events_df.iloc[idx] = self.extract_event_content(event)

    def extract_event_content(self, event):

        title = event.fin


if __name__ == "__main__":
    EventScraper().run()
