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
from programy.parser.template.nodes.request import TemplateRequestNode
from programy.dialog.conversation import Conversation
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateRequestNode(TemplateRequestNode):
    def __init__(self):
        TemplateRequestNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateRequestNodeTests(ParserTestsBaseClass):

    def test_to_str_defaults(self):
        node = TemplateRequestNode()
        self.assertEqual("[REQUEST]", node.to_string())

    def test_to_str_no_defaults(self):
        node = TemplateRequestNode(index=2)
        self.assertEqual("[REQUEST index=2]", node.to_string())

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode()
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><request /></template>", xml_str)

    def test_to_xml_no_defaults(self):
        root = TemplateNode()
        node = TemplateRequestNode(index=3)
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><request index="3" /></template>', xml_str)

    def test_resolve_with_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(1, node.index)

        conversation = Conversation(self._client_context)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        question = Question.create_from_text(self._client_context, "What did you say")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_resolve_with_no_defaults(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode(index=1)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(1, node.index)

        conversation = Conversation(self._client_context)
        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        question = Question.create_from_text(self._client_context, "What did you say")
        question.current_sentence()._response = "Hello matey"
        conversation._questions.append(question)

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "Hello world")

    def test_resolve_no_sentence(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateRequestNode(index=3)
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertEqual(3, node.index)

        conversation = Conversation(self._client_context)

        question = Question.create_from_text(self._client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        conversation.record_dialog(question)

        question = Question.create_from_text(self._client_context, "How are you. Are you well")
        question.current_sentence()._response = "Fine thanks"
        conversation.record_dialog(question)

        self._client_context.bot._conversation_mgr._conversations["testid"] = conversation

        response = root.resolve(self._client_context)
        self.assertIsNotNone(response)
        self.assertEqual(response, "")

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateRequestNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
