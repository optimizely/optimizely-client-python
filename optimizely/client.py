import urlparse
import requests

from optimizely import error
from optimizely import resource

base = 'https://www.optimizelyapis.com/experiment/v1/'


class Client(object):
    ALLOWED_REQUESTS = ['get', 'post', 'put', 'delete']

    def __init__(self, api_key, api_base=base):
        self.api_key = api_key
        self.api_base = api_base

        self.Project = resource.ResourceGenerator(client=self, resource=resource.Project)
        self.Experiment = resource.ResourceGenerator(client=self, resource=resource.Experiment)
        self.Variation = resource.ResourceGenerator(client=self, resource=resource.Variation)
        self.Goal = resource.ResourceGenerator(client=self, resource=resource.Goal)
        self.Audience = resource.ResourceGenerator(client=self, resource=resource.Audience)

    def request(self, method, url_parts, headers=None, data=''):

        if method in self.ALLOWED_REQUESTS:
            # add request token header
            headers = headers or {}
            headers.update({'Token': self.api_key})

            # make request and return parsed response
            return self.parse_response(getattr(requests, method)(urlparse.urljoin(
                self.api_base, '/'.join([str(url_part) for url_part in url_parts])), headers=headers, data=data))
        else:
            raise BadRequestError('%s is not a valid request type.' % method)

    @staticmethod
    def parse_response(resp):
        if resp.status_code in [200, 201, 202]:
            return resp.json()
        elif resp.status_code == 204:
            return
        elif resp.status_code == 400:
            raise error.BadRequestError(resp.json().get('message'))
        elif resp.status_code == 401:
            raise error.UnauthorizedError(resp.json().get('message'))
        elif resp.status_code == 403:
            raise error.ForbiddenError(resp.json().get('message'))
        elif resp.status_code == 404:
            raise error.NotFoundError(resp.json().get('message'))
        elif resp.status_code == 429:
            raise error.TooManyRequestsError(resp.json().get('message'))
        elif resp.status_code == 503:
            raise error.ServiceUnavailableError(resp.json().get('message'))
        else:
            raise error.OptimizelyError(resp.text)
