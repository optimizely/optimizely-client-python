import json

from api_requester import APIRequester
from optimizely.error import (
    OptimizelyError, BadRequestError, UnauthorizedError, ForbiddenError, NotFoundError, TooManyRequestsError,
    ServiceUnavailableError, InvalidIDError)


class APIResource(object):
    endpoint = ''

    def __init__(self, param):
        if type(param) == int:
            self.__init__(self.get(param).__dict__)
        elif type(param) == dict:
            for (k, v) in param.iteritems():
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
        return cls.from_api_response(APIRequester.request('get', cls.endpoint))

    @classmethod
    def get(cls, pid):
        return cls.from_api_response(APIRequester.request('get', cls.endpoint + str(pid)))

    @classmethod
    def create(cls, data):
        return cls.from_api_response(APIRequester.request('post', cls.endpoint, data=json.dumps(data),
                                                          headers={'Content-Type': 'application/json'}))

    @classmethod
    def update(cls, rid, data):
        return cls.from_api_response(APIRequester.request('put', cls.endpoint + str(rid), data=json.dumps(data),
                                                          headers={'Content-Type': 'application/json'}))

    @classmethod
    def delete(cls, pid):
        return cls.from_api_response(APIRequester.request('delete', cls.endpoint + str(pid)))


class Project(APIResource):
    endpoint = 'projects/'

    @classmethod
    def delete(cls, pid):
        raise NotImplementedError('Projects may not be deleted through the API.')

    def experiments(self):
        if not hasattr(self, 'id'):
            raise InvalidIDError('Project is missing its ID.')
        return Experiment.from_api_response(APIRequester.request('get', self.endpoint + str(self.id) + '/experiments'))

    def audiences(self):
        if not hasattr(self, 'id'):
            raise InvalidIDError('Project is missing its ID.')
        return Audience.from_api_response(APIRequester.request('get', self.endpoint + str(self.id) + '/audiences'))


class Experiment(APIResource):
    endpoint = 'experiments/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all experiments. '
                                  'Try using Project.experiments() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(APIRequester.request('post', 'projects/' + str(data['project_id']) + '/' +
                                                          cls.endpoint, data=json.dumps(data),
                                                          headers={'Content-Type': 'application/json'}))

    def results(self):
        return Result.from_api_response(APIRequester.request('get', self.endpoint + str(self.id) + '/results'))

    def variations(self):
        return Variation.from_api_response(APIRequester.request('get', self.endpoint + str(self.id) + '/variations'))

    def add_goal(self, gid):
        goal = Goal.get(gid)
        experiment_ids = set(goal.experiment_ids)
        experiment_ids.add(self.id)
        return Goal.update(goal.id, {'experiment_ids': list(experiment_ids)})

    def remove_goal(self, gid):
        goal = Goal.get(gid)
        experiment_ids = set(goal.experiment_ids)
        experiment_ids.remove(self.id)
        return Goal.update(goal.id, {'experiment_ids': list(experiment_ids)})


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
        raise NotImplementedError('There is no method to create a result.')

    @classmethod
    def update(cls, pid, data):
        raise NotImplementedError('There is no method to update a result.')

    @classmethod
    def delete(cls, pid):
        raise NotImplementedError('There is no method to delete a result.')


class Variation(APIResource):
    endpoint = 'variations/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.variations() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(APIRequester.request('post', 'experiments/' + str(data['experiment_id']) + '/' +
                                                          cls.endpoint, data=json.dumps(data),
                                                          headers={'Content-Type': 'application/json'}))


class Goal(APIResource):
    endpoint = 'goals/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all goals.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(APIRequester.request('post', 'projects/' + str(data['project_id']) + '/' +
                                                          cls.endpoint, data=json.dumps(data),
                                                          headers={'Content-Type': 'application/json'}))


class Audience(APIResource):
    endpoint = 'audiences/'

    @classmethod
    def list(cls):
        raise NotImplementedError('There is no method to list all results. Try using Experiment.variations() instead.')

    @classmethod
    def create(cls, data):
        return cls.from_api_response(APIRequester.request('post', 'projects/' + str(data['project_id']) + '/' +
                                                          cls.endpoint, data=json.dumps(data),
                                                          headers={'Content-Type': 'application/json'}))

    @classmethod
    def delete(cls, pid):
        raise NotImplementedError('Audiences may not be deleted through the API.')