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

from programy.parser.template.nodes.resetlearnf import TemplateResetLearnfNode

from programytest.parser.base import ParserTestsBaseClass
from programy.parser.template.nodes.base import TemplateNode


class MockTemplateResetLearnfNode(TemplateResetLearnfNode):
    def __init__(self):
        TemplateResetLearnfNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateResetLearnfNodeTests(ParserTestsBaseClass):

    def test_node(self):
        root = TemplateResetLearnfNode()
        self.assertIsNotNone(root)
        self.assertEqual("", root.resolve(self._client_context))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateResetLearnfNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)

    def test_to_string(self):
        node = TemplateResetLearnfNode()
        self.assertEqual("[RESETLEARNF]", node.to_string())

    def test_to_xml(self):
        node = TemplateResetLearnfNode()
        self.assertEqual("<resetlearnf />", node.to_xml(self._client_context))
