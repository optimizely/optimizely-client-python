import json
import requests

api_key = ''
api_base = 'https://www.optimizelyapis.com/experiment/v1/'


class APIResource(object):
    endpoint = ''

    def __init__(self):
        raise NotImplementedError(self.__class__.__name__ +
                                  ' contains only class methods and should not be instantiated.')

    @staticmethod
    def _parse_response(r):
        if r.status_code in [200, 201, 202, 204]:
            return r.json()
        elif r.status_code == 400:
            raise BadRequestError(r.text)
        elif r.status_code == 401:
            raise UnauthorizedError(r.text)
        elif r.status_code == 403:
            raise ForbiddenError(r.text)
        elif r.status_code == 404:
            raise NotFoundError(r.text)
        elif r.status_code == 429:
            raise TooManyRequestsError(r.text)
        elif r.status_code == 503:
            raise ServiceUnavailableError(r.text)
        else:
            raise OptimizelyError(r.text)

    @classmethod
    def all(cls):
        return cls._parse_response(requests.get(api_base + cls.endpoint, headers={'Token': api_key}))

    @classmethod
    def get(cls, pid):
        return cls._parse_response(requests.get(api_base + cls.endpoint + str(pid), headers={'Token': api_key}))

    @classmethod
    def create(cls, data):
        return cls._parse_response(requests.post(api_base + cls.endpoint, data=json.dumps(data),
                                                 headers={'Token': api_key, 'Content-Type': 'application/json'}))

    @classmethod
    def update(cls, pid, data):
        return cls._parse_response(requests.put(api_base + cls.endpoint + str(pid), data=json.dumps(data),
                                                headers={'Token': api_key, 'Content-Type': 'application/json'}))

    @classmethod
    def delete(cls, pid):
        return cls._parse_response(requests.delete(api_base + cls.endpoint + str(pid), headers={'Token': api_key}))


class Project(APIResource):
    endpoint = 'projects/'


class Experiment(APIResource):
    endpoint = 'experiments/'

    @classmethod
    def all(cls):
        raise NotImplementedError('There is no method to get all experiments. Try using get_from_project() instead.')

    @classmethod
    def get_from_project(cls, pid):
        return cls._parse_response(requests.get(api_base + Project.endpoint + str(pid) + '/' + cls.endpoint,
                                                headers={'Token': api_key}))

    @classmethod
    def get_results(cls, eid):
        return cls._parse_response(requests.get(api_base + cls.endpoint + str(eid) + '/results',
                                                headers={'Token': api_key}))


class OptimizelyError(Exception):
    """ General exception for all Optimizely Experiments API related issues."""
    pass


class BadRequestError(OptimizelyError):
    """ Exception for when request was not sent in valid JSON."""
    pass


class UnauthorizedError(OptimizelyError):
    """ Exception for when API token is missing or included in the body rather than the header."""
    pass


class ForbiddenError(OptimizelyError):
    """ Exception for when API token is provided but it is invalid or revoked."""
    pass


class NotFoundError(OptimizelyError):
    """ Exception for when the id used in request is inaccurate or token user doesn't have permission to
    view/edit it."""
    pass


class TooManyRequestsError(OptimizelyError):
    """ Exception for when a rate limit for the API is hit."""
    pass


class ServiceUnavailableError(OptimizelyError):
    """ Exception for when the API is overloaded or down for maintenance."""
    pass