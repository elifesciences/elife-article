import unittest
import os
import re
from elifearticle import parse


class TestParseBuildDatasets(unittest.TestCase):

    def setUp(self):
        pass

    def test_datasets_uri_to_doi(self):
        "test converting uri to doi value"
        # based on a dataset in elife-01201-v1
        dataset_data = {'generated': [
            {'uri': 'http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?acc=GSE51740'},
            {'uri': 'http://dx.doi.org/10.5061/dryad.cv39v'},
        ]}
        datasets = parse.build_datasets(dataset_data)
        self.assertEqual(datasets[0].doi, None)
        self.assertEqual(datasets[1].doi, '10.5061/dryad.cv39v')
