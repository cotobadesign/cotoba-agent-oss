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
from programy.parser.template.nodes.set import TemplateSetNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateSetNode(TemplateSetNode):
    def __init__(self):
        TemplateSetNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSetNodeTests(ParserTestsBaseClass):

    def test_typevar_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.property_type = "var"
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello")
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        result = node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", question.property("name"))

    def test_to_xml_typevar_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "var"
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set var="name">keith</set></template>', xml_str)

    def test_typedata_set(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSetNode()
        self.assertIsNotNone(node)
        node.name = TemplateWordNode("name")
        node.property_type = "data"
        node.append(TemplateWordNode("keith"))

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)

        result = node.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("keith", result)

        self.assertEqual("keith", conversation.data_property("name"))

    def test_to_xml_typedata_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "data"
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set data="name">keith</set></template>', xml_str)

    def test_to_xml_typename_set(self):
        root = TemplateNode()
        node = TemplateSetNode()
        node.name = TemplateWordNode("name")
        node.property_type = "name"
        root.append(node)
        node.append(TemplateWordNode("keith"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><set name="name">keith</set></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSetNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
