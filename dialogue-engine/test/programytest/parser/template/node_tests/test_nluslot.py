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
from programy.parser.template.nodes.nluslot import TemplateNluSlotNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateNluSlotNode(TemplateNluSlotNode):
    def __init__(self):
        TemplateNluSlotNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateNluSlotNodeTests(ParserTestsBaseClass):

    def test_nluslot(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("entity")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value", result)

    def test_nluslot_with_index(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("entity")
        node._index = TemplateWordNode("1")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value1"}, {"slot": "nlu_slot", "entity": "value2"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value2", result)

    def test_nluslot_with_index_over(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("entity")
        node._index = TemplateWordNode("2")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value1"}, {"slot": "nlu_slot", "entity": "value2"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluslot_count(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("count")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value1"}, {"slot": "nlu_slot", "entity": "value2"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("2", result)

    def test_nluslot_slot_count(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot1")
        node._itemName = TemplateWordNode("count")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value1"}, {"slot": "nlu_slot1", "entity": "value2"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("1", result)

    def test_to_xml_nluslot(self):
        root = TemplateNode()
        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("entity")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><nluslot><name>nlu_slot</name><item>entity</item></nluslot></template>', xml_str)

    def test_to_xml_nluslot_with_index(self):
        root = TemplateNode()
        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("*")
        node._itemName = TemplateWordNode("entity")
        node._index = TemplateWordNode("0")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><nluslot><name>*</name><item>entity</item><index>0</index></nluslot></template>', xml_str)

    def test_nluslot_no_slot(self):
        root = TemplateNode()
        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("entity")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot_x", "entity": "value"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluslot_no_item(self):
        root = TemplateNode()
        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("startOffset")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluslot_no_nlu_result(self):
        root = TemplateNode()
        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("startOffset")
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_nluslot_invalid_index(self):
        root = TemplateNode()
        node = TemplateNluSlotNode()
        node._slotName = TemplateWordNode("nlu_slot")
        node._itemName = TemplateWordNode("entity")
        node._index = TemplateWordNode("x")
        self.assertIsNotNone(node)
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        nlu_result = '{"intents": [], "slots": [{"slot": "nlu_slot", "entity": "value"}]}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateNluSlotNode()
        root.append(node)

        with self.assertRaises(Exception):
            result = root.resolve(self._client_context)
