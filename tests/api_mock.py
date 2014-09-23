import json
import mock

import optimizely


class APIResponseMock():
    """ A class used to mock responses from the requests module
    """
    def __init__(self, status_code=None, data=None, text=None):
        self.status_code = status_code
        self.json = mock.Mock(return_value=data)
        self.text = text


class APIMock():
    """ A class used to mock the Optimizely API. Its get, post, put, and delete functions can be used to mock the
    requests module.
    """
    def __init__(self, get_responses=None, post_responses=None, put_responses=None, delete_responses=None,
                 *args, **kwargs):
        self.get_responses = get_responses or {}
        self.post_responses = post_responses or {}
        self.put_responses = put_responses or {}
        self.delete_responses = delete_responses or {}

    def get(self, url, **kwargs):
        return self.get_responses[url]

    def post(self, url, **kwargs):
        return self.post_responses[url]

    def put(self, url, **kwargs):
        return self.put_responses[url]

    def delete(self, url, **kwargs):
        return self.delete_responses[url]


class TestResource(object):
    """ Base class used for testing Optimizely API Resources. It includes the base tests for standard/shared API
    requests
    """

    def create_mocks(self):
        # create updated data mocks
        self.sample_data_updated = self.sample_data.copy()
        self.sample_data_updated.update(self.sample_updates)

        # mock requests module
        self.mock_api_get = APIResponseMock(200, self.sample_data)
        self.mock_api_create = APIResponseMock(201, self.sample_data)
        self.mock_api_list = APIResponseMock(200, [self.sample_data, self.sample_data])
        self.mock_api_update = APIResponseMock(200, self.sample_data_updated)
        self.mock_api_delete = APIResponseMock(204, None)
        self.mock_api = APIMock(get_responses={
            optimizely.api_base + self.test_resource.endpoint + str(self.id): self.mock_api_get,
            optimizely.api_base + self.test_resource.endpoint: self.mock_api_list
        }, post_responses={
            optimizely.api_base + self.test_resource.endpoint: self.mock_api_create
        }, put_responses={
            optimizely.api_base + self.test_resource.endpoint + str(self.id): self.mock_api_update
        }, delete_responses={
            optimizely.api_base + self.test_resource.endpoint + str(self.id): self.mock_api_delete
        })
        requests_mock = mock.Mock()
        requests_mock.get = mock.Mock(side_effect=self.mock_api.get)
        requests_mock.post = mock.Mock(side_effect=self.mock_api.post)
        requests_mock.put = mock.Mock(side_effect=self.mock_api.put)
        requests_mock.delete = mock.Mock(side_effect=self.mock_api.delete)
        self.p = mock.patch('optimizely.requests', new=requests_mock)
        self.p.start()

    def tearDown(self):
        # if optimizely.requests has been patched, unpatch at the end of each test
        if hasattr(self, 'p'):
            self.p.stop()

    def test_list(self):
        """ Tests that .list() successfully retrieves two objects
        """
        # call .list()
        resources = self.test_resource.list()

        # ensure that the correct GET request was made
        optimizely.requests.get.assert_called_with(optimizely.api_base + self.test_resource.endpoint,
                                                   headers={'Token': optimizely.api_key})

        # ensure that values and types are correct
        self.assertEqual(2, len(resources))
        for resource in resources:
            for k, v in self.sample_data.iteritems():
                self.assertEquals(v, resource.__getattribute__(k))
            self.assertIsInstance(resource, self.test_resource)

    def test_get(self):
        """ Tests that .get() successfully retrieves the correct object
        """
        # call .get()
        resource = self.test_resource.get(self.id)

        # ensure that the correct GET request was made
        optimizely.requests.get.assert_called_with(optimizely.api_base + self.test_resource.endpoint +
                                                   str(self.id), headers={'Token': optimizely.api_key})

        # ensure that values and type are correct
        for k, v in self.sample_data.iteritems():
            self.assertEquals(v, resource.__getattribute__(k))
        self.assertIsInstance(resource, self.test_resource)

    def test_create(self):
        """ Tests that .create() successfully creates and retrieves the correct object
        """
        # call .create()
        resource = self.test_resource.create(self.sample_data)

        # ensure that the correct POST request was made
        optimizely.requests.post.assert_called_with(optimizely.api_base + self.test_resource.endpoint,
                                                    data=json.dumps(self.sample_data),
                                                    headers={'Token': optimizely.api_key,
                                                             'Content-Type': 'application/json'})

        # ensure that values and type are correct
        for k, v in self.sample_data.iteritems():
            self.assertEquals(v, resource.__getattribute__(k))
        self.assertIsInstance(resource, self.test_resource)

    def test_update(self):
        """ Tests that .update() successfully creates and retrieves the correct object
        """
        # call .create()
        resource = self.test_resource.update(self.id, self.sample_updates)

        # ensure that the correct PUT request was made
        optimizely.requests.put.assert_called_with(optimizely.api_base + self.test_resource.endpoint + str(self.id),
                                                   data=json.dumps(self.sample_updates),
                                                   headers={'Token': optimizely.api_key,
                                                            'Content-Type': 'application/json'})

        # ensure that values and type are correct
        for k, v in self.sample_data_updated.iteritems():
            self.assertEquals(v, resource.__getattribute__(k))
        self.assertIsInstance(resource, self.test_resource)

    def test_delete(self):
        """ Tests that .delete() calls the correct endpoint and that it returns None upon success
        """
        # call .delete()
        return_value = self.test_resource.delete(self.id)

        # ensure that the correct DELETE request was made
        optimizely.requests.delete.assert_called_with(optimizely.api_base + self.test_resource.endpoint +
                                                      str(self.id), headers={'Token': optimizely.api_key})

        # ensure that None is returned
        self.assertIsNone(return_value)