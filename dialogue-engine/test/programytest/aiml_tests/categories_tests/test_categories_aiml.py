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
import shutil
import logging

from programytest.client import TestClient

from programy.parser.aiml_parser import AIMLLoader, AIMLParser
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.storage.stores.file.store.config import FileStoreConfiguration
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.factory import StorageFactory


class AimlTestClient(TestClient):

    TEST_DIRECTORY = "debug"
    ERRORS_FILE = "errors.txt"
    DUPLICATES_FILE = "duplicates.txt"

    def __init__(self, aiml_type=None, category_file=None, set_store=True):
        self._aiml_type = aiml_type
        self._category_file = category_file
        self._set_store = set_store
        TestClient.__init__(self)

    def load_storage(self):
        super(AimlTestClient, self).load_storage()
        self.add_default_stores()

        bot_config = self.configuration.client_configuration.configurations[0]
        brain_config = bot_config.configurations[0]
        if self._aiml_type == "errors":
            brain_config.debugfiles._save_errors = True
            if self._set_store is True:
                self.add_errors_store()
        elif self._aiml_type == "duplicates":
            brain_config.debugfiles._save_duplicates = True
            if self._set_store is True:
                self.add_duplicates_store()

        if self._category_file is None:
            self.add_categories_store([os.path.dirname(__file__)])
        else:
            aimlfile = os.path.dirname(__file__) + os.sep + self._category_file
            self._file_store_config._categories_storage = FileStoreConfiguration(dirs=aimlfile, format="xml", extension="aiml", encoding="utf-8", delete_on_start=False)
            self.storage_factory._storage_engines[StorageFactory.CATEGORIES] = self._storage_engine
            self.storage_factory._store_to_engine_map[StorageFactory.CATEGORIES] = self._storage_engine

    def add_errors_store(self):
        config = FileStoreConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        tmpfile = tmpdir + os.sep + self.ERRORS_FILE
        config._dirs = [tmpfile]
        config._has_single_file = True
        self._file_store_config._errors_storage = config
        self.storage_factory._storage_engines[StorageFactory.ERRORS] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.ERRORS] = self._storage_engine

    def add_duplicates_store(self):
        config = FileStoreConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + self.TEST_DIRECTORY
        tmpfile = tmpdir + os.sep + self.DUPLICATES_FILE
        config._dirs = [tmpfile]
        config._has_single_file = True
        self._file_store_config._duplicates_storage = config
        self.storage_factory._storage_engines[StorageFactory.DUPLICATES] = self._storage_engine
        self.storage_factory._store_to_engine_map[StorageFactory.DUPLICATES] = self._storage_engine


class TempAimlFiles(object):

    def __init__(self, file=None, dirs=None, extension=None):
        if file is not None:
            if type(file) is list:
                self._file = None
                self._files = file
            else:
                self._file = file
                self._files = None
        self._directories = dirs
        self._extension = extension

    @property
    def file(self):
        return self._file

    @property
    def files(self):
        return self._files

    @property
    def directories(self):
        return self._directories

    @property
    def extension(self):
        return self._extension


class TempFiles(object):

    def __init__(self, file=None, dirs=None, extension=None):
        self._aiml_files = TempAimlFiles(file, dirs, extension)

    @property
    def aiml_files(self):
        return self._aiml_files


class TempDefaults(object):

    def __init__(self, leanfpath=None):
        self._learnf_path = leanfpath

    @property
    def learnf_path(self):
        return self._learnf_path


class TempAimlConfiguraton(object):

    def __init__(self, file=None, dirs=None, extension=None, learnfpath=None):

        self._files = TempFiles(file, dirs, extension)
        self._defaults = TempDefaults(learnfpath)

    @property
    def files(self):
        return self._files

    @property
    def defaults(self):
        return self._defaults


class AIMLLoaderTests(unittest.TestCase):

    def test_load_file_contents(self):
        client = TestClient()
        brain = client.bot_factory.bot('bot').brain

        aimlfile = os.path.dirname(__file__) + os.sep + "basic.aiml"
        loader = AIMLLoader(AIMLParser(brain))
        loader.load_file_contents("TestClient", aimlfile)


