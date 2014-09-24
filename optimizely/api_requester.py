import requests

from optimizely.error import BadRequestError, UnauthorizedError


class APIRequester(object):

    @classmethod
    def request(cls, method, url, headers=None, data=''):
        # get up-to-date key and base
        from optimizely import api_key, api_base
        if api_key is None:
            raise UnauthorizedError('API key is not set.')

        # add request token header
        headers = headers or {}
        headers.update({'Token': api_key})

        # make request
        if str(method).upper() == 'GET':
            if data:
                return requests.get(api_base + url, headers=headers, data=data)
            else:
                return requests.get(api_base + url, headers=headers)
        elif str(method).upper() == 'POST':
            if data:
                return requests.post(api_base + url, headers=headers, data=data)
            else:
                return requests.post(api_base + url, headers=headers)
        elif str(method).upper() == 'PUT':
            if data:
                return requests.put(api_base + url, headers=headers, data=data)
            else:
                return requests.put(api_base + url, headers=headers)
        elif str(method).upper() == 'DELETE':
            if data:
                return requests.delete(api_base + url, headers=headers, data=data)
            else:
                return requests.delete(api_base + url, headers=headers)
        else:
            raise BadRequestError('%s is not a valid request type.' % method)
