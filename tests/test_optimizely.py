import json
import mock
import unittest

import optimizely
from api_mock import APIResponseMock
from api_mock import TestResource
from optimizely.resource import APIResource


class TestAPIResource(unittest.TestCase):

    def test_from_api_response(self):
        """ Tests that APIResource.from_api_response() responds to API responses correctly
        """
        # set up API response
        mock_values = {'message': 'mock'}
        response = APIResponseMock(data=mock_values)

        # test error response codes
        response.status_code = 400
        self.assertRaises(optimizely.BadRequestError, APIResource.from_api_response, response)
        response.status_code = 401
        self.assertRaises(optimizely.UnauthorizedError, APIResource.from_api_response, response)
        response.status_code = 403
        self.assertRaises(optimizely.ForbiddenError, APIResource.from_api_response, response)
        response.status_code = 404
        self.assertRaises(optimizely.NotFoundError, APIResource.from_api_response, response)
        response.status_code = 429
        self.assertRaises(optimizely.TooManyRequestsError, APIResource.from_api_response, response)
        response.status_code = 503
        self.assertRaises(optimizely.ServiceUnavailableError, APIResource.from_api_response, response)
        response.status_code = 500
        self.assertRaises(optimizely.OptimizelyError, APIResource.from_api_response, response)

        # test correct response codes
        response.status_code = 200
        self.assertDictEqual(mock_values, APIResource.from_api_response(response).__dict__)
        response.status_code = 201
        self.assertDictEqual(mock_values, APIResource.from_api_response(response).__dict__)
        response.status_code = 202
        self.assertDictEqual(mock_values, APIResource.from_api_response(response).__dict__)
        response.status_code = 204
        self.assertIsNone(APIResource.from_api_response(response))


class TestProject(TestResource, unittest.TestCase):
    def setUp(self):
        """ Set up project-specific return values
        """
        # assign resource
        self.test_resource = optimizely.Project

        # test project information
        self.id = 12345
        self.sample_data = {
            'code_revision': 12,
            'installation_verified': None,
            'project_name': 'My project',
            'ip_filter': '1.2.3.4',
            'ip_anonymization': False,
            'created': '2014-04-16T21:33:34.408430Z',
            'library': 'jquery-1.6.4-trim',
            'last_modified': '2014-06-10T22:12:21.707170Z',
            'project_status': 'Active',
            'include_jquery': False,
            'js_file_size': 23693,
            'id': self.id,
            'code_last_modified': '2014-06-10T22:12:20.615820Z',
            'account_id': 555650815
        }
        self.sample_updates = {'project_name': 'My even newer project name'}

        # build mocks for tests
        self.create_mocks()

        # add additional mocks (experiments and audiences)
        self.sample_experiment_data = {
            'id': 15,
            'project_id': self.id,
            'variation_ids': [115, 210, 215],
            'edit_url': 'https://mysite.com/products/',
            'status': 'Not started'
        }
        self.sample_audience_data = {
            'description': 'People from Canada',
            'project_id': self.id,
            'conditions': '[\'and\', {\'type\': \'location\', \'value\': \'CA\'}]',
            'id': 1338260223,
            'name': 'Canadians',
            'last_modified': '2014-06-10T22:12:21.707170Z',
            'segmentation': False
        }
        self.mock_api.get_responses.update({
            optimizely.api_base + optimizely.Project.endpoint + str(self.id) + '/experiments': APIResponseMock(
                200, [self.sample_experiment_data, self.sample_experiment_data]),
            optimizely.api_base + optimizely.Project.endpoint + str(self.id) + '/audiences': APIResponseMock(
                200, [self.sample_audience_data, self.sample_audience_data])
        })

    def test_delete(self):
        """ Tests that Project.delete() raises a NotImplementedError (Projects may not be deleted through the API)
        """
        self.assertRaises(NotImplementedError, optimizely.Project.delete, self.id)

    def test_experiments(self):
        """ Tests that a project's experiments() function returns a list of experiments for that project.
        """
        # call .experiments()
        experiments = optimizely.Project(self.id).experiments()

        # ensure that the correct request was made
        optimizely.api_requester.requests.get.assert_called_with(optimizely.api_base + optimizely.Project.endpoint +
                                                                 str(self.id) + '/experiments',
                                                                 headers={'Token': optimizely.api_key})

        # ensure that values and types are correct
        self.assertEqual(2, len(experiments))
        for experiment in experiments:
            for k, v in self.sample_experiment_data.iteritems():
                self.assertEquals(v, experiment.__getattribute__(k))
            self.assertIsInstance(experiment, optimizely.Experiment)

    def test_audiences(self):
        """ Tests that a project's audiences() function returns a list of audiences for that project.
        """
        # call .experiments()
        audiences = optimizely.Project(self.id).audiences()

        # ensure that the correct request was made
        optimizely.api_requester.requests.get.assert_called_with(optimizely.api_base + optimizely.Project.endpoint +
                                                                 str(self.id) + '/audiences',
                                                                 headers={'Token': optimizely.api_key})

        # ensure that values and types are correct
        self.assertEqual(2, len(audiences))
        for audience in audiences:
            for k, v in self.sample_audience_data.iteritems():
                self.assertEquals(v, audience.__getattribute__(k))
            self.assertIsInstance(audience, optimizely.Audience)


