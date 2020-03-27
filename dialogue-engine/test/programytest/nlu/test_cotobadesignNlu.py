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

from programy.config.brain.nlu import BrainNluConfiguration
from programy.nlu.nlu import NluRequest
from programy.nlu.cotobadesignNlu import CotobadesignNlu


class MockRequestsResponse(object):

    def __init__(self, data, status_code):
        self._data = data
        self._status_code = status_code

    @property
    def text(self):
        return self._data

    @property
    def status_code(self):
        return self._status_code


class MockCotobadesignNluAPI(object):

    def __init__(self, response=None, status=200, exception=False):
        self._response = response
        self._status_code = status
        self._exception = exception

    def post(self, data=None, **kwargs):
        if self._exception is True:
            raise Exception("NLU error communication")
        return MockRequestsResponse(self._response, self._status_code)


class CotobadesignNluTests(unittest.TestCase):

    def test_nlu_initiate(self):

        nlu_config = BrainNluConfiguration()
        nlu_config._classname = "programy.nlu.cotobadesignNlu.CotobadesignNlu"

        nlu = NluRequest.load_nlu(nlu_config)
        self.assertIsNotNone(nlu)
        self.assertIsInstance(nlu, CotobadesignNlu)

    def test_nluCall(self):

        nlu_config = BrainNluConfiguration()
        nlu_config._classname = "programy.nlu.cotobadesignNlu.CotobadesignNlu"

        nlu = NluRequest.load_nlu(nlu_config)
        self.assertIsNotNone(nlu)
        self.assertIsInstance(nlu, CotobadesignNlu)

        response_data = '{"intents": [], "slots": []}'
        request_api = MockCotobadesignNluAPI(response=response_data)
        nlu.set_request_api(request_api)

        response = nlu.nluCall(None, "http://test.co.jp", "apikey", "Test")
        self.assertEqual(response, '{"intents": [], "slots": []}')

    def test_nluCall_exception(self):

        nlu_config = BrainNluConfiguration()
        nlu_config._classname = "programy.nlu.cotobadesignNlu.CotobadesignNlu"

        nlu = NluRequest.load_nlu(nlu_config)
        self.assertIsNotNone(nlu)
        self.assertIsInstance(nlu, CotobadesignNlu)

        response_data = ""
        request_api = MockCotobadesignNluAPI(response=response_data, exception=True)
        nlu.set_request_api(request_api)

        response = nlu.nluCall(None, "http://test.co.jp", "apikey", "Test")
        self.assertIsNone(response)
