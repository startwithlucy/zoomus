"""Zoom.us REST API Python Client -- User component"""

from zoomus import util
from zoomus.components import base


class UserComponent(base.BaseComponent):
    def list(self, **kwargs):
        return self.get_request('/users', params=kwargs)

    def create(self, **kwargs):
        return self.post_request('/users', data=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, 'id')

        return self.patch_request(f"/users/{kwargs['id']}", data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, 'id')

        return self.delete_request(f"/users/{kwargs['id']}", params=kwargs)

    def retrieve(self, **kwargs):
        util.require_keys(kwargs, 'id')

        return self.get_request(f"/users/{kwargs['id']}", params=kwargs)
