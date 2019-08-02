"""Zoom.us REST API Python Client"""

from zoomus import (
    components,
    util)


class ZoomClient(util.ApiClient):
    """Zoom.us REST API Python Client"""

    BASE_URI = 'https://api.zoom.us/v2'

    def __init__(self, api_key, api_secret, timeout=15):
        """Create a new Zoom client

        :param api_key: The Zooom.us API key
        :param api_secret: The Zoom.us API secret
        :param timeout: The time out to use for API requets
        """
        super().__init__(base_uri=self.BASE_URI, timeout=timeout)

        # Setup the config details
        self.config = {
            'api_key': api_key,
            'api_secret': api_secret,
            'token': util.generate_jwt(api_key, api_secret),
        }

        # Register all of the components
        self.components = {
            'meeting': components.meeting.MeetingComponent(
                base_uri=self.BASE_URI, config=self.config),
            'report': components.report.ReportComponent(
                base_uri=self.BASE_URI, config=self.config),
            'user': components.user.UserComponent(
                base_uri=self.BASE_URI, config=self.config),
            'webinar': components.webinar.WebinarComponent(
                base_uri=self.BASE_URI, config=self.config),
            'recording': components.recording.RecordingComponent(
                base_uri=self.BASE_URI, config=self.config)
        }

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def refresh_token(self):
        self.config['token'] = util.generate_jwt(
            self.config['api_key'],
            self.config['api_secret']),

    @property
    def api_key(self):
        """The Zoom.us api_key"""
        return self.config.get('api_key')

    @api_key.setter
    def api_key(self, value):
        """Set the api_key"""
        self.config['api_key'] = value
        self.refresh_token()

    @property
    def api_secret(self):
        """The Zoom.us api_secret"""
        return self.config.get('api_secret')

    @api_secret.setter
    def api_secret(self, value):
        """Set the api_secret"""
        self.config['api_secret'] = value
        self.refresh_token()

    @property
    def meeting(self):
        """Get the meeting component"""
        return self.components.get('meeting')

    @property
    def report(self):
        """Get the report component"""
        return self.components.get('report')

    @property
    def user(self):
        """Get the user component"""
        return self.components.get('user')

    @property
    def webinar(self):
        """Get the webinar component"""
        return self.components.get('webinar')

    @property
    def recording(self):
        """Get the recording component"""
        return self.components.get('recording')
