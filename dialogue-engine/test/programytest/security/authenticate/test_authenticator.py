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

from programy.security.authenticate.authenticator import Authenticator
from programy.config.brain.security import BrainSecurityConfiguration
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext

from programytest.client import TestClient


class AuthenticatorTests(unittest.TestCase):

    def test_authenticator_with_empty_config(self):
        client = TestClient()
        client_context = ClientContext(client, "console")
        client_context.bot = Bot(BotConfiguration(), client)
        client_context.bot.configuration.conversations._max_histories = 3
        client_context.brain = client_context.bot.brain

        service = Authenticator(BrainSecurityConfiguration("authentication"))
        self.assertIsNotNone(service)
        self.assertIsNotNone(service.configuration)
        self.assertIsNone(service.get_default_denied_srai())
        self.assertFalse(service.authenticate(client_context))
