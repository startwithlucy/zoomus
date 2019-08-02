"""Zoom.us REST API Python Client"""

from zoomus import util
from zoomus.components import base


class MeetingComponent(base.BaseComponent):

    def list(self, **kwargs):
        util.require_keys(kwargs, 'user_id')

        return self.get_request(f"users/{kwargs['user_id']}/meetings", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, 'user_id')

        if 'start_time' in kwargs:
            kwargs['start_time'] = util.date_to_str(kwargs['start_time'])

        return self.post_request(f"users/{kwargs['user_id']}/meetings", data=kwargs)

    def retrieve(self, **kwargs):
        util.require_keys(kwargs, 'id')

        return self.get_request(f"meetings/{kwargs['id']}", params=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, 'id')

        params = {}
        if 'ocurrence_id' in kwargs:
            params['ocurrence_id'] = kwargs.pop('ocurrence_id')

        return self.patch_request(f"meetings/{kwargs['id']}", params=params, data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, 'id')

        return self.delete_request(f"meetings/{kwargs['id']}", params=kwargs)

    def invitation(self, **kwargs):
        util.require_keys(kwargs, 'id')

        return self.get_request(f"meetings/{kwargs['id']}/invitation")