class AIMLParserTests(unittest.TestCase):

    def test_load_single_file(self):
        client = TestClient()
        brain = client.bot_factory.bot('bot').brain

        aimlfile = os.path.dirname(__file__) + os.sep + "basic.aiml"
        parser = AIMLParser(brain)

        configuration = TempAimlConfiguraton(file=aimlfile)
        parser.load_single_file(configuration)

    def test_load_files_from_directory(self):
        client = TestClient()
        brain = client.bot_factory.bot('bot').brain

        aimldir = os.path.dirname(__file__) + os.sep
        aimlfiles = ["basic.aiml"]
        parser = AIMLParser(brain)

        configuration = TempAimlConfiguraton(file=aimlfiles, dirs=aimldir, extension='aiml')
        parser.load_files_from_directory(configuration)

    def test_load_files_from_directory_empty(self):
        client = TestClient()
        brain = client.bot_factory.bot('bot').brain

        aimldir = os.path.dirname(__file__) + os.sep
        aimlfiles = []
        parser = AIMLParser(brain)

        configuration = TempAimlConfiguraton(file=aimlfiles, dirs=aimldir, extension='aiml')
        parser.load_files_from_directory(configuration)

    def test_load_learnf_files_from_directory(self):
        client = TestClient()
        brain = client.bot_factory.bot('bot').brain

        learnf_path = os.path.dirname(__file__) + os.sep
        parser = AIMLParser(brain)

        configuration = TempAimlConfiguraton(learnfpath=learnf_path, extension='aiml')
        parser.load_learnf_files_from_directory(configuration)

    def test_load_learnf_files_none_directory(self):
        client = TestClient()
        brain = client.bot_factory.bot('bot').brain

        parser = AIMLParser(brain)

        configuration = TempAimlConfiguraton(extension='aiml')
        parser.load_learnf_files_from_directory(configuration)


class DebugFilesTests(unittest.TestCase):
    def test_category_erros(self):
        tmpdir = os.path.dirname(__file__) + os.sep + AimlTestClient.TEST_DIRECTORY

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        AimlTestClient(aiml_type="errors", category_file="with_errors.aiml")

        tmpfile = tmpdir + os.sep + AimlTestClient.ERRORS_FILE
        self.assertTrue(os.path.exists(tmpfile))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_category_duplicatess(self):
        tmpdir = os.path.dirname(__file__) + os.sep + AimlTestClient.TEST_DIRECTORY

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        AimlTestClient(aiml_type="duplicates", category_file="with_duplicates.aiml")

        tmpfile = tmpdir + os.sep + AimlTestClient.DUPLICATES_FILE
        self.assertTrue(os.path.exists(tmpfile))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_category_erros_no_store(self):
        tmpdir = os.path.dirname(__file__) + os.sep + AimlTestClient.TEST_DIRECTORY

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        AimlTestClient(aiml_type="errors", category_file="with_errors.aiml", set_store=False)

        tmpfile = tmpdir + os.sep + AimlTestClient.ERRORS_FILE
        self.assertFalse(os.path.exists(tmpfile))

    def test_category_duplicatess_no_store(self):
        tmpdir = os.path.dirname(__file__) + os.sep + AimlTestClient.TEST_DIRECTORY

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        AimlTestClient(aiml_type="duplicates", category_file="with_duplicates.aiml", set_store=False)

        tmpfile = tmpdir + os.sep + AimlTestClient.DUPLICATES_FILE
        self.assertFalse(os.path.exists(tmpfile))

    def test_category_erros_none_logger(self):
        logging.getLogger().setLevel(level=logging.CRITICAL)
        tmpdir = os.path.dirname(__file__) + os.sep + AimlTestClient.TEST_DIRECTORY

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        AimlTestClient(aiml_type="errors", category_file="with_errors.aiml")

        tmpfile = tmpdir + os.sep + AimlTestClient.ERRORS_FILE
        self.assertTrue(os.path.exists(tmpfile))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_category_duplicatess_none_logger(self):
        logging.getLogger().setLevel(level=logging.CRITICAL)
        tmpdir = os.path.dirname(__file__) + os.sep + AimlTestClient.TEST_DIRECTORY

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        AimlTestClient(aiml_type="duplicates", category_file="with_duplicates.aiml")

        tmpfile = tmpdir + os.sep + AimlTestClient.DUPLICATES_FILE
        self.assertTrue(os.path.exists(tmpfile))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))
