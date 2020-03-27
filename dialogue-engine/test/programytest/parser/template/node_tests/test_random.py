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
from programy.parser.template.nodes.rand import TemplateRandomNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateRandomNode(TemplateRandomNode):
    def __init__(self):
        TemplateRandomNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateRandomNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        random = TemplateRandomNode()
        random.append(TemplateWordNode("Test1"))
        random.append(TemplateWordNode("Test2"))
        random.append(TemplateWordNode("Test3"))
        self.assertEqual(len(random.children), 3)

        root.append(random)

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertOneOf(resolved, ["Test1", "Test2", "Test3"])

    def test_to_xml(self):
        root = TemplateNode()
        random = TemplateRandomNode()
        root.append(random)
        random.append(TemplateWordNode("Test1"))
        random.append(TemplateWordNode("Test2"))

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><random><li>Test1</li><li>Test2</li></random></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateRandomNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
