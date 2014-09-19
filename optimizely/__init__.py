import json
import requests

api_key = ''
api_base = 'https://www.optimizelyapis.com/experiment/v1/'


class APIResource(dict):
    endpoint = ''

    def __init__(self, *arg, **kw):
        super(APIResource, self).__init__(*arg, **kw)

    @classmethod
    def from_json(cls, r):
        if r.status_code in [200, 201, 202]:
            if type(r.json()) == list:
                return [cls(resource) for resource in r.json()]
            else:
                return cls(r.json())
        elif r.status_code == 204:
            return
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
    def list(cls):
        return cls.from_json(requests.get(api_base + cls.endpoint, headers={'Token': api_key}))

    @classmethod
    def read(cls, pid):
        return cls.from_json(requests.get(api_base + cls.endpoint + str(pid), headers={'Token': api_key}))

    @classmethod
    def create(cls, data):
        return cls.from_json(requests.post(api_base + cls.endpoint, data=json.dumps(data),
                                           headers={'Token': api_key, 'Content-Type': 'application/json'}))

    @classmethod
    def put(cls, rid, data):
        return cls.from_json(requests.put(api_base + cls.endpoint + str(rid), data=json.dumps(data),
                                          headers={'Token': api_key, 'Content-Type': 'application/json'}))

    @classmethod
    def delete(cls, pid):
        return cls.from_json(requests.delete(api_base + cls.endpoint + str(pid), headers={'Token': api_key}))


class Project(APIResource):
    endpoint = 'projects/'

    @classmethod
    def delete(cls, pid):
        raise NotImplementedError('Projects may not be deleted through the API.')

    def experiments(self):
        if not self.get('id'):
            raise InvalidIDError('Project is missing its ID.')
        return Experiment.from_json(requests.get(api_base + self.endpoint + str(self['id']) + '/experiments',
                                                 headers={'Token': api_key}))

    def audiences(self):
        if not self.get('id'):
            raise InvalidIDError('Project is missing its ID.')
        return Audience.from_json(requests.get(api_base + self.endpoint + str(self['id']) + '/audiences',
                                               headers={'Token': api_key}))


class Experiment(APIResource):
    endpoint = 'experiments/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all experiments. '
                                  'Try using Project.experiments() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_json(requests.post(api_base + 'projects/' + str(data['project_id']) + '/' + cls.endpoint,
                                           data=json.dumps(data),
                                           headers={'Token': api_key, 'Content-Type': 'application/json'}))

    def results(self):
        return Result.from_json(requests.get(api_base + self.endpoint + str(self['id']) + '/results',
                                             headers={'Token': api_key}))

    def variations(self):
        return Variation.from_json(requests.get(api_base + self.endpoint + str(self['id']) + '/variations',
                                                headers={'Token': api_key}))

    def add_goal(self, gid):
        goal = Goal.read(gid)
        return Goal.from_json(Goal.put(goal.get('id'),
                                       {'experiment_ids': goal.get('experiment_ids').append(self['id'])}))

    def remove_goal(self, gid):
        goal = Goal.read(gid)
        experiment_ids = list(set(goal.get('experiment_ids')).remove(self['id']))
        return Goal.from_json(Goal.put(goal.get('id'), {'experiment_ids': experiment_ids}))


class Result(APIResource):
    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.results() instead.')

    @classmethod
    def read(cls, pid):
        raise NotImplementedError('There is no method to get a single result.')

    @classmethod
    def create(cls, data):
        return NotImplementedError('There is no method to create a result.')

    @classmethod
    def put(cls, pid, data):
        return NotImplementedError('There is no method to update a result.')

    @classmethod
    def delete(cls, pid):
        return NotImplementedError('There is no method to delete a result.')


class Variation(APIResource):
    endpoint = 'variations/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.variations() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_json(requests.post(api_base + 'experiments/' + str(data['experiment_id']) + '/' + cls.endpoint,
                                           data=json.dumps(data),
                                           headers={'Token': api_key, 'Content-Type': 'application/json'}))


class Goal(APIResource):
    endpoint = 'goals/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all goals.')

    @classmethod
    def create(cls, data):
        return cls.from_json(requests.post(api_base + 'projects/' + str(data['project_id']) + '/' + cls.endpoint,
                                           data=json.dumps(data),
                                           headers={'Token': api_key, 'Content-Type': 'application/json'}))


class Audience(APIResource):
    endpoint = 'audiences/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.variations() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_json(requests.post(api_base + 'projects/' + str(data['project_id']) + '/' + cls.endpoint,
                                           data=json.dumps(data),
                                           headers={'Token': api_key, 'Content-Type': 'application/json'}))


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


class InvalidIDError(OptimizelyError):
    """ Exception for when object is missing its ID."""
    pass