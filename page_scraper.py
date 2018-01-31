import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from urllib.request import Request, urlopen


class EventScraper():

    def __init__(self):
        self.events_df = pd.DataFrame(
            columns=['Title', 'Date-range', 'Cost', 'event-text', 'Venue', 'Time'])
        self.base_url = 'https://www.whatsonincapetown.com/category/2018'
        self.id = 1

    def get_page_content(self, page_url, extract=None):
        """
        Get the content of a page by requesting and parsing the URL
        Optionally only return a certain part of the page using the extract param

        For example adding extract='body' will only return the page body

        :param page_url:
        :param extract:
        :return:
        """
        # Make a request with some spoof header ;)
        req = Request(page_url, headers={'User-Agent': 'Mozilla/5.0'})

        # Gather the page content
        content = urlopen(req).read()

        soup = BeautifulSoup(content, 'html.parser')

        if extract:
            return soup.find(extract)

        return soup

    def run(self):

        for month in ['january', 'february']:
            # Construct the page url
            page_url = f'{self.base_url}/events-in-{month}-2018/'

            # Use BS to parse the page content
            soup = self.get_page_content(page_url)

            # Get all the articles on the page
            # These are only thumbnails though - we'd need to click through to get the real content
            event = soup.findAll('article')

            # For each event, extract the information and store in events_df
            events_data = []
            for event in event:
                events_data.append(self.extract_event_info(event))

            self.events_df = pd.DataFrame(events_data)

            print(self.events_df)
            exit()

    def extract_event_info(self, event):

        content = self.get_events_data(event)

        title = content.find('h1', {'class': 'post-title'}).getText().strip()

        print('Extracting : ',title)

        # Get a dictionary with Cost, Venue and Time
        event_info = self.parse_event_text(content.find_all('p'))

        # Get the title
        event_info['Title'] = title

        event_info['Date-range'] = content.find('div', {'class': 'event_date'}).getText()

        return event_info



    def get_events_data(self, event_thumb):
        """
        Click through on the event url from the thumbnail
        and return the full event HTML data

        :param event_thumb:
        :return:
        """
        event_url = event_thumb.find('a', {'class': 'image-link'})['href']

        event_content = self.get_page_content(event_url, extract='article')

        return event_content

    def parse_event_text(self, p_list):
        """
        From a list of p-tags, get the one which contains the event text and
        return that text
        :param p_list:
        :return:

        """

        event_info = {
            'event_text': [],
            'Venue': None,
            'Time': None,
            'Cost': None
        }

        keywords = ['Venue', 'Time', 'Cost']
        # For each paragraph tag
        for p in p_list:
            # Skip the loop back link
            if p.find('a', {'title': 'WHAT ELSE IS ON in CAPE TOWN SOUTH'}):
                continue

            # Get the inner text
            text = p.getText()

            # Get the separate words
            words = text.replace('\n', ' ').strip().split(' ')

            # Count how many keywords are in this body of text.
            keyword_count = sum([1 for w in keywords if f'{w}:' in words])

            # If keywords are found, put their value into the event_info dictionary
            if keyword_count > 0:
                lines = text.split('\n')

                if len(lines) > 0:

                    for keyword in keywords:
                        [value] = [line.replace(f'{keyword}: ', '') for line in lines if keyword in line]
                        event_info[keyword] = value
                else:
                    print('Couldnt get info')
                    print('text = ',text)

            else:
                event_info['event_text'].append(text)

        if not event_info['event_text']:
            raise UserWarning('No event text found!!')

        return event_info


if __name__ == "__main__":
    EventScraper().run()
