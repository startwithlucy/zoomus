"""Utility classes and functions"""

import functools
import requests
import time
import jwt

from zoomus import exceptions

__all__ = ['ApiClient']


def handle_request_error(request_method):
    @functools.wraps(request_method)
    def inner(*args, **kwargs):
        response = request_method(*args, **kwargs)

        # zoom uses custom status codes above 600 to indicate errors
        # response.ok only checks between 400 and 600 so we need to do a manual check
        if response.status_code >= 400:
            raise exceptions.ZoomException(response)

        return response

    return inner


class ApiClient(object):
    """Simple wrapper for REST API requests"""

    def __init__(self, base_uri=None, timeout=15, **kwargs):
        """Setup a new API Client

        :param base_uri: The base URI to the API
        :param timeout: The timeout to use for requests
        :param kwargs: Any other attributes. These will be added as
                           attributes to the ApiClient object.
        """
        self.base_uri = base_uri
        self.timeout = timeout
        for k, v in kwargs.items():
            setattr(self, k, v)

    @property
    def timeout(self):
        """The timeout"""
        return self._timeout

    @timeout.setter
    def timeout(self, value):
        """The default timeout"""
        if value is not None:
            try:
                value = int(value)
            except ValueError:
                raise ValueError("timeout value must be an integer")
        self._timeout = value

    @property
    def base_uri(self):
        """The base_uri"""
        return self._base_uri

    @base_uri.setter
    def base_uri(self, value):
        """The default base_uri"""
        if value and value.endswith("/"):
            value = value[:-1]
        self._base_uri = value

    def url_for(self, endpoint):
        """Get the URL for the given endpoint

        :param endpoint: The endpoint
        :return: The full URL for the endpoint
        """
        if not endpoint.startswith("/"):
            endpoint = "/{}".format(endpoint)
        if endpoint.endswith("/"):
            endpoint = endpoint[:-1]
        return self.base_uri + endpoint

    @handle_request_error
    def get_request(self, endpoint, params=None, headers=None):
        """Helper function for GET requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param headers: request headers
        :return: The :class:``requests.Response`` object for this request
        """
        if headers is None:
            headers = {'Authorization': 'Bearer {}'.format(self.config.get('token'))}

        return requests.get(
            self.url_for(endpoint),
            params=params,
            headers=headers,
            timeout=self.timeout,
        )

    @handle_request_error
    def post_request(
            self, endpoint, params=None, data=None, headers=None, cookies=None):
        """Helper function for POST requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data as a dict to include with the POST
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        if headers is None:
            headers = {'Authorization': 'Bearer {}'.format(self.config.get('token'))}

        return requests.post(
            self.url_for(endpoint),
            params=params,
            json=data,
            headers=headers,
            cookies=cookies,
            timeout=self.timeout,
        )

    @handle_request_error
    def patch_request(
            self, endpoint, params=None, data=None, headers=None, cookies=None):
        """Helper function for PATCH requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data as a dict to include with the PATCH
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        if headers is None:
            headers = {'Authorization': 'Bearer {}'.format(self.config.get('token'))}

        return requests.patch(
            self.url_for(endpoint),
            params=params,
            json=data,
            headers=headers,
            cookies=cookies,
            timeout=self.timeout,
        )

    @handle_request_error
    def delete_request(
            self, endpoint, params=None, data=None, headers=None, cookies=None):
        """Helper function for DELETE requests

        :param endpoint: The endpoint
        :param params: The URL parameters
        :param data: The data as a dict to include with the DELETE
        :param headers: request headers
        :param cookies: request cookies
        :return: The :class:``requests.Response`` object for this request
        """
        if headers is None:
            headers = {'Authorization': 'Bearer {}'.format(self.config.get('token'))}

        return requests.delete(
            self.url_for(endpoint),
            params=params,
            json=data,
            headers=headers,
            cookies=cookies,
            timeout=self.timeout,
        )


def require_keys(d, keys, allow_none=True):
    """Require that the object have the given keys

    :param d: The dict the check
    :param keys: The keys to check :attr:`obj` for. This can either be a single
                 string, or an iterable of strings

    :param allow_none: Whether ``None`` values are allowed
    :raises:
        :ValueError: If any of the keys are missing from the obj
    """
    if isinstance(keys, str):
        keys = [keys]
    for k in keys:
        if k not in d:
            raise ValueError("'{}' must be set".format(k))
        if not allow_none and d[k] is None:
            raise ValueError("'{}' cannot be None".format(k))
    return True


def date_to_str(d):
    """Convert date and datetime objects to a string

    Note, this does not do any timezone conversion.

    :param d: The :class:`datetime.date` or :class:`datetime.datetime` to
              convert to a string
    :returns: The string representation of the date
    """
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def generate_jwt(key, secret):
    header = {
        "alg": "HS256",
        "typ": "JWT"
    }

    payload = {
        "iss": key,
        "exp": int(time.time() + 3600)
    }

    token = jwt.encode(payload, secret, algorithm='HS256', headers=header)
    return token
