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
from programy.parser.template.nodes.json import TemplateJsonNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.dialog.question import Question

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateJsonNode(TemplateJsonNode):
    def __init__(self):
        TemplateJsonNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateJsonNodeTests(ParserTestsBaseClass):

    #  GET

    def test_json_get_typename(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_property("name_json", '{"key_name": "value_name"}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value_name", result)

    def test_json_get_typedata(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_data_property("data_json", '{"key_data": "value_data"}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value_data", result)

    def test_json_get_typevar(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.set_property("var_json", '{"key_var": "value_var"}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value_var", result)

    def test_json_get_key(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._item = TemplateWordNode("key")
        node._index = TemplateWordNode("2")
        node._key = TemplateWordNode("key_data")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_data_property("data_json", '{"key_data" : {"key_1": "val_1", "key_2": "val_2", "key_3": "val_3"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("key_3", result)

    def test_json_get_len(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._function = TemplateWordNode("len")
        node._key = TemplateWordNode("key_data")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_data_property("data_json", '{"key_data": ["list_1", "list_2", "list_3"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("3", result)

    def test_json_get_empty(self):
        root = TemplateNode()

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": ""}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('""', result)

    def test_json_get_int_value(self):
        root = TemplateNode()

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": 100}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("100", result)

        node._function = TemplateWordNode("len")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("1", result)

        node._function = None
        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("100", result)

        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("100", result)

        node._index = TemplateWordNode("-1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("100", result)

        node._index = TemplateWordNode("1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

        node._index = TemplateWordNode("-2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_list(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": ["list_1", "list_2", "list_3"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('["list_1", "list_2", "list_3"]', result)

    def test_json_get_list_element(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("list_1", result)

        node._index = TemplateWordNode("1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("list_2", result)

        node._index = TemplateWordNode("2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("list_3", result)

        node._index = TemplateWordNode("3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_list_element_from_end(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("-1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("list_3", result)

        node._index = TemplateWordNode("-2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("list_2", result)

        node._index = TemplateWordNode("-3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("list_1", result)

        node._index = TemplateWordNode("-4")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_dict(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"dic_1": "val_1", "dic_2": "val_2", "dic_3": "val_3"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('{"dic_1": "val_1", "dic_2": "val_2", "dic_3": "val_3"}', result)

    def test_json_get_dict_key(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._item = TemplateWordNode("key")
        node._key = TemplateWordNode("key_data")
        root.append(node)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"dic_1": "val_1", "dic_2": "val_2", "dic_3": "val_3"}}')

        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('dic_1', result)

        node._index = TemplateWordNode("1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('dic_2', result)

        node._index = TemplateWordNode("2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('dic_3', result)

        node._index = TemplateWordNode("3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_dict_element(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"dic_1": "val_1", "dic_2": "val_2", "dic_3": "val_3"}}')

        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('val_1', result)

        node._index = TemplateWordNode("1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('val_2', result)

        node._index = TemplateWordNode("2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('val_3', result)

        node._index = TemplateWordNode("3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_dict_element_from_end(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        root.append(node)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"dic_1": "val_1", "dic_2": "val_2", "dic_3": "val_3"}}')

        node._index = TemplateWordNode("-1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('val_3', result)

        node._index = TemplateWordNode("-2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('val_2', result)

        node._index = TemplateWordNode("-3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('val_1', result)

        node._index = TemplateWordNode("-4")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_invalid_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._index = TemplateWordNode("x")
        node._key = TemplateWordNode("key_data")
        root.append(node)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_data": ["list_1", "list_2", "list_3"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    #  SET

    def test_json_set_typename(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("value_name"))

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": "value_name"}', conversation.property("name_json"))

    def test_json_set_typedata(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("value_data"))

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_data": "value_data"}', conversation.data_property("data_json"))

    def test_json_set_typevar(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("value_var"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": "value_var"}', question.property("var_json"))

    def test_json_set_with_quote(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode('"value_var"'))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": "value_var"}', question.property("var_json"))

    def test_json_set_short_value(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("v"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": "v"}', question.property("var_json"))

    def test_json_set_empty(self):
        root = TemplateNode()

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        node.append(TemplateWordNode(""))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertIsNone(conversation.data_property("data_json"))

    def test_json_set_empty_data(self):
        root = TemplateNode()

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        node.append(TemplateWordNode('""'))
        root.append(node)
        self.assertEqual(len(root.children), 1)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_data": ""}', conversation.data_property("data_json"))

    def test_json_set_sub_dic(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json.key_data")
        node._type = "data"
        node._key = TemplateWordNode("child")
        node.append(TemplateWordNode("value_data"))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_data": {"child": "value_data"}}', conversation.data_property("data_json"))

    def test_json_set_value_to_dict(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json.key_data.child")
        node._type = "data"
        node._key = TemplateWordNode("key")
        node.append(TemplateWordNode("value_data"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"child": "data"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_data": {"child": {"key": "value_data"}}}', conversation.data_property("data_json"))

    def test_json_set_sub_child(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json.key_data")
        node._type = "data"
        node._key = TemplateWordNode("child2")
        node.append(TemplateWordNode("value_data"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_data_property("data_json", '{"key_data": {"child1": "data"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_data": {"child1": "data", "child2": "value_data"}}', conversation.data_property("data_json"))

    def test_json_set_add_dic(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json.key_data.child")
        node._type = "data"
        node._key = TemplateWordNode("add")
        root.append(node)
        node.append(TemplateWordNode("value_data"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"child": {"data": ""}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_data": {"child": {"add": "value_data"}}}', conversation.data_property("data_json"))

    def test_json_set_with_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("data"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["data", "list_2", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["data", "data", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["data", "data", "data"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["data", "data", "data"]}', conversation.property("name_json"))

    def test_json_set_with_index_from_end(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("data"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("-1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "data"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("-2")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "data", "data"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("-3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["data", "data", "data"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("-4")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["data", "data", "data"]}', conversation.property("name_json"))

    def test_json_set_list(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode('"list_1", "list_2", "list_3"'))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

    def test_json_set_list_emptydata(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode('"", "list_2", ""'))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertEqual('{"key_name": ["", "list_2", ""]}', conversation.property("name_json"))

    def test_json_set_list_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node._index = TemplateWordNode("1")
        node.append(TemplateWordNode('"data_1", "data_2", "data3"'))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual('{"key_name": ["list_1", ["data_1", "data_2", "data3"], "list_3"]}', conversation.property("name_json"))

    def test_json_set_jsonform(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode('{"key_1": "val_1", "key_2": "val_2"}'))

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": {"key_1": "val_1", "key_2": "val_2"}}', conversation.property("name_json"))

    def test_json_set_jsonform_with_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node._index = TemplateWordNode("1")
        node.append(TemplateWordNode('{"key_1": "val_1", "key_2": "val_2"}'))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": ["list_1", {"key_1": "val_1", "key_2": "val_2"}, "list_3"]}', conversation.property("name_json"))

    def test_json_set_convert_null(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("null"))
        node._is_convert = True
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": null}', conversation.property("name_json"))

    def test_json_set_convert_true(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("true"))
        node._is_convert = True
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": true}', conversation.property("name_json"))

    def test_json_set_convert_false(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("false"))
        node._is_convert = True
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": false}', conversation.property("name_json"))

    def test_json_set_convert_integer(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("100"))
        node._is_convert = True
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": 100}', conversation.property("name_json"))

    def test_json_set_convert_float(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("0.11"))
        node._is_convert = True
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": 0.11}', conversation.property("name_json"))

    def test_json_set_convert_other(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("text"))
        node._is_convert = True
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_name": "text"}', conversation.property("name_json"))

    def test_json_set_invalid_listform(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        node.append(TemplateWordNode('val_1, val_2'))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_json_set_invalid_listform_short(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        node.append(TemplateWordNode("v, a"))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_json_set_invalid_jsonform(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_data")
        node.append(TemplateWordNode('{"key_1": "val_1, "key_2": "val_2"}'))
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_json_set_invalid_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_name")
        node.append(TemplateWordNode("value_var"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("x")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("-4")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

    #  INSERT

    def test_json_insert_first(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("0")
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("value_var"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["value_var", "list_1", "list_2"]}', question.property("var_json"))

    def test_json_insert_middle(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("1")
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("var_val"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["list_1", "var_val", "list_2"]}', question.property("var_json"))

    def test_json_insert_middle_from_end(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("-2")
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("var_val"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["list_1", "var_val", "list_2"]}', question.property("var_json"))

    def test_json_insert_last(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("-1")
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        node.append(TemplateWordNode("value_var"))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["list_1", "list_2", "value_var"]}', question.property("var_json"))

    def test_json_insert_new_first(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("0")
        node._key = TemplateWordNode("key_var")
        node.append(TemplateWordNode("value_var"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["value_var"]}', question.property("var_json"))

    def test_json_insert_new_last(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("-1")
        node.append(TemplateWordNode("value_var"))
        node._key = TemplateWordNode("key_var")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["value_var"]}', question.property("var_json"))

    def test_json_insert_new_jsonform(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("-1")
        node.append(TemplateWordNode('{"key_1": "data_1"}'))
        node._key = TemplateWordNode("key_var")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": [{"key_1": "data_1"}]}', question.property("var_json"))

    def test_json_insert_list(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("0")
        node._key = TemplateWordNode("key_var")
        node.append(TemplateWordNode('"data_1", "data_2"'))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": ["data_1", "data_2", "list_1", "list_2"]}', question.property("var_json"))

    def test_json_insert_jsonform(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("0")
        node._key = TemplateWordNode("key_var")
        node.append(TemplateWordNode('{"key_1": "data_1", "key_2": "data_2"}'))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": [{"key_1": "data_1", "key_2": "data_2"}, "list_1", "list_2"]}', question.property("var_json"))

    def test_json_insert_not_list(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("0")
        node._key = TemplateWordNode("key_var")
        node.append(TemplateWordNode('"data_1", "data_2"'))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": "value"}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertIsNotNone(conversation.current_question())
        self.assertIsNotNone(conversation)
        self.assertEqual('{"key_var": "value"}', question.property("var_json"))

    def test_json_insert_not_index_top(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("1")
        node._key = TemplateWordNode("key_name2")
        node.append(TemplateWordNode('"data_1", "data_2"'))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": "value"}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual('{"key_name": "value"}', conversation.property("name_json"))

    def test_json_insert_invalid_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._key = TemplateWordNode("key_var")
        node.append(TemplateWordNode("var_val"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        question.set_property("var_json", '{"key_var": ["list_1", "list_2"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        node._index = TemplateWordNode("x")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_var": ["list_1", "list_2"]}', question.property("var_json"))

        node._index = TemplateWordNode("3")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_var": ["list_1", "list_2"]}', question.property("var_json"))

        node._index = TemplateWordNode("-4")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_var": ["list_1", "list_2"]}', question.property("var_json"))

    #  DELETE

    def test_json_delete_typename(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_name")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_property("name_json", '{"key_name": "value_name"}')

        self.assertEqual('{"key_name": "value_name"}', conversation.property("name_json"))

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual("{}", conversation.property("name_json"))

    def test_json_delete_typedata(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_data")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_data_property("data_json", '{"key_data": "value_data"}')

        self.assertEqual('{"key_data": "value_data"}', conversation.data_property("data_json"))

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual("{}", conversation.data_property("data_json"))

    def test_json_delete_typevar(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_var")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        question.set_property("var_json", '{"key_var": "value_var"}')

        self.assertEqual('{"key_var": "value_var"}', question.property("var_json"))

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual("{}", question.property("var_json"))

    def test_json_delete_child_dic(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json.key_data")
        node._type = "data"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("elemrnt")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_data_property("data_json", '{"key_data": {"elemrnt": "value_data"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual('{"key_data": {}}', conversation.data_property("data_json"))

    def test_json_delete_list_element(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_name")
        node._index = TemplateWordNode("1")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual('{"key_name": ["list_1", "list_3"]}', conversation.property("name_json"))

    def test_json_delete_dic_element(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_name")
        node._index = TemplateWordNode("1")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property("name_json", '{"key_name": {"dic_1": "val_1", "dic_2": "val_2", "dic_3": "val_3"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

        self.assertEqual('{"key_name": {"dic_1": "val_1", "dic_3": "val_3"}}', conversation.property("name_json"))

    def test_json_delete_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_name")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("0")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_2", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("-1")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_2"]}', conversation.property("name_json"))

    def test_json_delete_no_target(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_name")
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_json_delete_invalid_key(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        node._key = TemplateWordNode("key_x")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

        node._key = TemplateWordNode("key_name.key_x")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

    def test_json_delete_invalid_child_key(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json.child1")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("child2")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_property("name_json", '{"key_name": {"child1": "data"}}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": {"child1": "data"}}', conversation.property("name_json"))

    def test_json_delete_invalid_index(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._function = TemplateWordNode("delete")
        node._key = TemplateWordNode("key_name")
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        conversation.set_property("name_json", '{"key_name": ["list_1", "list_2", "list_3"]}')

        node._index = TemplateWordNode("x")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("5")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

        node._index = TemplateWordNode("-5")
        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)
        self.assertEqual('{"key_name": ["list_1", "list_2", "list_3"]}', conversation.property("name_json"))

    #  to XML

    def test_to_xml_json_typename(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        node._key = TemplateWordNode("key_1")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><json name="name_json"><key>key_1</key></json></template>', xml_str)

    def test_to_xml_json_typedata(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        node._key = TemplateWordNode("key_1")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><json data="data_json"><key>key_1</key></json></template>', xml_str)

    def test_to_xml_json_typevar(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._key = TemplateWordNode("key_1")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><json var="var_json"><key>key_1</key></json></template>', xml_str)

    def test_to_xml_json_all_parameter(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        node._index = TemplateWordNode("0")
        node._item = TemplateWordNode("key")
        node._key = TemplateWordNode("key_1")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><json var="var_json"><function>insert</function><index>0</index><item>key</item><key>key_1</key></json></template>', xml_str)

    def test_to_xml_json_no_key(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json.key_1")
        node._type = "var"
        node._function = TemplateWordNode("delete")
        node._index = TemplateWordNode("0")
        root.append(node)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><json var="var_json.key_1"><function>delete</function><index>0</index></json></template>', xml_str)

    #  others

    def test_json_get_key_in_name(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json.key_1")
        node._type = "name"
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())
        conversation.set_property("name_json", '{"key_1": "value_name"}')

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("value_name", result)

    def test_json_get_no_typename(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("name_json")
        node._type = "name"
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_no_typedata(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("data_json")
        node._type = "data"
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_get_no_typevar(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self._client_context.brain.properties.add_property("default-get", "unknown")

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("unknown", result)

    def test_json_invlid_function(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("update")
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_json_invlid_insert(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("var_json")
        node._type = "var"
        node._function = TemplateWordNode("insert")
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_json_invlid_type(self):
        root = TemplateNode()
        node = TemplateJsonNode()
        node._name = TemplateWordNode("other_json")
        node._type = "other"
        root.append(node)

        result = root.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual("", result)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateJsonNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
