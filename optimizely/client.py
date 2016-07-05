__all__ = ['Client']

import urlparse
import requests

from optimizely import error
from optimizely import resource

BASE_URL = 'https://www.optimizelyapis.com/experiment/v1/'

VALID_TOKEN_TYPES = ('legacy', 'oauth')

class Client(object):
  ALLOWED_REQUESTS = ['get', 'post', 'put', 'delete']

  def __init__(self, api_key, token_type, api_base=BASE_URL):
    # set API information
    self.api_key = api_key
    self.api_base = api_base

    if token_type in VALID_TOKEN_TYPES:
      self.token_type = token_type
    else:
      raise ValueError('Invalid token type! Valid types are: %s' % (VALID_TOKEN_TYPES,))

    # instantiate resource generators for the relevant API resources
    self.Projects = resource.ResourceGenerator(client=self, resource=resource.Project)
    self.Experiments = resource.ResourceGenerator(client=self, resource=resource.Experiment)
    self.Variations = resource.ResourceGenerator(client=self, resource=resource.Variation)
    self.Goals = resource.ResourceGenerator(client=self, resource=resource.Goal)
    self.Audiences = resource.ResourceGenerator(client=self, resource=resource.Audience)
    self.Dimensions = resource.ResourceGenerator(client=self, resource=resource.Dimension)
    self.Schedules = resource.ResourceGenerator(client=self, resource=resource.Schedule)

  def request(self, method, url_parts, headers=None, data=None):
    """ Method for making requests to the Optimizely API
    """
    if method in self.ALLOWED_REQUESTS:
      # add request token header
      headers = headers or {}

      # test if Oauth token
      if self.token_type == 'legacy':
        headers.update({'Token': self.api_key, 'User-Agent': 'optimizely-client-python/0.1.1'})
      elif self.token_type == 'oauth':
        headers.update({'Authorization': ' Bearer ' + self.api_key, 'User-Agent': 'optimizely-client-python/0.1.1'})
      else:
        raise ValueError('%s is not a valid token type.' % token_type)
      # make request and return parsed response
      url = urlparse.urljoin(self.api_base, '/'.join([str(url_part) for url_part in url_parts]))
      return self.parse_response(getattr(requests, method)(url, headers=headers, data=data))
    else:
      raise error.BadRequestError('%s is not a valid request type.' % method)

  @staticmethod
  def parse_response(resp):
    """ Method to parse response from the Optimizely API and return results as JSON. Errors are thrown for various
    errors that the API can throw.
    """
    if resp.status_code in [200, 201, 202]:
      return resp.json()
    elif resp.status_code == 204:
      return None
    elif resp.status_code == 400:
      raise error.BadRequestError(resp.text)
    elif resp.status_code == 401:
      raise error.UnauthorizedError(resp.text)
    elif resp.status_code == 403:
      raise error.ForbiddenError(resp.text)
    elif resp.status_code == 404:
      raise error.NotFoundError(resp.text)
    elif resp.status_code == 429:
      raise error.TooManyRequestsError(resp.text)
    elif resp.status_code == 503:
      raise error.ServiceUnavailableError(resp.text)
    else:
      raise error.OptimizelyError(resp.text)
