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
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration
from programy.security.linking.accountlinker import BasicAccountLinkerService

from programytest.security.linking.accounlinker_asserts import AccountLinkerAsserts
import programytest.storage.engines as Engines


class SQLAccountLinkerServiceTests(AccountLinkerAsserts):

    def setUp(self):
        config = SQLStorageConfiguration()
        self.storage_engine = SQLStorageEngine(config)
        self.storage_engine.initialise()

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_init(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assertIsNotNone(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generate_key(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_key(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generate_expirary(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generate_expirary(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_happy_path(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_happy_path(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_user_client_link_already_exists(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_user_client_link_already_exists(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_provided_key_not_matched(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_provided_key_not_matched(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generated_key_not_matched(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generated_key_not_matched(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_generated_key_expired(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_generated_key_expired(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_lockout_after_max_retries(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_lockout_after_max_retries(mgr)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_unlink_user_from_client(self):
        mgr = BasicAccountLinkerService(self.storage_engine)
        self.assert_unlink_user_from_client(mgr)
