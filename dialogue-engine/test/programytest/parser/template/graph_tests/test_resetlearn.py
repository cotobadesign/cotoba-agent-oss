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

from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode
from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.base import TemplateNode
from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphResetLearnTests(TemplateGraphTestClient):

    def test_learnf_type1(self):
        template = ET.fromstring("""
            <template>
                <resetlearn />
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateResetLearnNode)
        self.assertEqual(0, len(ast.children[0].children))

    def test_learnf_type2(self):
        template = ET.fromstring("""
            <template>
                <resetlearn></resetlearn>
            </template>
        """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateResetLearnNode)
        self.assertEqual(0, len(ast.children[0].children))

    def test_request_with_children(self):
        template = ET.fromstring("""
            <template>
                <resetlearn>Error</resetlearn>
            </template>
            """)
        with self.assertRaises(ParserException):
            self._graph.parse_template_expression(template)

    def test_removal(self):
        client_context1 = self.create_client_context("testid")

        template = ET.fromstring("""
            <template>
                <learn>
                    <category>
                        <pattern>HELLO THERE</pattern>
                        <template>HIYA ONE</template>
                    </category>
                </learn>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context1)

        response = client_context1.bot.ask_question(client_context1, "HELLO THERE")
        self.assertEqual("HIYA ONE.", response)

        client_context2 = self.create_client_context("testid")

        template = ET.fromstring("""
            <template>
                <learn>
                    <category>
                        <pattern>HELLO THERE</pattern>
                        <template>HIYA TWO</template>
                    </category>
                </learn>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context2)

        response = client_context2.bot.ask_question(client_context2, "HELLO THERE")
        self.assertEqual("HIYA TWO.", response)

        template = ET.fromstring("""
            <template>
                <resetlearn />
            </template>
            """)

        ast = self._graph.parse_template_expression(template)

        learn_node = ast.children[0]

        learn_node.resolve(client_context2)
