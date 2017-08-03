import unittest
import os
import re

from elifearticle import parse

# Test settings to read in test data
TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
XLS_PATH = TEST_BASE_PATH + "test_data" + os.sep

class TestParseBuildRefList(unittest.TestCase):

    def setUp(self):
        pass

    def test_build_ref_list_666(self):
        xml_files = [os.path.join(XLS_PATH, 'elife-00666.xml')]
        articles = parse.build_articles_from_article_xmls(xml_files)
        article = articles[0]

        # Now check various details as desired
        # ref bib11 all authors
        self.assertEqual(len(article.ref_list[10].authors), 4)
        # ref bib11 authors of type author
        self.assertEqual(len([c for c in article.ref_list[10].authors
                              if c.get('group-type') == 'author']), 2)
        # ref bib11 authors of type editor
        self.assertEqual(len([c for c in article.ref_list[10].authors
                              if c.get('group-type') == 'editor']), 2)
        # ref bib46 author is a collab
        self.assertEqual(article.ref_list[45].authors[0].get('collab'),
                         'The <italic>Shigella</italic> Genome Sequencing Consortium')
