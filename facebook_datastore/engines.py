# -*- coding: utf-8 -*-
import isodate
import logging

from django.contrib.auth.models import User
from facebook_datastore import models
from facebook_datastore import parser
import facepy

logger = logging.getLogger(__name__)


class BaseEngine(object):
    """
    TODO - handle 500
    """
    def __init__(self, facebook_user):
        super(BaseEngine, self).__init__()
        self.facebook_user = facebook_user

    def should_run(self):
        return True

    def run(self):
        if self.should_run():
            self.perform()

    def perform(self):
        data = self.fetch()
        data = self.parse(data)
        self.save(data)

    def fetch(self):
        raise NotImplementedError

    def parse(self, data):
        raise NotImplementedError

    def save(self, data):
        raise NotImplementedError


class UserProfileEngine(BaseEngine):
    def should_run(self):
        facebook_id = self.facebook_user.user_id
        return not models.FacebookUserProfile.objects.filter(
            facebook_id=facebook_id).exists()

    def fetch(self):
        graph = facepy.GraphAPI(self.facebook_user.access_token)
        return graph.get('me')

    def parse(self, data):
        parser_instance = parser.FacebookDataParser(data=data)
        return parser_instance.run()

    def save(self, data):
        profile = models.FacebookUserProfile.objects.create_or_update(data)
        try:
            user = User.objects.get(id=self.facebook_user.id)
        except User.DoesNotExist:
            message = "UserProfileEngine missing user for facebook_user %d"
            logger.warning(message % self.facebook_user.id)
        else:
            profile.user = user
        profile.save()


class UserLikeEngine(BaseEngine):
    def fetch(self):
        graph = facepy.GraphAPI(self.facebook_user.access_token)
        likes = []

        response = graph.get('me/likes', True)
        for page in response:
            if 'data' in page and page['data']:
                likes += page['data']
        return likes

    def parse(self, data):
        for like in data:
            like['id'] = int(like['id'])
            like['created_time'] = isodate.parse_datetime(like['created_time'])
            yield like

    def get_user(self):
        try:
            return User.objects.get(id=self.facebook_user.id)
        except User.DoesNotExist:
            message = "UserProfileEngine missing user for facebook_user %d"
            logger.warning(message % self.facebook_user.id)
            raise

    def save(self, data):
        user = self.get_user()
        processed_likes = []
        for like in data:
            user_like = models.FacebookUserLike.objects
            defaults = {'name': like['name'],
                        'category': like['category'],
                        'created_time': like['created_time']}

            like, _ = user_like.get_or_create(user=user,
                                              facebook_id=like['id'],
                                              defaults=defaults)
            processed_likes.append(like.id)

        removed_likes = models.FacebookUserLike.objects.filter(user=user)
        removed_likes = removed_likes.exclude(id__in=processed_likes)
        removed_likes.delete()


ENGINES_ENABLED = [UserProfileEngine, UserLikeEngine]
