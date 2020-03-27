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

from programytest.storage.asserts.store.assert_sets import SetStoreAsserts

from programy.storage.stores.sql.store.sets import SQLSetsStore
from programy.storage.stores.sql.engine import SQLStorageEngine
from programy.storage.stores.sql.config import SQLStorageConfiguration

import programytest.storage.engines as Engines


class SQLSetsStoreTests(SetStoreAsserts):

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_initialise(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_set_storage(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_set_storage(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_text(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_from_text(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_from_text_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_from_text_file(store)

    @unittest.skipIf(Engines.sql is False, Engines.sql_disabled)
    def test_upload_text_files_from_directory_no_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_text_files_from_directory_no_subdir(store)

    @unittest.skip("CSV not supported yet")
    def test_upload_from_csv_file(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_from_csv_file(store)

    @unittest.skip("CSV not supported yet")
    def test_upload_csv_files_from_directory_with_subdir(self):
        config = SQLStorageConfiguration()
        engine = SQLStorageEngine(config)
        engine.initialise()
        store = SQLSetsStore(engine)

        self.assert_upload_csv_files_from_directory_with_subdir(store)
