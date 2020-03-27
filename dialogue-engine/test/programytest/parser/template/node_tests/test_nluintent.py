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
from programy.parser.template.nodes.nluintent import TemplateNluIntentNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateNluIntentNode(TemplateNluIntentNode):
    def __init__(self):
        TemplateNluIntentNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateNluIntentNodeTests(ParserTestsBaseClass):

    def test_nluintent(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("nlu_intent")
        node._itemName = TemplateWordNode("score")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [{"intent": "nlu_intent", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("0.9", result)

    def test_nluintent_with_index(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("nlu_intent")
        node._itemName = TemplateWordNode("score")
        node._index = TemplateWordNode("1")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [{"intent": "nlu_intent", "score": 0.9}, {"intent": "nlu_intent", "score": 0.75}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("0.75", result)

    def test_nluintent_with_index_over(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("score")
        node._index = TemplateWordNode("2")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [{"intent": "nlu_intent", "score": 0.9}, {"intent": "nlu_intent", "score": 0.75}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluintent_count(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("count")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [{"intent": "nlu_intent", "score": 0.9}, {"intent": "nlu_intent", "score": 0.75}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("2", result)

    def test_nluintent_intent_count(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("nlu_intent1")
        node._itemName = TemplateWordNode("count")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [{"intent": "nlu_intent", "score": 0.9}, {"intent": "nlu_intent1", "score": 0.75}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("1", result)

    def test_to_xml_nluintent(self):
        root = TemplateNode()
        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("nlu_intent")
        node._itemName = TemplateWordNode("score")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><nluintent><name>nlu_intent</name><item>score</item></nluintent></template>', xml_str)

    def test_to_xml_nluintent_with_index(self):
        root = TemplateNode()
        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("score")
        node._index = TemplateWordNode("0")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><nluintent><name>*</name><item>score</item><index>0</index></nluintent></template>', xml_str)

    def test_nluintent_no_intent(self):
        root = TemplateNode()
        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("nlu_intent")
        node._itemName = TemplateWordNode("score")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        nlu_result = '{"intents": [{"intent": "intent_x", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluintent_no_item(self):
        root = TemplateNode()
        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("nlu_intent")
        node._itemName = TemplateWordNode("score")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        nlu_result = '{"intents": [{"intent": "nlu_intent"}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluintent_no_nlu_result(self):
        root = TemplateNode()
        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("score")
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_nluintent_invalid_index(self):
        root = TemplateNode()
        node = TemplateNluIntentNode()
        node._intentName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("score")
        node._index = TemplateWordNode("x")
        self.assertIsNotNone(node)
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        nlu_result = '{"intents": [{"intent": "nlu_intent", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("0.9", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateNluIntentNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
