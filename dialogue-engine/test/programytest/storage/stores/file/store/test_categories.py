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
import os
import os.path

from programytest.storage.asserts.store.assert_category import CategoryStoreAsserts
from programy.storage.stores.file.store.categories import FileCategoryStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration


class MockAIMLParser(object):

    def __init__(self):
        self._parsed_files = []

    def parse_from_file(self, filename, userid="*"):
        self._parsed_files.append(filename)


class FileCategoryStoreTests(CategoryStoreAsserts):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_load_from_text_file(self):
        config = FileStorageConfiguration()
        file = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories" + os.sep + "kinghorn.aiml"
        self.assertTrue(os.path.exists(file))
        config._categories_storage = FileStoreConfiguration(file=file, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(1, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))

    def test_load_from_text_check_extention(self):
        config = FileStorageConfiguration()
        file = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories" + os.sep + "kinghorn.aiml"
        self.assertTrue(os.path.exists(file))
        config._categories_storage = FileStoreConfiguration(file=file, extension="txt", format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(0, len(parser._parsed_files))

    def test_load_from_test_dir_no_subdir(self):
        config = FileStorageConfiguration()
        dirs = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"
        self.assertTrue(os.path.exists(dirs))
        config._categories_storage = FileStoreConfiguration(dirs=[dirs], extension="aiml", subdirs=False, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(1, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))

    def test_load_from_test_dir_with_subdir(self):
        config = FileStorageConfiguration()
        dirs = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"
        self.assertTrue(os.path.exists(dirs))
        config._categories_storage = FileStoreConfiguration(dirs=[dirs], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(3, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))
        self.assertTrue(parser._parsed_files[1].endswith("/fife.aiml"))
        self.assertTrue(parser._parsed_files[2].endswith("/scotland.aiml"))

    def test_load_from_test_dir_with_subdir_not_extst(self):
        config = FileStorageConfiguration()
        dirs = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories_1"
        self.assertTrue(os.path.exists(dirs))
        config._categories_storage = FileStoreConfiguration(dirs=[dirs], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(2, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/fife.aiml"))
        self.assertTrue(parser._parsed_files[1].endswith("/kinghorn.aiml"))

    def test_load_from_test_dir_multi_dir(self):
        config = FileStorageConfiguration()
        dir = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories_2"
        dir1 = dir + os.sep + "folder1"
        dir2 = dir + os.sep + "folder2"
        self.assertTrue(os.path.exists(dir1))
        self.assertTrue(os.path.exists(dir2))
        config._categories_storage = FileStoreConfiguration(dirs=[dir1, dir2], extension="aiml", subdirs=True, format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load_all(parser)

        self.assertEqual(2, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/fife.aiml"))
        self.assertTrue(parser._parsed_files[1].endswith("/kinghorn.aiml"))

    def test_load_file(self):
        config = FileStorageConfiguration()
        dirs = os.path.dirname(__file__) + os.sep + "data" + os.sep + "categories"
        filename = dirs + os.sep + "kinghorn.aiml"
        self.assertTrue(os.path.exists(filename))
        config._categories_storage = FileStoreConfiguration(dirs=[dirs], format="xml", encoding="utf-8", delete_on_start=False)
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileCategoryStore(engine)

        parser = MockAIMLParser()
        store.load(parser, filename)

        self.assertEqual(1, len(parser._parsed_files))
        self.assertTrue(parser._parsed_files[0].endswith("/kinghorn.aiml"))
