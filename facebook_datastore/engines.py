# -*- coding: utf-8 -*-
import copy
import json
import logging
import threading

from django.contrib.auth.models import User
from django import db
from facebook_datastore import models
from facebook_datastore import parser
import facepy

logger = logging.getLogger(__name__)


class BaseThreadedEngine(object):
    """
    TODO - handle 500
    """
    Thread = threading.Thread

    def __init__(self, facebook_user):
        super(BaseThreadedEngine, self).__init__()
        self.facebook_user = copy.deepcopy(facebook_user)

    def should_run(self):
        return True

    def run(self):
        if self.should_run():
            try:
                # http://stackoverflow.com/a/660974
                thread = threading.Thread(target=self.perform)
                thread.start()
            finally:
                db.close_connection()

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


class UserProfileEngine(BaseThreadedEngine):
    def should_run(self):
        facebook_id = self.facebook_user.user_id
        return models.FacebookUserProfile.objects.filter(
            facebook_id=facebook_id).exists()

    def fetch(self):
        graph = facepy.GraphAPI(self.facebook_user.access_token)
        data = graph.get('me')
        return json.loads(data)

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
