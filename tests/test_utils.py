import unittest
import re
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

    def test_replace_tags(self):
        self.assertEqual(utils.replace_tags("<i>"), "<italic>")


if __name__ == '__main__':
    unittest.main()
