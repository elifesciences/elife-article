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
        # ref bib1 details
        self.assertEqual(article.ref_list[0].id, 'bib1')
        self.assertEqual(article.ref_list[0].article_title, 'TIP47 is a key effector for Rab9 localization')
        self.assertEqual(article.ref_list[0].source, 'The Journal of Cell Biology')
        self.assertEqual(article.ref_list[0].volume, '173')
        # note: no test for issue attribute yet
        self.assertEqual(article.ref_list[0].fpage, '917')
        self.assertEqual(article.ref_list[0].lpage, '926')
        self.assertEqual(article.ref_list[0].doi, '10.1083/jcb.200510010')
        self.assertEqual(article.ref_list[0].year, '2006')
        self.assertEqual(article.ref_list[0].pmid, '16769818')
        # ref bib2 details
        self.assertEqual(article.ref_list[1].uri, 'https://cran.r-project.org/web/packages/lme4/index.html')
        self.assertEqual(article.ref_list[1].version, '1.1-12')
        self.assertEqual(article.ref_list[1].data_title, 'Lme4: Linear Mixed-Effects Models Using Eigen and S4')
        # ref bib7 details
        self.assertEqual(article.ref_list[6].publisher_loc, 'Cambridge, UK')
        self.assertEqual(article.ref_list[6].publisher_name, 'Global Phasing Ltd')
        # ref bib10 details
        self.assertEqual(article.ref_list[9].edition, '2')
        # ref bib11 details
        self.assertEqual(article.ref_list[10].publication_type, 'book')
        self.assertEqual(article.ref_list[10].chapter_title, 'Two rules of speciation')
        # ref bib11 all authors
        self.assertEqual(len(article.ref_list[10].authors), 4)
        # ref bib11 authors of type author
        self.assertEqual(len([c for c in article.ref_list[10].authors
                              if c.get('group-type') == 'author']), 2)
        # ref bib11 authors of type editor
        self.assertEqual(len([c for c in article.ref_list[10].authors
                              if c.get('group-type') == 'editor']), 2)
        # ref bib13 details
        self.assertEqual(article.ref_list[12].isbn, '9781474130158')
        # ref bib15 details
        self.assertEqual(article.ref_list[14].publication_type, 'web')
        self.assertEqual(article.ref_list[14].date_in_citation, 'August 19, 2016')
        # ref bib24 details
        self.assertEqual(article.ref_list[23].conf_name, 'IEEE Conference on Computer Vision and Pattern Recognition (CVPR), 2010')
        # ref bib32 details
        self.assertEqual(article.ref_list[31].patent, 'US20100941530')
        self.assertEqual(article.ref_list[31].country, 'United States')
        # ref bib37 details
        self.assertEqual(article.ref_list[36].comment, 'In press')
        # ref bib40 details
        self.assertEqual(article.ref_list[39].year_iso_8601_date, '1993-09-09')
        self.assertEqual(article.ref_list[39].year_numeric, 1993)
        # ref bib46 author is a collab
        self.assertEqual(article.ref_list[45].authors[0].get('collab'),
                         'The <italic>Shigella</italic> Genome Sequencing Consortium')
        # ref bib51 details
        self.assertEqual(article.ref_list[50].elocation_id, 'e149')