class TestExperiment(TestResource, unittest.TestCase):
    def setUp(self):
        """ Set up experiment-specific return values
        """
        # assign resource
        self.test_resource = optimizely.Experiment

        # test experiment information
        self.id = 12345
        self.project_id = 54321
        self.sample_data = {
            'id': self.id,
            'project_id': self.project_id,
            'percentage_included': 10000,
            'is_multivariate': False,
            'variation_ids': [
                800227656,
                800227657
            ],
            'status': 'Not started',
            'url_conditions': [
                {
                    'index': 0,
                    'match_type': 'simple',
                    'created': '2014-04-12T19:10:53.806640Z',
                    'value': 'https://mysite.com/products',
                    'last_modified': '2014-04-12T19:10:53.806650Z',
                    'negate': False
                }
            ],
            'description': 'My Experiment Name',
            'activation_mode': 'immediate',
            'custom_css': '',
            'custom_js': '',
            'experiment_type': 'ab',
        }
        self.sample_updates = {'status': 'Running'}

        # build mocks for tests
        self.create_mocks()

        # add handling for special create case
        self.mock_api.post_responses = {
            optimizely.api_base + 'projects/' + str(self.project_id) + '/experiments/': self.mock_api_create
        }

        # add additional mocks (results, variations, and goals)
        self.sample_results_data = {
            'variation_id': '925781903',
            'variation_name': 'My Variation',
            'goal_id': 820360058,
            'goal_name': 'Engagement',
            'baseline_id': '924521605',
            'begin_time': '2014-07-25T20:30:00Z',
            'end_time': '2014-07-25T20:38:09Z',
            'visitors': 853,
            'conversions': 204,
            'conversion_rate': 0.239,
            'status': 'inconclusive',
            'improvement': 0.014,
            'confidence': 0.631,
            'is_revenue': False,
        }
        self.sample_variation_data = {
            'is_paused': False,
            'description': 'Original',
            'weight': None,
            'created': '2014-04-17T00:47:58.390560Z',
            'variation_id': 854613530,
            'section_id': None,
            'js_component': '',
            'experiment_id': 854484703,
            'project_id': 859720118,
            'id': 854613530
        }
        self.goal_id = 55555
        self.sample_goal_data = {
            'id': self.goal_id,
            'experiment_ids': []
        }
        self.mock_api.get_responses.update({
            optimizely.api_base + optimizely.Experiment.endpoint + str(self.id) + '/results': APIResponseMock(
                200, [self.sample_results_data, self.sample_results_data]),
            optimizely.api_base + optimizely.Experiment.endpoint + str(self.id) + '/variations': APIResponseMock(
                200, [self.sample_variation_data, self.sample_variation_data]),
            optimizely.api_base + optimizely.Goal.endpoint + str(self.goal_id): APIResponseMock(
                200, self.sample_goal_data)
        })
        self.mock_api.put_responses.update({
            optimizely.api_base + optimizely.Goal.endpoint + str(self.goal_id): APIResponseMock(
                200, self.sample_goal_data)
        })

    def test_create(self):
        """ Tests that .create() successfully creates and retrieves the correct object
        """
        # call .create()
        experiment = optimizely.Experiment.create(self.sample_data)

        # ensure that the correct request was made
        optimizely.api_requester.requests.post.assert_called_with(optimizely.api_base + 'projects/' +
                                                                  str(self.sample_data['project_id']) + '/' +
                                                                  self.test_resource.endpoint,
                                                                  data=json.dumps(self.sample_data),
                                                                  headers={'Token': optimizely.api_key,
                                                                           'Content-Type': 'application/json'})

        # ensure that values and type are correct
        for k, v in self.sample_data.iteritems():
            self.assertEquals(v, experiment.__getattribute__(k))
        self.assertIsInstance(experiment, optimizely.Experiment)

    def test_list(self):
        """ Tests that Experiment.list() raises a NotImplementedError (Experiments can only be listed on a per-Project
        basis)
        """
        self.assertRaises(NotImplementedError, optimizely.Experiment.list)

    def test_results(self):
        """ Tests that an experiment's results() function returns a list of results for that experiment.
        """
        # call .experiments()
        results = optimizely.Experiment(self.id).results()

        # ensure that the correct request was made
        optimizely.api_requester.requests.get.assert_called_with(optimizely.api_base + optimizely.Experiment.endpoint +
                                                                 str(self.id) + '/results',
                                                                 headers={'Token': optimizely.api_key})

        # ensure that values and types are correct
        self.assertEqual(2, len(results))
        for result in results:
            for k, v in self.sample_results_data.iteritems():
                self.assertEquals(v, result.__getattribute__(k))
            self.assertIsInstance(result, optimizely.Result)

    def test_variations(self):
        """ Tests that an experiment's variations() function returns a list of variations for that experiment.
        """
        # call .experiments()
        variations = optimizely.Experiment(self.id).variations()

        # ensure that the correct request was made
        optimizely.api_requester.requests.get.assert_called_with(optimizely.api_base + optimizely.Experiment.endpoint +
                                                                 str(self.id) + '/variations',
                                                                 headers={'Token': optimizely.api_key})

        # ensure that values and types are correct
        self.assertEqual(2, len(variations))
        for variation in variations:
            for k, v in self.sample_variation_data.iteritems():
                self.assertEquals(v, variation.__getattribute__(k))
            self.assertIsInstance(variation, optimizely.Variation)

    @mock.patch('optimizely.Goal.update', mock.Mock())
    def test_add_goal(self):
        """ Tests that an experiment's add_goal() function correctly adds a goal to given experiment
        """
        # add goal to experiment
        experiment = optimizely.Experiment(self.sample_data)
        experiment.add_goal(self.goal_id)

        # ensure that Goal.update() is called with the correct arguments
        optimizely.Goal.update.assert_called_with(self.goal_id, {'experiment_ids': [self.id]})

    @mock.patch('optimizely.Goal.update', mock.Mock())
    def test_remove_goal(self):
        """ Tests that an experiment's remove_goal() function correctly adds a goal to given experiment
        """
        # add experiment_id to goal's experiment_ids list
        self.sample_goal_data['experiment_ids'] = [self.id]

        # remove goal from experiment
        experiment = optimizely.Experiment(self.sample_data)
        experiment.remove_goal(self.goal_id)

        # ensure that Goal.update() is called with the correct arguments
        optimizely.Goal.update.assert_called_with(self.goal_id, {'experiment_ids': []})


