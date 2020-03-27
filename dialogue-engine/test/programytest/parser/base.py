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

from programy.bot import Bot
from programytest.custom import CustomAssertions
from programy.config.bot.bot import BotConfiguration
from programy.context import ClientContext
from programytest.client import TestClient


class TestBot(Bot):

    def __init__(self, bot_config, client):
        Bot.__init__(self, bot_config, client)
        self._response = "Unknown"

    @property
    def response(self):
        return self._response

    @response.setter
    def response(self, text):
        self._response = text

    def ask_question(self, clientid, text, srai=False):
        return self._response


class ParserTestsBaseClass(unittest.TestCase, CustomAssertions):

    def setUp(self):
        client = TestClient()
        client.add_default_stores()
        self._client_context = ClientContext(client, "testid")
        self._client_context.bot = TestBot(BotConfiguration(), client)
        self._client_context.brain = self._client_context.bot.brain
