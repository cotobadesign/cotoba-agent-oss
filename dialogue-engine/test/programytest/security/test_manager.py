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

from programy.security.manager import SecurityManager
from programy.config.brain.securities import BrainSecuritiesConfiguration
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.config.brain.security import BrainSecurityAccountLinkerConfiguration
from programytest.client import TestClient


class TestSecurityManager(unittest.TestCase):

    def test_init(self):
        config = BrainSecuritiesConfiguration()
        config._authorisation = BrainSecurityAuthorisationConfiguration()
        config._authentication = BrainSecurityAuthenticationConfiguration()
        config._account_linker = BrainSecurityAccountLinkerConfiguration()

        mgr = SecurityManager(config)
        self.assertIsNotNone(mgr)

        client = TestClient()

        mgr.load_security_services(client)

        self.assertIsNotNone(mgr.authorisation)
        self.assertIsNotNone(mgr.authentication)
        self.assertIsNotNone(mgr.account_linker)