class TestResult(unittest.TestCase):

    def test_list(self):
        """ Tests that Result.list() raises a NotImplementedError
        """
        self.assertRaises(NotImplementedError, optimizely.Result.list)

    def test_get(self):
        """ Tests that Result.get() raises a NotImplementedError
        """
        self.assertRaises(NotImplementedError, optimizely.Result.get, 1)

    def test_create(self):
        """ Tests that Result.create() raises a NotImplementedError
        """
        self.assertRaises(NotImplementedError, optimizely.Result.create, {'mock': 'mock'})

    def test_update(self):
        """ Tests that Result.update() raises a NotImplementedError
        """
        self.assertRaises(NotImplementedError, optimizely.Result.update, 1, {'mock': 'mock'})

    def test_delete(self):
        """ Tests that Result.delete() raises a NotImplementedError
        """
        self.assertRaises(NotImplementedError, optimizely.Result.delete, 1)


class TestVariation(TestResource, unittest.TestCase):
    def setUp(self):
        """ Set up variation-specific return values
        """
        # assign resource
        self.test_resource = optimizely.Variation

        # test variation information
        self.id = 12345
        self.experiment_id = 54321
        self.sample_data = {
            'is_paused': False,
            'description': 'Original',
            'weight': None,
            'created': '2014-04-17T00:47:58.390560Z',
            'variation_id': self.id,
            'section_id': None,
            'js_component': '',
            'experiment_id': self.experiment_id,
            'project_id': 859720118,
            'id': 854613530
        }
        self.sample_updates = {'js_component': '$(".headline").text("Updated headline");'}

        # build mocks for tests
        self.create_mocks()

        # add handling for special create case
        self.mock_api.post_responses = {
            optimizely.api_base + 'experiments/' + str(self.experiment_id) + '/variations/': self.mock_api_create
        }

    def test_create(self):
        """ Tests that .create() successfully creates and retrieves the correct object
        """
        # call .create()
        variation = optimizely.Variation.create(self.sample_data)

        # ensure that the correct request was made
        optimizely.api_requester.requests.post.assert_called_with(optimizely.api_base + 'experiments/' +
                                                                  str(self.sample_data['experiment_id']) + '/' +
                                                                  self.test_resource.endpoint,
                                                                  data=json.dumps(self.sample_data),
                                                                  headers={'Token': optimizely.api_key,
                                                                           'Content-Type': 'application/json'})

        # ensure that values and type are correct
        for k, v in self.sample_data.iteritems():
            self.assertEquals(v, variation.__getattribute__(k))
        self.assertIsInstance(variation, optimizely.Variation)

    def test_list(self):
        """ Tests that Variation.list() raises a NotImplementedError (Variations can only be listed on a per-Experiment
        basis)
        """
        self.assertRaises(NotImplementedError, optimizely.Variation.list)


