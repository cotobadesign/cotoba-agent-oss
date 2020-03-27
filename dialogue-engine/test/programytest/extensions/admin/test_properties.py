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

from programy.dialog.question import Question
from programy.extensions.admin.properties import PropertiesAdminExtension
from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class PropertiesAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(PropertiesAdminExtensionClient, self).load_configuration(arguments, subs)


class PropertiesAdminExtensionTests(unittest.TestCase):

    def test_get_bot_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.properties.add_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_bot_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET BOT XXXXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_user_local_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question()
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)
        question.set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER VAR PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_user_Local_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER VAR XXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_user_global_known(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.bot.get_conversation(client_context).set_property("PROP1", "Value1")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER NAME PROP1")
        self.assertIsNotNone(result)
        self.assertEqual("Value1", result)

    def test_get_user_global_unknown(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "GET USER NAME XXX")
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_get_bot(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        client_context.bot.get_conversation(client_context)

        result = extension.execute(client_context, "BOT")
        self.assertIsNotNone(result)
        self.assertEqual("Properties:<br /><ul></ul><br />", result)

    def test_get_user(self):

        client = PropertiesAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = PropertiesAdminExtension()
        self.assertIsNotNone(extension)

        client_context.bot.get_conversation(client_context)

        result = extension.execute(client_context, "USER")
        self.assertIsNotNone(result)
        self.assertEqual("Properties:<br /><ul><li>topic = *</li></ul><br />", result)
