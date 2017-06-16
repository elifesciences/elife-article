import unittest
import os
import re

from elifearticle import parse

# Test settings to read in test data
TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
XLS_PATH = TEST_BASE_PATH + "test_data" + os.sep

class TestParseDeep(unittest.TestCase):

    def test_parse_article_02935_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'elife-02935-v2.xml')
        # list of individual comparisons of interest
        self.assertIsNotNone(article_object.doi)
        # count contributors
        self.assertEqual(len(article_object.contributors), 180)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.contrib_type == 'author']), 53)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.contrib_type == 'author non-byline']), 127)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.collab is not None]), 3)
        # ethics - not parsed yet
        self.assertEqual(len(article_object.ethics), 0)
        # compare dates
        self.assertEqual(unicode(article_object.dates.get('received')),
                         "{'date': u'time.struct_time(tm_year=2014, tm_mon=3, tm_mday=28, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=87, tm_isdst=0)', 'date_type': u'received'}")
        self.assertEqual(unicode(article_object.dates.get('accepted')),
                         "{'date': u'time.struct_time(tm_year=2014, tm_mon=9, tm_mday=26, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=269, tm_isdst=0)', 'date_type': u'accepted'}")
        self.assertEqual(unicode(article_object.dates.get('pub')),
                         "{'date': u'time.struct_time(tm_year=2014, tm_mon=10, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=274, tm_isdst=0)', 'date_type': u'pub'}")
        # datasets - not parsed yet
        self.assertEqual(len(article_object.datasets), 0)
        # related_articles
        self.assertEqual(len(article_object.related_articles), 0)
        # funding
        self.assertEqual(len(article_object.funding_awards), 16)
        # keywords
        self.assertEqual(len(article_object.author_keywords), 6)
        # categories
        self.assertEqual(len(article_object.article_categories), 1)
        # research organism
        self.assertEqual(len(article_object.research_organisms), 1)
        # components
        self.assertEqual(len(article_object.component_list), 28)
        # refs
        self.assertEqual(len(article_object.ref_list), 59)


    def test_parse_article_02935_compare_fixtures(self):
        "test by comparing data with test fixtures"
        with open(os.path.join(XLS_PATH, 'fixtures', '02935', 'article_unicode.txt'), 'rb') as fp:
            article_unicode = fp.read()
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'elife-02935-v2.xml')
        self.assertEqual(unicode(article_object), article_unicode)
