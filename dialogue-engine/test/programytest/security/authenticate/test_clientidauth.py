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

from programy.security.authenticate.clientidauth import ClientIdAuthenticationService
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class MockClientIdAuthenticationService(ClientIdAuthenticationService):

    def __init__(self, brain_config):
        ClientIdAuthenticationService.__init__(self, brain_config)
        self.should_authorised = False
        self.raise_exception = False

    def user_auth_service(self, context):
        if self.raise_exception is True:
            raise Exception("Bad thing happen!")
        return self.should_authorised


class ClientIdAuthenticationServiceTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = ClientContext(client, "unknown")
        self._client_context.bot = Bot(BotConfiguration(), client)
        self._client_context.bot.configuration.conversations._max_histories = 3
        self._client_context.brain = self._client_context.bot.brain

    def test_init(self):
        service = ClientIdAuthenticationService(BrainSecurityAuthenticationConfiguration())
        self.assertIsNotNone(service)
        self._client_context._userid = "console"
        self.assertTrue(service.authenticate(self._client_context))
        self._client_context._userid = "anyone"
        self.assertFalse(service.authenticate(self._client_context))

    def test_authorise_success(self):
        service = MockClientIdAuthenticationService(BrainSecurityAuthenticationConfiguration())
        service.should_authorised = True
        self.assertTrue("console" in service.authorised)
        self._client_context._userid = "console"
        self.assertTrue(service.authenticate(self._client_context))
        self.assertFalse("unknown" in service.authorised)
        self._client_context._userid = "unknown"
        self.assertTrue(service.authenticate(self._client_context))
        self.assertTrue("unknown" in service.authorised)

    def test_authorise_failure(self):
        service = MockClientIdAuthenticationService(BrainSecurityAuthenticationConfiguration())
        service.should_authorised = False
        self.assertFalse("unknown" in service.authorised)
        self.assertFalse(service.authenticate(self._client_context))

    def test_authorise_exception(self):
        service = MockClientIdAuthenticationService(BrainSecurityAuthenticationConfiguration())
        service.should_authorised = True
        service.raise_exception = True
        self.assertFalse(service.authenticate(self._client_context._userid))
