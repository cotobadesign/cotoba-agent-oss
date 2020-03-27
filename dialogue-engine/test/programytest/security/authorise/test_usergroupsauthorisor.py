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

from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.security.authorise.authorisor import AuthorisationException
from programytest.client import TestClient


class BasicUserGroupAuthorisationServiceTests(unittest.TestCase):

    def test_usersgroups(self):
        client = TestClient()

        client.add_usergroups_store()

        service_config = BrainSecurityAuthorisationConfiguration("authorisation")
        service_config._usergroups = os.path.dirname(__file__) + os.sep + "test_usergroups.yaml"

        service = BasicUserGroupAuthorisationService(service_config)
        self.assertIsNotNone(service)

        service.initialise(client)

        self.assertTrue(service.authorise("console", "root"))
        self.assertFalse(service.authorise("console", "uber"))

        with self.assertRaises(AuthorisationException):
            service.authorise("anyone", "root")
