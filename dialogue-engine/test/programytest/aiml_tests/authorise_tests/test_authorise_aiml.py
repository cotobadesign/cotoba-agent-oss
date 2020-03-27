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
import os

from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class AuthoriseTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(AuthoriseTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(AuthoriseTestClient, self).load_configuration(arguments)
        self.configuration.client_configuration.configurations[0].configurations[0].security._authorisation = BrainSecurityAuthorisationConfiguration()
        self.configuration.client_configuration.configurations[0].configurations[0].security.authorisation._classname = \
            "programy.security.authorise.usergroupsauthorisor.BasicUserGroupAuthorisationService"
        self.configuration.client_configuration.configurations[0].configurations[0].security.authorisation._denied_srai = "ACCESS_DENIED"
        self.configuration.client_configuration.configurations[0].configurations[0].security.authorisation._usergroups = os.path.dirname(__file__) + os.sep + "usergroups.yaml"


class AuthoriseAIMLTests(unittest.TestCase):

    def setUp(self):
        client = AuthoriseTestClient()
        self._client_context = client.create_client_context("console")

    def test_authorise_allowed(self):
        response = self._client_context.bot.ask_question(self._client_context, "ALLOW ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Access Allowed.')

    def test_authorise_denied(self):
        response = self._client_context.bot.ask_question(self._client_context, "DENY ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Sorry, but you are not authorised to access this content!')

    def test_authorise_denied_custom_response(self):
        response = self._client_context.bot.ask_question(self._client_context, "CUSTOM DENY ACCESS")
        self.assertIsNotNone(response)
        self.assertEqual(response, 'Sorry, but no chance!')
