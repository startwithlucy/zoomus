"""Zoom.us REST API Python Client -- Webinar component"""

from __future__ import absolute_import

from zoomus import util
from zoomus.components import base


class WebinarComponent(base.BaseComponent):
    """Component dealing with all webinar related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, 'user_id')

        return self.get_request(f"/users/{kwargs['user_id']}/webinars", params=kwargs)

    def create(self, **kwargs):
        util.require_keys(kwargs, 'user_id')

        return self.post_request(f"/users/{kwargs['user_id']}/webinars", data=kwargs)

    def update(self, **kwargs):
        util.require_keys(kwargs, 'meeting_id')

        params = {}
        if 'ocurrence_id' in kwargs:
            params['ocurrence_id'] = kwargs.pop('ocurrence_id')

        return self.patch_request(f"/webinars/{kwargs['meeting_id']}", params=params, data=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, 'meeting_id')

        return self.delete_request(f"/webinars/{kwargs['meeting_id']}", params=kwargs)
