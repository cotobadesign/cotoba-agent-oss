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
from programy.parser.template.nodes.log import TemplateLogNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateLogNode(TemplateLogNode):
    def __init__(self):
        TemplateLogNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateLogNodeTests(ParserTestsBaseClass):

    def test_init(self):
        log = TemplateLogNode()

        log.level = "debug"
        self.assertEqual("debug", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "warning"
        self.assertEqual("warning", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "error"
        self.assertEqual("error", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "info"
        self.assertEqual("info", log.level)
        self.assertEqual("", log.resolve(self._client_context))

        log.level = "exception"
        self.assertEqual("exception", log.level)
        self.assertEqual("", log.resolve(self._client_context))

    def test_set_attrib(self):
        log = TemplateLogNode()

        log.set_attrib('level', 'debug')
        self.assertEqual("debug", log.level)

        log.set_attrib('level', 'warning')
        self.assertEqual("warning", log.level)

        log.set_attrib('level', 'error')
        self.assertEqual("error", log.level)

        log.set_attrib('level', 'info')
        self.assertEqual("info", log.level)

        with self.assertRaises(ParserException):
            log.set_attrib('unknown', 'info')

        with self.assertRaises(ParserException):
            log.set_attrib('level', 'unknown')

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        log = TemplateLogNode()
        self.assertIsNotNone(log)
        log.append(TemplateWordNode("Log Test"))

        root.append(log)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_node_saerver_mode(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        error_log = TemplateLogNode()
        self.assertIsNotNone(error_log)
        error_log.level = "error"
        error_log.append(TemplateWordNode("Error Log"))

        warnig_log = TemplateLogNode()
        self.assertIsNotNone(warnig_log)
        warnig_log.level = "warnig"
        warnig_log.append(TemplateWordNode("Warnig Log"))

        info_log = TemplateLogNode()
        self.assertIsNotNone(info_log)
        info_log.level = "info"
        info_log.append(TemplateWordNode("Info log"))

        debug_log = TemplateLogNode()
        self.assertIsNotNone(debug_log)
        debug_log.level = "debug"
        debug_log.append(TemplateWordNode("Debug Log"))

        root.append(error_log)
        root.append(warnig_log)
        root.append(info_log)
        root.append(debug_log)
        self.assertEqual(4, len(root.children))

        self._client_context._server_mode = True

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertEqual(4, len(conversation.logs))

    def test_to_xml_default(self):

        root = TemplateNode()
        log = TemplateLogNode()

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="info">Log Test</log></template>', xml_str)

    def test_to_xml_debug(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "debug"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="debug">Log Test</log></template>', xml_str)

    def test_to_xml_error(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "error"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="error">Log Test</log></template>', xml_str)

    def test_to_xml_info(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "info"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="info">Log Test</log></template>', xml_str)

    def test_to_xml_warning(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = "warning"

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log level="warning">Log Test</log></template>', xml_str)

    def test_to_xml_unknown(self):

        root = TemplateNode()
        log = TemplateLogNode()
        log.level = None

        log.append(TemplateWordNode("Log Test"))
        root.append(log)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><log>Log Test</log></template>', xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLogNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
