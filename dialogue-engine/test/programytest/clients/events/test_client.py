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
import unittest.mock

from programy.clients.events.client import EventBotClient
from programy.clients.config import ClientConfigurationData

from programytest.clients.arguments import MockArgumentParser


class MockEventBotClient(EventBotClient):

    def __init__(self, id, argument_parser=None):
        EventBotClient.__init__(self, id, argument_parser)

    def get_client_configuration(self):
        return ClientConfigurationData("events")

    def load_license_keys(self):
        pass


class MockRunningEventBotClient(EventBotClient):

    def __init__(self, id, argument_parser=None):
        EventBotClient.__init__(self, id, argument_parser)
        self.prior = False
        self.ran = False
        self.post = False

    def get_client_configuration(self):
        return ClientConfigurationData("events")

    def load_license_keys(self):
        pass

    def prior_to_run_loop(self):
        self.prior = True

    def wait_and_answer(self):
        self.ran = True

    def post_run_loop(self):
        self.post = True


class EventBotClientTests(unittest.TestCase):

    def test_init_raw(self):
        arguments = MockArgumentParser()
        with self.assertRaises(NotImplementedError):
            EventBotClient("testevents", arguments)

    def test_init_actual(self):
        arguments = MockArgumentParser()
        client = MockEventBotClient("testevents", arguments)
        self.assertIsNotNone(client)

        with self.assertRaises(NotImplementedError):
            client.wait_and_answer()

    def test_init_running(self):
        arguments = MockArgumentParser()
        client = MockRunningEventBotClient("testevents", arguments)
        self.assertIsNotNone(client)

        client.run()

        self.assertTrue(client.prior)
        self.assertTrue(client.ran)
        self.assertTrue(client.post)
