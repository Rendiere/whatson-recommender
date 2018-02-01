import os,sys
import unittest
import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen

ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))


from page_scraper import EventScraper

class TestPageScraper(unittest.TestCase):

    def test_parse_event_text(self):

        event_url ='https://www.whatsonincapetown.com/post/antarctica-2020-dr-roger-melvill/'

        # page_content =

