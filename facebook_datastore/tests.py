from django.test import TestCase
import json
from os import path

from facebook_datastore import engines
from facebook_datastore import factories
from facebook_datastore import models


class TestBaseThreadedEngine(TestCase):
    def test_basic_usage(self):
        dummy_user = object()
        engine = engines.BaseThreadedEngine(dummy_user)
        self.assertRaises(NotImplementedError, engine.run())


class TestUserProfileEngine(TestCase):
    def setUp(self):
        with open(path.join(path.dirname(__file__), "test_data/test_data.json")) as data_file:
            self.raw_data = data_file.read()
        self.data = json.loads(self.raw_data)
        self.expected_facebook_id = 100002364688506
        self.facebook_user = factories.FacebookUserFactory(
            user_id=self.expected_facebook_id)

    def test_if_engine_creates_profile(self):
        test_data = self.data
        class UserProfileEngine(engines.UserProfileEngine):
            def fetch(self):
                return test_data

        engine = UserProfileEngine(self.facebook_user)
        engine.perform()

        profile = models.FacebookUserProfile.objects.get(
            facebook_id=self.expected_facebook_id)

        self.assertEqual(self.expected_facebook_id, profile.facebook_id)
        self.assertEqual(self.data['first_name'], profile.first_name)
        self.assertEqual(self.data['last_name'], profile.last_name)
        self.assertEqual('m', profile.gender)
        self.assertEqual(self.facebook_user.id, profile.user.id)


class TestUserLikeEngine(TestCase):
    def setUp(self):
        with open(path.join(path.dirname(__file__), "test_data/test_likes_data.json")) as data_file:
            self.raw_data = data_file.read()
        self.data = json.loads(self.raw_data)
        self.facebook_id = 100002364688506
        self.facebook_user = factories.FacebookUserFactory(
            user_id=self.facebook_id)

    def test_if_engine_creates_likes(self):
        test_data = self.data
        class UserLikeEngine(engines.UserLikeEngine):

            def fetch(self):
                return test_data

        engine = UserLikeEngine(self.facebook_user)
        engine.perform()
        likes = models.FacebookUserLike.objects.filter(user__id=self.facebook_user.id)
        self.assertEqual(3, likes.count())
        like = likes.get(name='DajeRade.com')
        self.assertEqual('Website', like.category)
