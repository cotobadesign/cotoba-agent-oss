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

from programy.extensions.admin.client import ClientAdminExtension
from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class ClientAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(ClientAdminExtensionClient, self).load_configuration(arguments, subs)


class ClientAdminExtensionTests(unittest.TestCase):

    def test_client_commands(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()
        self.assertEqual("LIST BOTS, LIST BRAINS, DUMP BRAIN", extension.execute(client_context, "COMMANDS"))

    def test_client_list_bots(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("bot", extension.execute(client_context, "LIST BOTS"))

    def test_client_list_brains(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("brain", extension.execute(client_context, "LIST BRAINS bot"))

    def test_client_dump_brain(self):
        client = ClientAdminExtensionClient()
        client_context = client.create_client_context("testid")

        extension = ClientAdminExtension()

        self.assertEqual("Brain dumped, see config for location", extension.execute(client_context, "DUMP BRAIN bot brain"))
