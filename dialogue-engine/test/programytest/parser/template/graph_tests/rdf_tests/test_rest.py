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

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphFirstTests(TemplateGraphTestClient):

    def test_rest_single_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
            <template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>HASFUR</pred>
                            <obj>true</obj>
                        </q>
                    </select>
                </rest>
            </template>
            """)
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('unknown', result)

    def test_rest_single_var_multipe_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
            <template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>LEGS</pred>
                            <obj>2</obj>
                        </q>
                    </select>
                </rest>
            </template>
            """)
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('[[["?x", "BIRD"]]]', result)

    def test_rest_multi_var_single_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
            <template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>HASFUR</pred>
                            <obj>?y</obj>
                        </q>
                    </select>
                </rest>
            </template>
            """)
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('unknown', result)

    def test_rest_multiple_var_multipe_result(self):

        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
            <template>
               <rest>
                    <select>
                        <vars>?x</vars>
                        <q>
                            <subj>?x</subj>
                            <pred>LEGS</pred>
                            <obj>?y</obj>
                        </q>
                    </select>
                </rest>
            </template>
            """)
        self.assertIsNotNone(template)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        self.assertEqual('[[["?x", "ZEBRA"], ["?y", "4"]], [["?x", "BIRD"], ["?y", "2"]]]', result)
