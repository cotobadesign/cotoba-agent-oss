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
import os
import os.path

from programy.storage.stores.file.store.usergroups import FileUserGroupStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.security.authorise.usergroupsauthorisor import BasicUserGroupAuthorisationService
from programy.storage.stores.file.config import FileStoreConfiguration


class FileSpellingStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_users_and_groups(self):
        config = FileStorageConfiguration()
        config._usergroups_storage = FileStoreConfiguration(file=os.path.dirname(__file__) + os.sep + "data" + os.sep + "security" + os.sep + "roles.yaml",
                                                            format="yaml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileUserGroupStore(engine)

        store.empty()

        config = unittest.mock.Mock()
        config.usergroups = "Test"
        usersgroupsauthorisor = BasicUserGroupAuthorisationService(config)
        store.load_usergroups(usersgroupsauthorisor)

        self.assertTrue(usersgroupsauthorisor.authorise("console", "admin"))
        with self.assertRaises(Exception):
            self.assertFalse(usersgroupsauthorisor.authorise("offred", "admin"))
