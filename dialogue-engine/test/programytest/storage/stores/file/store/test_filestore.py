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
import os.path
import shutil

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class MockFileStore(FileStore):

    def __init__(self, engine):
        FileStore.__init__(self, engine)
        self._temp_folder = "/tmp/filestoretemp"

    def _get_storage_path(self):
        return self._temp_folder


class FileStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = FileStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_file_path_operations(self):
        self.assertEqual("/temp", FileStore._get_dir_from_path("/temp/files.txt"))
        self.assertEqual("/temp/files", FileStore._get_dir_from_path("/temp/files/files.txt"))
        self.assertEqual("./temp", FileStore._get_dir_from_path("./temp/files.txt"))
        self.assertEqual(".", FileStore._get_dir_from_path("./files.txt"))
        self.assertEqual("", FileStore._get_dir_from_path("files.txt"))

    def test_ensure_dir_exists(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        store = MockFileStore(engine)

        if os.path.exists(store._get_storage_path()):
            shutil.rmtree(store._get_storage_path())
        self.assertFalse(os.path.exists(store._get_storage_path()))

        store._ensure_dir_exists(store._get_storage_path())

        self.assertTrue(os.path.exists(store._get_storage_path()))
