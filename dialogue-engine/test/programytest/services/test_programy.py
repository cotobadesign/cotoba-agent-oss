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

from programy.services.programy import ProgramyRESTService
from programy.config.brain.service import BrainServiceConfiguration

from programytest.client import TestClient


class ProgramyRESTServiceTests(unittest.TestCase):

    def test_format_payload(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        config = BrainServiceConfiguration("rest")
        config._classname = "programy.testclass"
        config._method = "GET"
        config._host = "localhost"
        config._port = 8080
        config._url = "/api/v1.0/ask"

        service = ProgramyRESTService(config, api=None)
        self.assertEqual({'question': 'Hello', 'userid': 'testid'}, service._format_payload(client_context, "Hello"))

    def test_format_get_url(self):
        client = TestClient()
        client_context = client.create_client_context("testid")

        config = BrainServiceConfiguration("rest")
        config._classname = "programy.testclass"
        config._method = "GET"
        config._host = "localhost"
        config._port = 8080
        config._url = "/api/v1.0/ask"

        service = ProgramyRESTService(config, api=None)
        self.assertEqual("/api/v1.0/ask?question=Hello&userid=testid", service._format_get_url("/api/v1.0/ask", client_context, "Hello"))

    def test_parse_response(self):
        client = TestClient()
        client.create_client_context("testid")

        config = BrainServiceConfiguration("rest")
        config._classname = "programy.testclass"
        config._method = "GET"
        config._host = "localhost"
        config._port = 8080
        config._url = "/api/v1.0/ask"

        service = ProgramyRESTService(config, api=None)
        self.assertEqual("Hello", service._parse_response('[{"response": {"answer": "Hello"}}]'))