class TestGoal(TestResource, unittest.TestCase):
    def setUp(self):
        """ Set up goal-specific return values
        """
        # assign resource
        self.test_resource = optimizely.Goal

        # test variation information
        self.id = 12345
        self.project_id = 54321
        self.sample_data = {
            'metric': 0,
            'is_editable': None,
            'target_to_experiments': True,
            'revenue_tracking_amount': None,
            'id': self.id,
            'target_urls': [],
            'title': 'Navigation button clicks',
            'preview_user_agent': '',
            'event': 'nav_button_clicks',
            'url_match_types': [],
            'element_id': '',
            'project_id': self.project_id,
            'goal_type': 0,
            'deleted': False,
            'experiment_ids': [
                561450169
            ],
            'selector': '.portal-navigation > button',
            'multi_event': False,
            'created': '2014-01-09T23:47:51.042343Z',
            'target_url_match_types': [],
            'revenue_tracking': False,
            'preview_url': 'http://www.google.com/',
            'addable': True,
            'urls': []
        }
        self.sample_updates = {'title': 'Updated goal name'}

        # build mocks for tests
        self.create_mocks()

        # add handling for special create case
        self.mock_api.post_responses = {
            optimizely.api_base + 'projects/' + str(self.project_id) + '/goals/': self.mock_api_create
        }

    def test_create(self):
        """ Tests that .create() successfully creates and retrieves the correct object
        """
        # call .create()
        goal = optimizely.Goal.create(self.sample_data)

        # ensure that the correct request was made
        optimizely.api_requester.requests.post.assert_called_with(optimizely.api_base + 'projects/' +
                                                                  str(self.sample_data['project_id']) + '/' +
                                                                  self.test_resource.endpoint,
                                                                  data=json.dumps(self.sample_data),
                                                                  headers={'Token': optimizely.api_key,
                                                                           'Content-Type': 'application/json'})

        # ensure that values and type are correct
        for k, v in self.sample_data.iteritems():
            self.assertEquals(v, goal.__getattribute__(k))
        self.assertIsInstance(goal, optimizely.Goal)

    def test_list(self):
        """ Tests that Goal.list() raises a NotImplementedError (there is no method to list all goals)
        """
        self.assertRaises(NotImplementedError, optimizely.Goal.list)


class TestAudience(TestResource, unittest.TestCase):
    def setUp(self):
        """ Set up audience-specific return values
        """
        # assign resource
        self.test_resource = optimizely.Audience

        # test variation information
        self.id = 12345
        self.project_id = 54321
        self.sample_data = {
            'description': 'People from Canada',
            'project_id': self.project_id,
            'id': self.id,
            'name': 'Canadians',
            'conditions': '["and", {"type":"browser", "value":"gc"}, '
                          '{"type":"query", "name":"utm_campaign", "value":"true"}]',
            'last_modified': '2014-06-10T22:12:21.707170Z',
            'segmentation': False
        }
        self.sample_updates = {'description': 'People who bought Chinese food'}

        # build mocks for tests
        self.create_mocks()

        # add handling for special create case
        self.mock_api.post_responses = {
            optimizely.api_base + 'projects/' + str(self.project_id) + '/audiences/': self.mock_api_create
        }

    def test_create(self):
        """ Tests that .create() successfully creates and retrieves the correct object
        """
        # call .create()
        audience = optimizely.Audience.create(self.sample_data)

        # ensure that the correct request was made
        optimizely.api_requester.requests.post.assert_called_with(optimizely.api_base + 'projects/' +
                                                                  str(self.sample_data['project_id']) + '/' +
                                                                  self.test_resource.endpoint,
                                                                  data=json.dumps(self.sample_data),
                                                                  headers={'Token': optimizely.api_key,
                                                                           'Content-Type': 'application/json'})

        # ensure that values and type are correct
        for k, v in self.sample_data.iteritems():
            self.assertEquals(v, audience.__getattribute__(k))
        self.assertIsInstance(audience, optimizely.Audience)

    def test_list(self):
        """ Tests that Audience.list() raises a NotImplementedError
        """
        self.assertRaises(NotImplementedError, optimizely.Audience.list)

    def test_delete(self):
        """ Tests that Audience.delete() raises a NotImplementedError (Audiences may not be deleted through the API)
        """
        self.assertRaises(NotImplementedError, optimizely.Audience.delete, self.id)