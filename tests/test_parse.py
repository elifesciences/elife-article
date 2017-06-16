import unittest
import os
import re

from elifearticle import parse

# Test settings to read in test data
TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
XLS_PATH = TEST_BASE_PATH + "test_data" + os.sep

class TestParseXml(unittest.TestCase):

    def setUp(self):
        self.passes = []
        self.passes.append(os.path.join(XLS_PATH, 'elife-02935-v2.xml'))
        self.passes.append(os.path.join(XLS_PATH, 'elife-04637-v2.xml'))
        self.passes.append(os.path.join(XLS_PATH, 'elife-15743-v1.xml'))
        self.passes.append(os.path.join(XLS_PATH, 'elife-02043-v2.xml'))
        self.passes.append(os.path.join(XLS_PATH, 'elife-14003.xml'))

    def test_parse(self):
        articles = parse.build_articles_from_article_xmls(self.passes)
        self.assertEqual(len(articles), 5)
