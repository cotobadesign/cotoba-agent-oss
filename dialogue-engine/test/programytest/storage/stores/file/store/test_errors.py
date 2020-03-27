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
import os.path
import shutil

from programy.storage.stores.file.store.errors import FileErrorsStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileErrorsStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileErrorsStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_errors(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "errors"
        tmpfile = tmpdir + os.sep + "errors.txt"
        config.errors_storage._dirs = [tmpfile]
        config.errors_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileErrorsStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        store.empty()

        errors = [["aiml1.xml", "10", "20", "1", "5", "node", "Error_1"]]
        store.save_errors(errors)
        self.assertTrue(os.path.exists(store._get_storage_path()))

        store.empty()
        self.assertFalse(os.path.exists(store._get_storage_path()))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_load_errors(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "errors"
        tmpfile = tmpdir + os.sep + "errors.txt"
        config.errors_storage._dirs = [tmpfile]
        config.errors_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileErrorsStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        store.empty()

        errors = [["aiml1.xml", "10", "20", "1", "5", "node", "Error_1"]]
        store.save_errors(errors)
        self.assertTrue(os.path.exists(store._get_storage_path()))

        errorInfo = store.load_errors()
        self.assertIsNotNone(errorInfo)
        self.assertIsNotNone(errorInfo['errors'])
        errors = errorInfo['errors']
        error = errors[0]
        self.assertEqual("aiml1.xml", error['file'])

        store.empty()
        self.assertFalse(os.path.exists(store._get_storage_path()))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_load_errors_no_file(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "errors"
        tmpfile = tmpdir + os.sep + "errors.txt"
        config.errors_storage._dirs = [tmpfile]
        config.errors_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileErrorsStore(engine)

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        errorInfo = store.load_errors()
        self.assertIsNone(errorInfo)
