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

from programy.storage.stores.file.store.binaries import FileBinariesStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class PretendAimlParser(object):

    def __init__(self, name):
        self._name = name


class FileBinariesStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBinariesStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_load_binaries(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "braintree"
        tmpfile = tmpdir + os.sep + "braintree.bin"
        config.binaries_storage._dirs = [tmpfile]
        config.binaries_storage._has_single_file = True
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileBinariesStore(engine)

        aiml_parser = PretendAimlParser("pretend1")

        path = store._get_dir_from_path(store._get_storage_path())
        if os.path.exists(path):
            shutil.rmtree(path)
        self.assertFalse(os.path.exists(path))

        store.save_binary(aiml_parser)

        self.assertTrue(os.path.exists(store._get_storage_path()))

        aiml_parser2 = store.load_binary()
        self.assertIsNotNone(aiml_parser2)

        self.assertEqual(aiml_parser2._name, "pretend1")

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))
