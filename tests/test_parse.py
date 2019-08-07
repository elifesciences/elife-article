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
        self.passes.append(os.path.join(XLS_PATH, 'elife-00666.xml'))
        self.passes.append(os.path.join(XLS_PATH, 'cstp77-jats.xml'))

    def test_parse(self):
        articles = parse.build_articles_from_article_xmls(self.passes)
        self.assertEqual(len(articles), 7)

    def test_parse_build_parts_default(self):
        "test parse build parts"

        def check_article(article):
            "function for repeatable article assertions for the two builds"
            self.assertNotEqual(article.abstract, '')
            self.assertNotEqual(article.elocation_id, '')
            self.assertGreater(len(article.article_categories), 0)
            self.assertGreater(len(article.component_list), 0)
            self.assertGreater(len(article.contributors), 0)
            self.assertGreater(len(article.funding_awards), 0)
            self.assertGreater(len(article.dates), 0)
            self.assertIsNotNone(article.get_date('received'))
            self.assertIsNotNone(article.is_poa)
            self.assertGreater(len(article.author_keywords), 0)
            self.assertIsNotNone(article.get_date('pub'))

        def check_article_15743(article):
            "function for repeatable article assertions for the two builds"
            self.assertGreater(len(article.related_articles), 0)

        #first, default build parts should build all parts
        article_xmls = [os.path.join(XLS_PATH, 'elife-02043-v2.xml')]
        article = parse.build_articles_from_article_xmls(article_xmls)[0]
        check_article(article)
        # also check building an article with a related article
        article_xmls = [os.path.join(XLS_PATH, 'elife-15743-v1.xml')]
        article = parse.build_articles_from_article_xmls(article_xmls)[0]
        check_article_15743(article)
        #second, set all the build parts and the result should be the same
        detail = 'full'
        build_parts = [
            'abstract', 'basic', 'categories', 'components', 'contributors', 'datasets', 'funding',
            'history', 'is_poa', 'keywords', 'license', 'pub_dates', 'references',
            'related_articles', 'research_organisms', 'volume', 'sub_articles']
        article_xmls = [os.path.join(XLS_PATH, 'elife-02043-v2.xml')]
        article = parse.build_articles_from_article_xmls(article_xmls, detail, build_parts)[0]
        check_article(article)
        # also check building an article with a related article
        article_xmls = [os.path.join(XLS_PATH, 'elife-15743-v1.xml')]
        article = parse.build_articles_from_article_xmls(article_xmls, detail, build_parts)[0]
        check_article_15743(article)


    def test_parse_build_parts_basic(self):
        "test building with very basic build parts"
        detail = 'brief'
        build_parts = ['basic']
        article_xmls = [os.path.join(XLS_PATH, 'elife-02043-v2.xml')]
        article = parse.build_articles_from_article_xmls(article_xmls, detail, build_parts)[0]
        # check the result
        # elocation_id will exist, but not other parts we check
        self.assertNotEqual(article.elocation_id, '')
        self.assertEqual(article.abstract, '')
        self.assertEqual(len(article.article_categories), 0)
        self.assertEqual(len(article.component_list), 0)
        self.assertEqual(len(article.contributors), 0)
        self.assertEqual(len(article.funding_awards), 0)
        self.assertEqual(article.dates, {})
        self.assertIsNone(article.get_date('received'))
        self.assertIsNone(article.is_poa)
        self.assertEqual(len(article.author_keywords), 0)
        self.assertIsNone(article.get_date('pub'))
        self.assertEqual(len(article.related_articles), 0)
        # also check building an article with a related article
        article_xmls = [os.path.join(XLS_PATH, 'elife-15743-v1.xml')]
        article = parse.build_articles_from_article_xmls(article_xmls, detail, build_parts)[0]
        self.assertEqual(len(article.related_articles), 0)
