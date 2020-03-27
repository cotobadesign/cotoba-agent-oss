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
import xml.etree.ElementTree as ET
import shutil

from programy.storage.stores.file.store.learnf import FileLearnfStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.client import TestClient


class FileLearnfStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = FileStorageConfiguration()
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_learnf(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)

        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)

        self.assertFalse(os.path.exists(learnf_fullpath))

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))

        category = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category, is_replace)

        self.assertTrue(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_save_learnf_remake(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)

        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)

        self.assertFalse(os.path.exists(learnf_fullpath))

        learnf_path = store._get_storage_path()
        store._ensure_dir_exists(learnf_path)
        with open(learnf_fullpath, "w+", encoding="utf-8") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<aiml>\n')
            file.close()

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))
        category = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category, is_replace)

        self.assertTrue(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_save_learnf_multi_pattern(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)

        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)

        self.assertFalse(os.path.exists(learnf_fullpath))

        learnf_path = store._get_storage_path()
        store._ensure_dir_exists(learnf_path)
        with open(learnf_fullpath, "w+", encoding="utf-8") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<aiml>\n')
            file.close()

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))
        category1 = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category1, is_replace)

        pattern = ET.Element('pattern')
        pattern.text = "HELLO1"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))
        category2 = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category2, is_replace)

        self.assertTrue(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_save_learnf_same_pattern(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)

        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)

        self.assertFalse(os.path.exists(learnf_fullpath))

        learnf_path = store._get_storage_path()
        store._ensure_dir_exists(learnf_path)
        with open(learnf_fullpath, "w+", encoding="utf-8") as file:
            file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
            file.write('<aiml>\n')
            file.close()

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))
        category = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category, is_replace)

        is_replace = True
        store.save_learnf(client_context, category, is_replace)

        self.assertTrue(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_load_learnf(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)
        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)
        self.assertFalse(os.path.exists(learnf_fullpath))

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))
        category = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category, is_replace)
        self.assertTrue(os.path.exists(learnf_fullpath))

        store.load_learnf(client_context)

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_load_learnf_no_path(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)
        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)
        self.assertFalse(os.path.exists(learnf_fullpath))

        store.load_learnf(client_context)

    def test_load_learnf_no_file(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        store._ensure_dir_exists(learnf_path)
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)
        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)
        self.assertFalse(os.path.exists(learnf_fullpath))

        store.load_learnf(client_context)

    def test_delete_learnf(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)
        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)
        self.assertFalse(os.path.exists(learnf_fullpath))

        pattern = ET.Element('pattern')
        pattern.text = "HELLO"
        topic = ET.Element('topic')
        topic.text = '*'
        that = ET.Element('that')
        that.text = '*'
        template = TemplateNode()
        template.append(TemplateWordNode("Hello"))
        category = LearnCategory(pattern, topic, that, template)

        is_replace = False
        store.save_learnf(client_context, category, is_replace)
        self.assertTrue(os.path.exists(learnf_fullpath))

        store.delete_learnf(client_context)
        self.assertFalse(os.path.exists(learnf_fullpath))

        shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_delete_learnf_no_file(self):
        config = FileStorageConfiguration()
        tmpdir = os.path.dirname(__file__) + os.sep + "learnf"
        config.learnf_storage._dirs = [tmpdir]
        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        learnf_path = store._get_storage_path()
        learnf_fullpath = store.create_learnf_path(client_context, learnf_path)
        if os.path.exists(learnf_fullpath):
            os.remove(learnf_fullpath)
        self.assertFalse(os.path.exists(learnf_fullpath))

        store.delete_learnf(client_context)
        self.assertFalse(os.path.exists(learnf_fullpath))
