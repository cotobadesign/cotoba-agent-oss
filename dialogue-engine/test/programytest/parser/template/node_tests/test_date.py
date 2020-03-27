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

from programy.clients.restful.client import UserInfo
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.date import TemplateDateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException

from programytest.parser.base import ParserTestsBaseClass
from programytest.custom import CustomAssertions


class MockTemplateDateNode(TemplateDateNode):

    def __init__(self, date_format=None):
        TemplateDateNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is a failure")


class TemplateDateNodeTests(ParserTestsBaseClass, CustomAssertions):

    DEFAULT_DATETIME_REGEX = r"^.{3}\s*.{3}\s*\d{1,}\s\d{2}:\d{2}:\d{2}\s\d{4}"

    def test_node_defaultformat(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_defaultformat_with_userinfo(self):

        userInfo = UserInfo(None, None)
        userInfo.set('__USER_LOCALE__', "ja-jp")
        userInfo.set('__USER_TIME__', "2019-01-01T00:00:00+0900")
        self._client_context.userInfo = userInfo

        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)

        dateTime = root.resolve(self._client_context)
        self.assertEqual(dateTime, "Tue Jan 1 00:00:00 2019")

    def test_node_defaultformat_with_userinfo_locale_US(self):

        userInfo = UserInfo(None, None)
        userInfo.set('__USER_LOCALE__', "en-US")
        userInfo.set('__USER_TIME__', "2019-01-01T00:00:00+0900")
        self._client_context.userInfo = userInfo

        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)

        dateTime = root.resolve(self._client_context)
        self.assertEqual(dateTime, "Mon Dec 31 10:00:00 2018")

    def test_node_defaultformat_with_userinfo_invalid_locale(self):

        userInfo = UserInfo(None, None)
        userInfo.set('__USER_LOCALE__', "x-x")
        userInfo.set('__USER_TIME__', "2019-01-01T00:00:00+0900")
        self._client_context.userInfo = userInfo

        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)

        dateTime = root.resolve(self._client_context)
        self.assertEqual(dateTime, "Tue Jan 1 00:00:00 2019")

        userInfo.set('__USER_LOCALE__', "JP")
        dateTime = root.resolve(self._client_context)
        self.assertEqual(dateTime, "Tue Jan 1 00:00:00 2019")

    def test_node_defaultformat_with_userinfo_invalid_timeform(self):

        userInfo = UserInfo(None, None)
        userInfo.set('__USER_LOCALE__', "ja-jp")
        userInfo.set('__USER_TIME__', "2019-01-01T00:00:00+09:00")
        self._client_context.userInfo = userInfo

        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)

        dateTime = root.resolve(self._client_context)
        self.assertRegex(dateTime, TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_defaultformat_with_userinfo_None(self):

        userInfo = UserInfo(None, None)
        self._client_context.userInfo = userInfo

        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)

        dateTime = root.resolve(self._client_context)
        self.assertRegex(dateTime, TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_constructor(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode(date_format="%c")
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_parameter(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)
        node.format = "%c"
        root.append(node)

        self.assertEqual(len(root.children), 1)
        self.assertEqual("%c", node.format)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_set_attrib(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)
        node.set_attrib("format", "%c")

        root.append(node)
        self.assertEqual(len(root.children), 1)
        self.assertRegex(root.resolve(self._client_context), TemplateDateNodeTests.DEFAULT_DATETIME_REGEX)

    def test_node_customformat_set_attrib_invalid(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateDateNode()
        self.assertIsNotNone(node)
        with self.assertRaises(ParserException):
            node.set_attrib("unknown", "%c")

    def test_to_xml_defaults(self):
        root = TemplateNode()
        node = TemplateDateNode()
        root.append(node)
        node.append(TemplateWordNode("Mon Sep 30 07:06:05 2013"))
        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><date format="%c">Mon Sep 30 07:06:05 2013</date></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = MockTemplateDateNode()
        self.assertIsNotNone(node)

        root.append(node)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
