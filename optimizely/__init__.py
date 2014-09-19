import json
import requests

from errors import *

api_key = ''
api_base = 'https://www.optimizelyapis.com/experiment/v1/'


class APIResource(object):
    endpoint = ''

    def __init__(self, params):
        if type(params) == dict:
            for (k, v) in params.iteritems():
                self.__setattr__(k, v)
        else:
            raise ValueError('%s can only be initiated with a dict.' % self.__class__.__name__)

    def __repr__(self):
        if hasattr(self, 'id'):
            return '<%s object with ID: %s>' % (self.__class__.__name__, self.id)
        else:
            return '<%s object without ID>' % self.__class__.__name__


    @classmethod
    def from_api_response(cls, r):
        if r.status_code in [200, 201, 202]:
            if type(r.json()) == list:
                return [cls(resource) for resource in r.json()]
            else:
                return cls(r.json())
        elif r.status_code == 204:
            return
        elif r.status_code == 400:
            raise BadRequestError(r.json().get('message'))
        elif r.status_code == 401:
            raise UnauthorizedError(r.json().get('message'))
        elif r.status_code == 403:
            raise ForbiddenError(r.json().get('message'))
        elif r.status_code == 404:
            raise NotFoundError(r.json().get('message'))
        elif r.status_code == 429:
            raise TooManyRequestsError(r.json().get('message'))
        elif r.status_code == 503:
            raise ServiceUnavailableError(r.json().get('message'))
        else:
            raise OptimizelyError(r.text)

    @classmethod
    def list(cls):
        return cls.from_api_response(requests.get(api_base + cls.endpoint, headers={'Token': api_key}))

    @classmethod
    def get(cls, pid):
        return cls.from_api_response(requests.get(api_base + cls.endpoint + str(pid), headers={'Token': api_key}))

    @classmethod
    def create(cls, data):
        return cls.from_api_response(requests.post(api_base + cls.endpoint, data=json.dumps(data),
                                                   headers={'Token': api_key, 'Content-Type': 'application/json'}))

    @classmethod
    def update(cls, rid, data):
        return cls.from_api_response(requests.put(api_base + cls.endpoint + str(rid), data=json.dumps(data),
                                                  headers={'Token': api_key, 'Content-Type': 'application/json'}))

    @classmethod
    def delete(cls, pid):
        return cls.from_api_response(requests.delete(api_base + cls.endpoint + str(pid), headers={'Token': api_key}))


class Project(APIResource):
    endpoint = 'projects/'

    @classmethod
    def delete(cls, pid):
        raise NotImplementedError('Projects may not be deleted through the API.')

    def experiments(self):
        if not hasattr(self, 'id'):
            raise InvalidIDError('Project is missing its ID.')
        return Experiment.from_api_response(requests.get(api_base + self.endpoint + str(self.id) + '/experiments',
                                                         headers={'Token': api_key}))

    def audiences(self):
        if not hasattr(self, 'id'):
            raise InvalidIDError('Project is missing its ID.')
        return Audience.from_api_response(requests.get(api_base + self.endpoint + str(self.id) + '/audiences',
                                                       headers={'Token': api_key}))


class Experiment(APIResource):
    endpoint = 'experiments/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all experiments. '
                                  'Try using Project.experiments() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(requests.post(api_base + 'projects/' + str(data['project_id']) + '/' +
                                                   cls.endpoint, data=json.dumps(data),
                                                   headers={'Token': api_key, 'Content-Type': 'application/json'}))

    def results(self):
        return Result.from_api_response(requests.get(api_base + self.endpoint + str(self.id) + '/results',
                                                     headers={'Token': api_key}))

    def variations(self):
        return Variation.from_api_response(requests.get(api_base + self.endpoint + str(self.id) + '/variations',
                                                        headers={'Token': api_key}))

    def add_goal(self, gid):
        goal = Goal.get(gid)
        return Goal.from_api_response(Goal.update(goal.id, {'experiment_ids': goal.experiment_ids.append(self.id)}))

    def remove_goal(self, gid):
        goal = Goal.get(gid)
        experiment_ids = list(set(goal.experiment_ids).remove(self.id))
        return Goal.from_api_response(Goal.update(goal.id, {'experiment_ids': experiment_ids}))


class Result(APIResource):
    def __repr__(self):
        return '<%s object>' % self.__class__.__name__

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.results() instead.')

    @classmethod
    def get(cls, pid):
        raise NotImplementedError('There is no method to get a single result.')

    @classmethod
    def create(cls, data):
        return NotImplementedError('There is no method to create a result.')

    @classmethod
    def update(cls, pid, data):
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
        return cls.from_api_response(requests.post(api_base + 'experiments/' + str(data['experiment_id']) + '/' +
                                                   cls.endpoint, data=json.dumps(data),
                                                   headers={'Token': api_key, 'Content-Type': 'application/json'}))


class Goal(APIResource):
    endpoint = 'goals/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all goals.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(requests.post(api_base + 'projects/' + str(data['project_id']) + '/' +
                                                   cls.endpoint, data=json.dumps(data),
                                                   headers={'Token': api_key, 'Content-Type': 'application/json'}))


class Audience(APIResource):
    endpoint = 'audiences/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.variations() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(requests.post(api_base + 'projects/' + str(data['project_id']) + '/' +
                                                   cls.endpoint, data=json.dumps(data),
                                                   headers={'Token': api_key, 'Content-Type': 'application/json'}))