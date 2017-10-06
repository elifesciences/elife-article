import unittest
import os
import re
import json

from elifearticle import parse

# Test settings to read in test data
TEST_BASE_PATH = os.path.dirname(os.path.abspath(__file__)) + os.sep
XLS_PATH = TEST_BASE_PATH + "test_data" + os.sep

class TestParseDeep(unittest.TestCase):

    def test_parse_article_02935_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'elife-02935-v2.xml')
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, '10.7554/eLife.02935')
        self.assertEqual(article_object.journal_issn, '2050-084X')
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
                         "{'date_type': u'pub', 'day': u'01', 'year': u'2014', 'date': u'time.struct_time(tm_year=2014, tm_mon=10, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=2, tm_yday=274, tm_isdst=0)', 'month': u'10', 'publication_format': u'electronic'}")
        # datasets
        self.assertEqual(len(article_object.datasets), 2)
        self.assertEqual(article_object.datasets[0].accession_id, 'EGAS00001000968')
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
        # self_uri_list
        self.assertEqual(len(article_object.self_uri_list), 1)
        self.assertIsNotNone(article_object.get_self_uri('pdf'))
        self.assertEqual(article_object.get_self_uri('pdf').xlink_href, 'elife-02935-v2.pdf')
        # version
        self.assertEqual(article_object.version, 2)
        # publisher_name
        self.assertEqual(article_object.publisher_name, 'eLife Sciences Publications, Ltd')


    def test_parse_article_02935_compare_fixtures(self):
        "test by comparing data with test fixtures"
        with open(os.path.join(XLS_PATH, 'fixtures', '02935', 'article_json.txt'), 'rb') as fp:
            article_json = json.loads(fp.read())
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'elife-02935-v2.xml')
        self.assertEqual(article_object.pretty(), article_json)


    def test_parse_article_00666_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'elife-00666.xml')
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, '10.7554/eLife.00666')
        self.assertEqual(article_object.journal_issn, '2050-084X')
        # count contributors
        self.assertEqual(len(article_object.contributors), 14)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.contrib_type == 'author']), 4)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.contrib_type == 'on-behalf-of']), 1)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.contrib_type == 'author non-byline']), 9)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.collab is not None]), 3)
        # first contributor has a suffix
        self.assertEqual(article_object.contributors[0].suffix, 'Jnr')
        # ethics - not parsed yet
        self.assertEqual(len(article_object.ethics), 0)
        # compare dates
        self.assertEqual(unicode(article_object.dates.get('received')),
                         "{'date': u'time.struct_time(tm_year=2016, tm_mon=3, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=61, tm_isdst=0)', 'date_type': u'received'}")
        self.assertEqual(unicode(article_object.dates.get('accepted')),
                         "{'date': u'time.struct_time(tm_year=2016, tm_mon=4, tm_mday=1, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=4, tm_yday=92, tm_isdst=0)', 'date_type': u'accepted'}")
        self.assertEqual(unicode(article_object.dates.get('publication')),
                         "{'date_type': u'publication', 'day': u'25', 'year': u'2016', 'date': u'time.struct_time(tm_year=2016, tm_mon=4, tm_mday=25, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=0, tm_yday=116, tm_isdst=0)', 'month': u'04', 'publication_format': u'electronic'}")
        # datasets
        self.assertEqual(len(article_object.datasets), 3)
        self.assertEqual(len(article_object.get_datasets('datasets')), 1)
        self.assertEqual(len(article_object.get_datasets('prev_published_datasets')), 2)
        self.assertEqual(len(article_object.datasets[0].authors), 2)
        self.assertEqual(article_object.datasets[0].dataset_type, 'datasets')
        self.assertEqual(article_object.datasets[0].year, '2016')
        self.assertEqual(article_object.datasets[0].title, 'xml-mapping')
        self.assertEqual(article_object.datasets[0].comment, 'Publicly available on GitHub')
        self.assertEqual(article_object.datasets[0].uri, 'https://github.com/elifesciences/XML-mapping/blob/master/elife-00666.xml')
        self.assertEqual(article_object.datasets[2].doi, '10.5061/dryad.cv323')
        # related_articles
        self.assertEqual(len(article_object.related_articles), 0)
        # funding
        self.assertEqual(len(article_object.funding_awards), 2)
        # keywords
        self.assertEqual(len(article_object.author_keywords), 4)
        # categories
        self.assertEqual(len(article_object.article_categories), 2)
        # research organism
        self.assertEqual(len(article_object.research_organisms), 2)
        # components
        self.assertEqual(len(article_object.component_list), 39)
        # component id examples
        self.assertEqual(article_object.component_list[0].id, None)
        self.assertEqual(article_object.component_list[2].id, 'table1')
        # component type examples
        self.assertEqual(article_object.component_list[0].type, 'abstract')
        self.assertEqual(article_object.component_list[2].type, 'table-wrap')
        self.assertEqual(article_object.component_list[5].type, 'supplementary-material')
        self.assertEqual(article_object.component_list[9].type, 'fig')
        self.assertEqual(article_object.component_list[13].type, 'media')
        self.assertEqual(article_object.component_list[15].type, 'supplementary-material')
        self.assertEqual(article_object.component_list[19].type, 'boxed-text')
        self.assertEqual(article_object.component_list[22].type, 'supplementary-material')
        self.assertEqual(article_object.component_list[34].type, 'sub-article')
        self.assertEqual(article_object.component_list[35].type, 'sub-article')
        # component asset examples
        self.assertEqual(article_object.component_list[0].asset, None)
        self.assertEqual(article_object.component_list[2].asset, None)
        self.assertEqual(article_object.component_list[5].asset, 'data')
        self.assertEqual(article_object.component_list[9].asset, 'figsupp')
        self.assertEqual(article_object.component_list[13].asset, 'media')
        self.assertEqual(article_object.component_list[15].asset, 'code')
        self.assertEqual(article_object.component_list[19].asset, None)
        self.assertEqual(article_object.component_list[22].asset, 'supp')
        self.assertEqual(article_object.component_list[34].asset, 'dec')
        self.assertEqual(article_object.component_list[35].asset, 'resp')
        # refs
        self.assertEqual(len(article_object.ref_list), 54)

    def test_parse_article_cstp77_simple(self):
        "some simple comparisons and count list items"
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'cstp77-jats.xml')
        # list of individual comparisons of interest
        self.assertEqual(article_object.doi, "10.5334/cstp.77")
        self.assertEqual(article_object.journal_issn, '2057-4991')
        self.assertEqual(article_object.journal_title, "Citizen Science: Theory and Practice")
        # count contributors
        self.assertEqual(len(article_object.contributors), 4)
        self.assertEqual(len([c for c in article_object.contributors
                              if c.contrib_type == 'author']), 4)

        # compare dates
        self.assertEqual(unicode(article_object.dates.get('received')),
                         "{'date': u'time.struct_time(tm_year=2016, tm_mon=8, tm_mday=11, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=3, tm_yday=224, tm_isdst=0)', 'date_type': u'received'}")
        self.assertEqual(unicode(article_object.dates.get('accepted')),
                         "{'date': u'time.struct_time(tm_year=2017, tm_mon=3, tm_mday=28, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=87, tm_isdst=0)', 'date_type': u'accepted'}")
        self.assertEqual(unicode(article_object.dates.get('pub')),
                         "{'date_type': u'pub', 'day': u'04', 'year': u'2017', 'date': u'time.struct_time(tm_year=2017, tm_mon=7, tm_mday=4, tm_hour=0, tm_min=0, tm_sec=0, tm_wday=1, tm_yday=185, tm_isdst=0)', 'month': u'07', 'publication_format': u'electronic'}")
        # keywords
        self.assertEqual(len(article_object.author_keywords), 4)
        # refs
        self.assertEqual(len(article_object.ref_list), 36)
        # publisher_name
        self.assertEqual(article_object.publisher_name, 'Ubiquity Press')

    def test_parse_article_cstp77_compare_fixtures(self):
        "test by comparing data with test fixtures"
        with open(os.path.join(XLS_PATH, 'fixtures', 'cstp77', 'cstp77_article_json.txt'), 'rb') as fp:
            article_json = json.loads(fp.read())
        article_object, error_count = parse.build_article_from_xml(XLS_PATH + 'cstp77-jats.xml')
        self.assertEqual(article_object.pretty(), article_json)
