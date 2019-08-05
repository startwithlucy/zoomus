import requests

__all__ = ['ZoomException']


class ZoomException(requests.RequestException):
    def __init__(self, response):
        error_details = response.json()
        message = error_details['message']

        super().__init__(message, response=response)
