import unittest
import pandas as pd

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen


class TestPageScraper(unittest.TestCase):

    def test_parse_event_text(self):

        event_url ='https://www.whatsonincapetown.com/post/antarctica-2020-dr-roger-melvill/'


