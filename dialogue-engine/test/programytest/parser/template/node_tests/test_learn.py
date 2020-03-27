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
import unittest

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import TemplateLearnNode, LearnCategory
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateLearnNode(TemplateLearnNode):
    def __init__(self):
        TemplateLearnNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TestLearnCategory(unittest.TestCase):

    def test_init(self):
        learncat = LearnCategory("pattern", "topic", "that", "template")
        self.assertIsNotNone(learncat)
        self.assertIsNotNone(learncat._pattern)
        self.assertIsNotNone(learncat._topic)
        self.assertIsNotNone(learncat._that)
        self.assertIsNotNone(learncat._template)
        self.assertIsNotNone(learncat.children)
        self.assertEqual(0, len(learncat.children))

        self.assertEqual("[CATEGORY]", learncat.to_string())

        learncat.pattern = "pattern2"
        self.assertEqual("pattern2", learncat.pattern)
        learncat.topic = "topic2"
        self.assertEqual("topic2", learncat.topic)
        learncat.that = "that2"
        self.assertEqual("that2", learncat.that)
        learncat.template = "template2"
        self.assertEqual("template2", learncat.template)

        learncat.append("category1")
        learncat.append("category2")
        self.assertEqual(2, len(learncat.children))


class TemplateLearnNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnNode()
        self.assertIsNotNone(learn)

        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)

        root.append(learn)
        self.assertEqual(1, len(root.children))

        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnNode()
        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)
        root.append(learn)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual("<template><learn><category><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></category></learn></template>", xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLearnNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
