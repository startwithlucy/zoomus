"""Zoom.us REST API Python Client -- Recording component"""

from zoomus import util
from zoomus.components import base


class RecordingComponent(base.BaseComponent):
    """Component dealing with all recording related matters"""

    def list(self, **kwargs):
        util.require_keys(kwargs, 'user_id')

        start = kwargs.pop('start', None)
        if start:
            kwargs['from'] = util.date_to_str(start)

        end = kwargs.pop('end', None)
        if end:
            kwargs['to'] = util.date_to_str(end)

        return self.get_request(
            f"users/{kwargs['user_id']}/recordings",
            params=kwargs
        )

    def retrieve(self, **kwargs):
        util.require_keys(kwargs, 'meeting_id')

        return self.get_request(f"meetings/{kwargs['meeting_id']}/recordings", params=kwargs)

    def delete(self, **kwargs):
        util.require_keys(kwargs, 'meeting_id')

        return self.delete_request(f"meetings/{kwargs['meeting_id']}/recordings", params=kwargs)
