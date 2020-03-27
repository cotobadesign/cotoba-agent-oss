"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest

from programy.services.publishedrest import PublishedRestService, PublishedRestAPI
from programy.services.service import BrainServiceConfiguration

from programytest.client import TestClient


class MockResponseHeaders(object):

    def __init__(self):
        self._headers = {}

    def get(self, key):
        if key in self._headers:
            return self._headers[key]
        return None


class MockRequestsResponse(object):

    def __init__(self, data, status_code):
        self._data = data
        self._status_code = status_code
        self._headers = MockResponseHeaders()

    @property
    def text(self):
        return self._data

    @property
    def status_code(self):
        return self._status_code

    @property
    def headers(self):
        return self._headers


class MockPublishedRestRequest(object):

    def __init__(self, response=None):
        self._response = response

    def get(self, url, params, headers, data):
        return MockRequestsResponse(self._response, 200)

    def post(self, url, params, headers, data):
        return MockRequestsResponse(self._response, 200)

    def put(self, url, params, headers, data):
        return MockRequestsResponse(self._response, 200)

    def delete(self, url, params, headers, data):
        return MockRequestsResponse(self._response, 200)


class MockPublishedRestAPI(object):

    def __init__(self, status=200, response=None, throw_exception=False):
        self._status_code = status
        self._response = response
        self._throw_exception = throw_exception

    def get(self, url, query, header, body):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return MockRequestsResponse(self._response, self._status_code)

    def post(self, url, query, header, body):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return MockRequestsResponse(self._response, self._status_code)

    def put(self, url, query, header, body):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return MockRequestsResponse(self._response, self._status_code)

    def delete(self, url, query, header, body):
        if self._throw_exception is True:
            raise Exception(self._response)
        else:
            return MockRequestsResponse(self._response, self._status_code)


class PublishedRestAPITests(unittest.TestCase):

    def test_api_get(self):

        response_data = 'Hello'
        moc_request = MockPublishedRestRequest(response=response_data)
        request_api = PublishedRestAPI(request_api=moc_request)
        url = ""
        params = ""
        headers = ""
        data = ""
        response = request_api.get(url, params, headers, data)
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello', response.text)

    def test_api_post(self):

        response_data = 'Hello'
        moc_request = MockPublishedRestRequest(response=response_data)
        request_api = PublishedRestAPI(request_api=moc_request)
        url = ""
        params = ""
        headers = ""
        data = ""
        response = request_api.post(url, params, headers, data)
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello', response.text)

    def test_api_put(self):

        response_data = 'Hello'
        moc_request = MockPublishedRestRequest(response=response_data)
        request_api = PublishedRestAPI(request_api=moc_request)
        url = ""
        params = ""
        headers = ""
        data = ""
        response = request_api.put(url, params, headers, data)
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello', response.text)

    def test_api_delete(self):

        response_data = 'Hello'
        moc_request = MockPublishedRestRequest(response=response_data)
        request_api = PublishedRestAPI(request_api=moc_request)
        url = ""
        params = ""
        headers = ""
        data = ""
        response = request_api.delete(url, params, headers, data)
        self.assertIsNotNone(response)
        self.assertEqual(200, response.status_code)
        self.assertEqual('Hello', response.text)


class PublishedRestServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("testid")
        self._config = BrainServiceConfiguration("__PUBLISHEDBOT__")

    def test_ask_question_set_parameter(self):

        service = PublishedRestService(config=self._config)
        self.assertIsNotNone(service)

        service._host = "http://test.publishdrest.url"
        service._method = "GET"
        service._query = '"userid": "test01", "question": "Hello"'
        service._header = '"Content-type": "application/json;charset=UTF-8"'
        service._body = "Hello"

        self.assertEqual('http://test.publishdrest.url', service.host)
        self.assertEqual('GET', service.method)
        self.assertEqual('"userid": "test01", "question": "Hello"', service.query)
        self.assertEqual('"Content-type": "application/json;charset=UTF-8"', service.header)
        self.assertEqual('Hello', service.body)

    def test_ask_question_get(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "GET"
        service.query = None
        service.header = None
        service.body = "Hello"

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_post(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "POST"
        service.query = None
        service.header = None
        service.body = "Hello"

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_put(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "PUT"
        service.query = None
        service.header = None
        service.body = "Hello"

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_delete(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "DELETE"
        service.query = None
        service.header = None
        service.body = "Hello"

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_invlid_method(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "INSERT"
        service.query = None
        service.header = None
        service.body = "Hello"

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual("", response)

    def test_ask_question_get_parameter(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "GET"
        service.query = {"userid": "test01", "question": "Hello"}
        service.header = {"Content-type": "application/json;charset=UTF-8"}
        service.body = '{"json": {"data": "test"}}'

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_Illegal_status(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(status=500, response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "GET"
        service.query = {"userid": "test01", "question": "Hello"}
        service.header = {"Content-type": "application/json,charset=UTF-8"}
        service.body = '{"json": {"data": "test"}}'

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_no_parameter(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_no_host(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.method = "GET"
        service.query = '"userid": "test01", "question": "Hello"'
        service.header = '"Content-type": "application/json,charset=UTF-8"'
        service.body = None

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('', response)

    def test_ask_question_no_body(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "GET"
        service.query = {"userid": "test01", "question": "Hello"}
        service.header = {"Content-type": "application/json;charset=UTF-8"}
        service.body = None

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_no_content_type(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "GET"
        service.query = {"userid": "test01", "question": "Hello"}
        service.header = {"Content": "application/json;charset=UTF-8"}
        service.body = '{"json": {"data": "test"}}'

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)

    def test_ask_question_no_charset(self):

        response_data = 'Hello'
        request_api = MockPublishedRestAPI(response=response_data)
        service = PublishedRestService(config=self._config, api=request_api)
        self.assertIsNotNone(service)

        service.host = "http://test.publishdrest.url"
        service.method = "GET"
        service.query = {"userid": "test01", "question": "Hello"}
        service.header = {"Content-type": "application/json"}
        service.body = '{"json": {"data": "test"}}'

        question = None
        response = service.ask_question(self._client_context, question)
        self.assertEqual('Hello', response)
