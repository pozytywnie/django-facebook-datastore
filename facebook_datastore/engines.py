# -*- coding: utf-8 -*-
import copy
import threading


class BaseThreadedEngine(object):
    def __init__(self, facebook_user):
        super(BaseThreadedEngine, self).__init__()
        self.facebook_user = copy.deepcopy(facebook_user)

    def should_run(self):
        return True

    def run(self):
        if self.should_run():
            # http://stackoverflow.com/a/660974
            thread = threading.Thread(target=self.perform)
            thread.start()

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
