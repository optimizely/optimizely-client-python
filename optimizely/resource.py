__all__ = ['Project', 'Experiment', 'Result', 'Stat', 'Variation', 'Goal', 'Audience']

import json
import urllib


class ResourceGenerator(object):
  def __init__(self, client=None, resource=None):
    if client is None:
      raise ValueError('Must specify client.')
    if resource is None:
      raise ValueError('Must specify resource.')
    self.client = client
    self.resource = resource

  def get(self, optimizely_ids=None):
    if not optimizely_ids:
      return self.resource.list(client=self.client)
    elif type(optimizely_ids) == int or type(optimizely_ids) == long:
      instance = self.resource(self.client, optimizely_id=optimizely_ids)
      instance.refresh()
      return instance
    elif type(optimizely_ids) == list:
      response_list = []
      for optimizely_id in optimizely_ids:
        response_list.append(self.get(optimizely_id))
      return response_list

  def create(self, data):
    return self.resource.create(data, self.client)

  def update(self, rid, data):
    return self.resource.update(rid, data, self.client)


class APIObject(object):
  def __init__(self, client, optimizely_id=None):
    self.client = client
    if optimizely_id:
      self.id = optimizely_id
      self.refresh()

  def refresh(self):
    if not hasattr(self, 'id'):
      raise AttributeError('%s object has no ID, so it cannot be refreshed' % self.class_name())
    self._refresh_from(self.client.request('get', [self.class_url(), self.id]))

  def _refresh_from(self, params):
    for k, v in params.iteritems():
      self.__setattr__(k, v)

  @classmethod
  def class_name(cls):
    if cls == APIObject:
      raise NotImplementedError(
        'APIObject is an abstract class.  You should perform '
        'actions on its subclasses (e.g. Project, Experiment)')
    return cls.__name__.lower()

  @classmethod
  def class_url(cls):
    return '%ss' % cls.class_name()

  def get_child_objects(self, resource):
    resp = []
    for li in self.client.request('get', [self.class_url(), self.id, resource.class_url()]):
      e = resource(self.client)
      e._refresh_from(li)
      resp.append(e)
    return resp


class ListableObject(APIObject):
  @classmethod
  def list(cls, client):
    resp = []
    for li in client.request('get', [cls.class_url()]):
      e = cls(client)
      e._refresh_from(li)
      resp.append(e)
    return resp


class CreatableObject(APIObject):
  @classmethod
  def create(cls, data, client):
    instance = cls(client)
    instance._refresh_from(client.request('post', [cls.class_url()], data=json.dumps(data),
                                          headers={'Content-Type': 'application/json'}))
    return instance


class CreatableChildObject(APIObject):
  parent_resource = None

  @classmethod
  def create(cls, data, client):
    instance = cls(client)
    instance._refresh_from(client.request('post', [cls.parent_resource.class_url(),
                                                   data['%s_id' % cls.parent_resource.class_name()],
                                                   cls.class_url()],
                                          data=json.dumps(data),
                                          headers={'Content-Type': 'application/json'}))
    return instance


class UpdatableObject(APIObject):
  editable_fields = []

  def save(self):
    self._refresh_from(self.update(self.id, self.__dict__, self.client).__dict__)

  @classmethod
  def update(cls, rid, data, client):
    updates = {}
    for k, v in data.iteritems():
      if k in cls.editable_fields:
        updates[k] = v
    resp = client.request('put', [cls.class_url(), rid], data=json.dumps(updates),
                          headers={'Content-Type': 'application/json'})
    instance = cls(client)
    instance._refresh_from(resp)
    return instance


class DeletableObject(APIObject):
  def delete(self):
    self.client.request('delete', [self.class_url(), self.id])


class Project(ListableObject, CreatableObject, UpdatableObject):
  editable_fields = ['project_status',
                     'project_name',
                     'include_jquery',
                     'project_javascript',
                     'enable_force_variation',
                     'exclude_disabled_experiments',
                     'exclude_names',
                     'ip_anonymization',
                     'ip_filter']

  def experiments(self):
    return self.get_child_objects(Experiment)

  def goals(self):
    return self.get_child_objects(Goal)

  def audiences(self):
    return self.get_child_objects(Audience)

  def dimensions(self):
    return self.get_child_objects(Dimension)


class Experiment(CreatableChildObject, UpdatableObject, DeletableObject):
  parent_resource = Project
  editable_fields = ['audience_ids',
                     'activation_mode',
                     'description',
                     'edit_url',
                     'status',
                     'custom_css',
                     'custom_js',
                     'percentage_included',
                     'url_conditions']

  def results(self):
    return self.get_child_objects(Result)

  def stats(self):
    return self.get_child_objects(Stat)

  def variations(self):
    return self.get_child_objects(Variation)

  def schedules(self):
    return self.get_child_objects(Schedule)

  def add_goal(self, gid):
    goal = Goal(self.client, gid)
    experiment_ids = set(goal.experiment_ids)
    experiment_ids.add(self.id)
    goal.experiment_ids = list(experiment_ids)
    return goal.save()

  def remove_goal(self, gid):
    goal = Goal(self.client, gid)
    goal.refresh()
    experiment_ids = set(goal.experiment_ids)
    experiment_ids.remove(self.id)
    goal.experiment_ids = list(experiment_ids)
    return goal.save()


class Result(APIObject):
  pass

class Stat(APIObject):
  pass


class Variation(CreatableChildObject, UpdatableObject, DeletableObject):
  parent_resource = Experiment
  editable_fields = ['description',
                     'is_paused',
                     'js_component',
                     'weight']


class Goal(CreatableChildObject, UpdatableObject, DeletableObject):
  parent_resource = Project
  editable_fields = ['addable',
                     'archived',
                     'description',
                     'experiment_ids',
                     'goal_type',
                     'selector',
                     'target_to_experiments',
                     'target_urls',
                     'target_url_match_types',
                     'title',
                     'urls',
                     'url_match_types']


class Audience(CreatableChildObject, UpdatableObject):
  parent_resource = Project
  editable_fields = ['name',
                     'description',
                     'conditions',
                     'segmentation']


class Dimension(CreatableChildObject, UpdatableObject, DeletableObject):
  parent_resource = Project
  editable_fields = ['name',
                     'client_api_name',
                     'description']


class Schedule(CreatableChildObject, UpdatableObject, DeletableObject):
  parent_resource = Experiment
  editable_fields = ['start_time',
                     'stop_time']
