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
import os

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.learn import LearnCategory
from programy.parser.template.nodes.learnf import TemplateLearnfNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateLearnfNode(TemplateLearnfNode):
    def __init__(self):
        TemplateLearnfNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateLearnfNodeTests(ParserTestsBaseClass):

    def get_os_specific_path(self):
        if os.name == 'posix':
            return '/tmp/learnf'
        elif os.name == 'nt':
            return
        else:
            raise Exception("Unknown OS [%s]" % os.name)

    def test_node(self):

        root = TemplateNode()
        self.assertIsNotNone(root)

        learn = TemplateLearnfNode()
        self.assertIsNotNone(learn)
        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)
        root.append(learn)
        self.assertEqual(1, len(root.children))

        self._client_context.brain.configuration.defaults._learn_path = self.get_os_specific_path()
        resolved = root.resolve(self._client_context)
        self.assertIsNotNone(resolved)
        self.assertEqual("", resolved)

    def test_to_xml(self):
        root = TemplateNode()
        learn = TemplateLearnfNode()
        learn_cat = LearnCategory(ET.fromstring("<pattern>HELLO LEARN</pattern>"),
                                  ET.fromstring("<topic>*</topic>"),
                                  ET.fromstring("<that>*</that>"),
                                  TemplateWordNode("LEARN"))
        learn.append(learn_cat)
        root.append(learn)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        texts = "<template><learnf><category><pattern>HELLO LEARN</pattern><topic>*</topic><that>*</that><template>LEARN</template></category></learnf></template>"
        self.assertEqual(texts, xml_str)

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateLearnfNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
