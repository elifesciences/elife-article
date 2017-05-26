import unittest
from elifearticle import article as ea

class TestArticle(unittest.TestCase):

    def setUp(self):
        self.article = ea.Article()

    def test_article_init(self):
        self.assertEqual(self.article.articleType, 'research-article')

    def test_add_contributor(self):
        contributor = None
        self.article.add_contributor(contributor)
        self.assertEqual(len(self.article.contributors), 1)

if __name__ == '__main__':
    unittest.main()
