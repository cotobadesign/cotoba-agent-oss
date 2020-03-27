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
import xml.etree.ElementTree as ET

from programy.storage.stores.nosql.redis.store.learnf import RedisLearnfStore
from programy.storage.stores.nosql.redis.engine import RedisStorageEngine
from programy.storage.stores.nosql.redis.config import RedisStorageConfiguration
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.client import TestClient


class RedisLearnfStoreTests(unittest.TestCase):

    def test_initialise(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_save_learnf(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

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

    def test_save_learnf_multi_pattern(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

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

    def test_save_learnf_same_pattern(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

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

    def test_load_learnf(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

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

        store.load_learnf(client_context)

    def test_load_learnf_no_file(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        store.load_learnf(client_context)

    def test_delete_learnf(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

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

        store.delete_learnf(client_context)

    def test_delete_learnf_no_file(self):
        config = RedisStorageConfiguration()
        engine = RedisStorageEngine(config)
        engine.initialise()
        store = RedisLearnfStore(engine)

        test_client = TestClient()
        client_context = test_client.create_client_context("test1")

        store.delete_learnf(client_context)
