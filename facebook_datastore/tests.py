from django.test import TestCase

from facebook_datastore import engines


class TestBaseThreadedEngine(TestCase):
    def test_basic_usage(self):
        dummy_user = object()
        engine = engines.BaseThreadedEngine(dummy_user)
        self.assertRaises(NotImplementedError, engine.run())
