import os,sys
import unittest

ROOT_PATH = os.path.dirname(__file__)
sys.path.append(os.path.join(ROOT_PATH, '..'))


class TestPageScraper(unittest.TestCase):

    def test_parse_event_text(self):

        event_url ='https://www.whatsonincapetown.com/post/antarctica-2020-dr-roger-melvill/'

        # page_content =

