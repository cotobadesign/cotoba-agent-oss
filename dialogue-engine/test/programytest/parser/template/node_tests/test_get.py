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
import xml.etree.ElementTree as ET

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateGetNode(TemplateGetNode):
    def __init__(self):
        TemplateGetNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateGetNodeTests(ParserTestsBaseClass):

    def test_typevar_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "var"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.set_property("name", "keith")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_typevar_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "var"
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get var="name" /></template>', xml_str)

    def test_typevar_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "var"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_typedata_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "data"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_data_property("name", "keith")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_typedata_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "data"
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get data="name" /></template>', xml_str)

    def test_typedata_get_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "data"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)
        self.assertEqual("[GET [data] - [WORD]name]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_typedata_no_name(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.append(TemplateWordNode("Fred"))
        node.property_type = "data"
        self.assertIsNotNone(node)
        self.assertEqual("[GET [data] - None]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        with self.assertRaises(Exception):
            root.resolve(self._client_context)

    def test_typename_get(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "name"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_property("name", "keith")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

    def test_to_xml_typename_get(self):
        root = TemplateNode()
        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "name"
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get name="name" /></template>', xml_str)

    def test_typename_get_no_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "name"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)
        self.assertEqual("[GET [name] - [WORD]name]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_unknown_from_config(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "name"
        node.append(TemplateWordNode("Fred"))
        self.assertIsNotNone(node)
        self.assertEqual("[GET [name] - [WORD]name]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.bot.brain.configuration.defaults._default_get = None

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_typename_no_name(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateGetNode()
        node.append(TemplateWordNode("Fred"))
        node.property_type = "name"
        self.assertIsNotNone(node)
        self.assertEqual("[GET [name] - None]", node.to_string())

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        with self.assertRaises(Exception):
            root.resolve(self._client_context)

    def test_tuples(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        select = TemplateSelectNode()
        self.assertIsNotNone(select)

        node = TemplateGetNode()
        node.name = TemplateWordNode("?x ?y")
        node.tuples = select

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[GET [Tuples] - ([WORD]?x ?y)]", node.to_string())

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><get tuples="?x ?y"><select /></get></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateGetNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
