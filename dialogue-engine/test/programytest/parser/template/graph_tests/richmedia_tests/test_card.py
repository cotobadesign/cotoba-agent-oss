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
from programy.parser.template.nodes.richmedia.card import TemplateCardNode

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphCardTests(TemplateGraphTestClient):

    def test_card_node_from_xml(self):
        template = ET.fromstring("""
            <template>
                <card>
                    <image>http://www.servusai.com/aiml.png</image>
                    <title>Servusai.com</title>
                    <subtitle>The home of ProgramY</subtitle>
                    <button>
                        <text>Servusai.com</text>
                        <url>http://www.servusai.com</url>
                    </button>
                    <button>
                        <text>ProgramY</text>
                        <url>http://github.io/keiffster</url>
                    </button>
                </card>
            </template>
            """)
        root = self._graph.parse_template_expression(template)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, TemplateNode)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 1)

        node = root.children[0]
        self.assertIsNotNone(node)
        self.assertIsInstance(node, TemplateCardNode)

        self.assertIsNotNone(node._image)
        self.assertIsNotNone(node._title)
        self.assertIsNotNone(node._subtitle)
        self.assertIsNotNone(node._buttons)
        self.assertEqual(2, len(node._buttons))
