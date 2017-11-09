import unittest
import re
import os
import time
from elifearticle import utils

class TestUtils(unittest.TestCase):

    def setUp(self):
        pass

    def test_repl(self):
        string = "&#x2022;"
        m = re.match(r"&#x(....);", string)
        self.assertEqual(utils.repl(m), u"\u2022")

    def test_entity_to_unicode(self):
        self.passes = []
        self.passes.append(('N-terminal &#x03B1;-helix into the heterodimer interface',
                           u'N-terminal \u03b1-helix into the heterodimer interface'))

        self.passes.append(('N-terminal &alpha;-helix into the heterodimer interface',
                           u'N-terminal \u03b1-helix into the heterodimer interface'))

        self.passes.append(('&#x00A0; &#x00C5; &#x00D7; &#x00EF; &#x0394; &#x03B1; &#x03B2; &#x03B3; &#x03BA; &#x03BB; &#x2212; &#x223C; &alpha; &amp; &beta; &epsilon; &iuml; &ldquo; &ordm; &rdquo;',
                           u'\xa0 \xc5 \xd7 \xef \u0394 \u03b1 \u03b2 \u03b3 \u03ba \u03bb \u2212 \u223c \u03b1 &amp; \u03b2 \u03b5 \xcf " \xba "'))

        for string_input, string_output in self.passes:
            self.assertEqual(utils.entity_to_unicode(
                string_input), string_output)

    def test_remove_tag(self):
        self.assertEqual(utils.remove_tag("i", "<i>test</i>"), "test")
        self.assertEqual(utils.remove_tag("i", None), None)

    def test_replace_tags(self):
        self.assertEqual(utils.replace_tags("<i>"), "<italic>")

    def test_version_from_xml_filename(self):
        self.assertEqual(utils.version_from_xml_filename(None), None)
        self.assertEqual(utils.version_from_xml_filename("elife-00666.xml"), None)
        self.assertEqual(utils.version_from_xml_filename("elife-02935-v2.xml"), 2)
        self.assertEqual(utils.version_from_xml_filename(os.path.join("test-folder", "elife-02935-v2.xml")), 2)
        self.assertEqual(utils.version_from_xml_filename("bmjopen-4-e003269.xml"), None)

    def test_calculate_journal_volume(self):
        "for test coverage"
        self.assertEqual(utils.calculate_journal_volume(None, None), None)
        pub_date = time.strptime("2017-01-01", "%Y-%m-%d")
        self.assertEqual(utils.calculate_journal_volume(pub_date, 2017), "1")
        self.assertEqual(utils.calculate_journal_volume(pub_date, None), None)

    def test_get_last_commit_to_master(self):
        self.assertIsNotNone(utils.get_last_commit_to_master())

if __name__ == '__main__':
    unittest.main()
