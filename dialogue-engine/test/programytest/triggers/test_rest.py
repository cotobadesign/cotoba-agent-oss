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

from programy.triggers.manager import TriggerManager
from programy.triggers.config import TriggerConfiguration
from programytest.client import TestClient
from programy.triggers.rest import RestTriggerManager


class MockResponse(object):

    def __init__(self, status_code=200):
        self.status_code = status_code


class MockRestTriggerManager(RestTriggerManager):

    def __init__(self, config: TriggerConfiguration):
        RestTriggerManager.__init__(self, config)

    def post_data(self, api_url_base, headers, payload):
        return MockResponse()


class RestTriggerManagerTests(unittest.TestCase):

    def test_create(self):
        config = TriggerConfiguration()
        config._manager = TriggerConfiguration.REST_MANAGER

        mgr = TriggerManager.load_trigger_manager(config)
        self.assertIsNotNone(mgr)

    def test_trigger_triggers(self):
        config = TriggerConfiguration()
        config._manager = "programytest.triggers.test_rest.MockRestTriggerManager"
        config._additionals["url"] = "http://localhost/api/1.0/ask"

        mgr = TriggerManager.load_trigger_manager(config)

        client = TestClient()
        client_context = client.create_client_context("testid")

        triggered = mgr.trigger("SYSTEM_STARTUP")
        self.assertTrue(triggered)

        triggered = mgr.trigger("SYSTEM_STARTUP", additional={"key": "value"})
        self.assertTrue(triggered)

        triggered = mgr.trigger("CONVERSATION_START", client_context)
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT")
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context)
        self.assertTrue(triggered)

        triggered = mgr.trigger("OTHER_EVENT", client_context, additional={"key": "value"})
        self.assertTrue(triggered)
