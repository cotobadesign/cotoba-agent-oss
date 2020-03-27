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

from programy.dynamic.variables.system.splitter import SentenceSplitter as SentenceSplitterVar
from programy.dialog.splitter.splitter import SentenceSplitter
from programy.context import ClientContext
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.config.bot.splitter import BotSentenceSplitterConfiguration
from programy.activate import Activatable

from programytest.client import TestClient


class SentenceSplitterDynamicVarTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = ClientContext(client, "testid")
        self._client_context.bot = Bot(BotConfiguration(), client)

        config = BotSentenceSplitterConfiguration()
        self._client_context.bot._sentence_splitter = SentenceSplitter.initiate_sentence_splitter(config)

    def test_splitter_active(self):
        dyn_var = SentenceSplitterVar(None)
        self.assertIsNotNone(dyn_var)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(active)
        self.assertEquals(Activatable.ON, active)

        dyn_var.set_value(self._client_context, Activatable.OFF)
        active = dyn_var.get_value(self._client_context)
        self.assertIsNotNone(active)
        self.assertEquals(Activatable.OFF, active)
