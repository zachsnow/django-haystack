from django.test import TestCase
from mock import patch
from test_haystack.discovery.search_indexes import FooIndex

from haystack import connections
from haystack.utils.loading import UnifiedIndex


class ManualDiscoveryTestCase(TestCase):
    def test_discovery(self):
        new_index = UnifiedIndex()
        with patch.object(connections['default'], '_index', new=new_index):
            ui = connections['default'].get_unified_index()
            self.assertEqual(len(ui.get_indexed_models()), 5)

            ui.build(indexes=[FooIndex()])

            self.assertEqual(len(ui.get_indexed_models()), 1)

            ui.build(indexes=[])

            self.assertEqual(len(ui.get_indexed_models()), 0)


class AutomaticDiscoveryTestCase(TestCase):
    def test_discovery(self):
        new_index = UnifiedIndex()
        with patch.object(connections['default'], '_index', new=new_index):
            ui = connections['default'].get_unified_index()
            self.assertEqual(len(ui.get_indexed_models()), 5)

            # Test exclusions.
            ui.excluded_indexes = ['test_haystack.discovery.search_indexes.BarIndex']
            ui.build()

            self.assertEqual(len(ui.get_indexed_models()), 4)

            ui.excluded_indexes = ['test_haystack.discovery.search_indexes.BarIndex',
                                   'test_haystack.discovery.search_indexes.FooIndex']
            ui.build()

            self.assertEqual(len(ui.get_indexed_models()), 3)
