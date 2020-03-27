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
import json

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.template.nodes.select import TemplateSelectNode
from programy.parser.template.nodes.select import Query, NotQuery
from programy.parser.exceptions import ParserException

from programytest.parser.template.graph_tests.graph_test_client import TemplateGraphTestClient


class TemplateGraphSelectTests(TemplateGraphTestClient):

    ################################################################################################################
    # Test Node Construction
    #

    def test_select_single_vars_single_query(self):
        template = ET.fromstring("""
            <template>
                <select>
                    <vars>?x</vars>
                    <q><subj>?x</subj><pred>Y</pred><obj>Z</obj></q>
                </select>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]

        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)

        self.assertEqual(1, len(select_node.queries))
        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("Y", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("Z", query1.obj.resolve(self._client_context))

    def test_select_multi_vars_single_query(self):
        template = ET.fromstring("""
            <template>
                <select>
                    <vars>?x ?y</vars>
                    <q><subj>?x</subj><pred>?y</pred><obj>Z</obj></q>
                </select>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]

        self.assertIsNotNone(select_node.vars)
        self.assertEqual(2, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)
        self.assertTrue("?y" in select_node.vars)

        self.assertEqual(1, len(select_node.queries))
        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("?y", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("Z", query1.obj.resolve(self._client_context))

    def test_select_single_vars_multie_query(self):
        template = ET.fromstring("""
            <template>
                <select>
                    <vars>?x</vars>
                    <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
                    <q><subj>?x</subj><pred>Y</pred><obj>Z</obj></q>
                </select>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, Query)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("Y", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

    def test_select_multi_vars_multi_query(self):
        template = ET.fromstring("""
            <template>
                <select>
                    <vars>?x ?y</vars>
                    <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
                    <q><subj>?x</subj><pred>?y</pred><obj>Z</obj></q>
                </select>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(2, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)
        self.assertTrue("?y" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, Query)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("?y", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

    def test_select_single_vars_mixed_query(self):
        template = ET.fromstring("""
            <template>
                <select>
                    <vars>?x</vars>
                    <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
                    <notq><subj>?x</subj><pred></pred><obj>Z</obj></notq>
                </select>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, NotQuery)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsNone(query2.pred)
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

    def test_select_multi_vars_mixed_query(self):
        template = ET.fromstring("""
            <template>
                <select>
                    <vars>?A ?X</vars>
                    <q><subj>?A</subj><pred>B</pred><obj>C</obj></q>
                    <notq><subj>?X</subj><pred>Y</pred><obj>Z</obj></notq>
                </select>
            </template>
            """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node)
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(2, len(select_node.vars))
        self.assertTrue("?A" in select_node.vars)
        self.assertTrue("?X" in select_node.vars)

        self.assertEqual(2, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("?A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

        query2 = select_node.queries[1]
        self.assertIsInstance(query2, NotQuery)
        self.assertIsInstance(query2.subj, TemplateNode)
        self.assertEqual(1, len(query2.subj.children))
        self.assertIsInstance(query2.subj.children[0], TemplateWordNode)
        self.assertEqual("?X", query2.subj.resolve(self._client_context))
        self.assertIsInstance(query2.pred, TemplateNode)
        self.assertEqual("Y", query2.pred.resolve(self._client_context))
        self.assertIsInstance(query2.obj, TemplateNode)
        self.assertEqual("Z", query2.obj.resolve(self._client_context))

    def test_select_no_vars_single_query(self):
        template = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)
        self.assertIsNotNone(ast)

        self.assertIsInstance(ast, TemplateNode)
        self.assertIsNotNone(ast.children)
        self.assertIsNotNone(ast.children[0])
        self.assertIsInstance(ast.children[0], TemplateSelectNode)
        self.assertEqual(0, len(ast.children[0].children))

        select_node = ast.children[0]
        self.assertIsNotNone(select_node)
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(0, len(select_node.vars))

        self.assertEqual(1, len(select_node.queries))

        query1 = select_node.queries[0]
        self.assertIsInstance(query1, Query)
        self.assertIsInstance(query1.subj, TemplateNode)
        self.assertEqual(1, len(query1.subj.children))
        self.assertIsInstance(query1.subj.children[0], TemplateWordNode)
        self.assertEqual("A", query1.subj.resolve(self._client_context))
        self.assertIsInstance(query1.pred, TemplateNode)
        self.assertEqual("B", query1.pred.resolve(self._client_context))
        self.assertIsInstance(query1.obj, TemplateNode)
        self.assertEqual("C", query1.obj.resolve(self._client_context))

    def test_select_multi_vars_tags(self):
        template1 = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <vars>?y</vars>
                        <q><subj>A</subj><pred>B</pred><obj>C</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template1)

        select_node = ast.children[0]
        self.assertIsNotNone(select_node.vars)
        self.assertEqual(1, len(select_node.vars))
        self.assertTrue("?x" in select_node.vars)
        self.assertFalse("?y" in select_node.vars)

    def test_select_no_element(self):
        template1 = ET.fromstring("""
                <template>
                    <select>
                        <q><pred>LEGS</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast1 = self._graph.parse_template_expression(template1)
        select_node = ast1.children[0]
        query1 = select_node.queries[0]
        self.assertIsNone(query1.subj)
        self.assertEqual("LEGS", query1.pred.resolve(self._client_context))
        self.assertEqual("2", query1.obj.resolve(self._client_context))

        template2 = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>?x</subj><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast2 = self._graph.parse_template_expression(template2)
        select_node2 = ast2.children[0]
        query2 = select_node2.queries[0]
        self.assertEqual("?x", query2.subj.resolve(self._client_context))
        self.assertIsNone(query2.pred)
        self.assertEqual("2", query2.obj.resolve(self._client_context))

        template3 = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>?x</subj><pred>LEGS</pred></q>
                    </select>
                </template>
                """)

        ast3 = self._graph.parse_template_expression(template3)
        select_node3 = ast3.children[0]
        query3 = select_node3.queries[0]
        self.assertEqual("?x", query3.subj.resolve(self._client_context))
        self.assertEqual("LEGS", query3.pred.resolve(self._client_context))
        self.assertIsNone(query3.obj)

    def test_select_no_var_define(self):
        template1 = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast1 = self._graph.parse_template_expression(template1)
        select_node = ast1.children[0]
        query1 = select_node.queries[0]
        self.assertEqual("?x", query1.subj.resolve(self._client_context))
        self.assertEqual("LEGS", query1.pred.resolve(self._client_context))
        self.assertEqual("2", query1.obj.resolve(self._client_context))

        template2 = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>MONKEY</subj><pred>?y</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast2 = self._graph.parse_template_expression(template2)
        select_node = ast2.children[0]
        query2 = select_node.queries[0]
        self.assertEqual("MONKEY", query2.subj.resolve(self._client_context))
        self.assertEqual("?y", query2.pred.resolve(self._client_context))
        self.assertEqual("2", query2.obj.resolve(self._client_context))

        template3 = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>MONKEY</subj><pred>LEGS</pred><obj>?z</obj></q>
                    </select>
                </template>
                """)

        ast3 = self._graph.parse_template_expression(template3)
        select_node = ast3.children[0]
        query3 = select_node.queries[0]
        self.assertEqual("MONKEY", query3.subj.resolve(self._client_context))
        self.assertEqual("LEGS", query3.pred.resolve(self._client_context))
        self.assertEqual("?z", query3.obj.resolve(self._client_context))

    def test_select_invalid_query_subtag(self):
        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj><plus>a</plus></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)
        select_node = ast.children[0]
        query = select_node.queries[0]
        self.assertEqual("?x", query.subj.resolve(self._client_context))
        self.assertEqual("LEGS", query.pred.resolve(self._client_context))
        self.assertEqual("2", query.obj.resolve(self._client_context))

    ################################################################################################################
    # Test Matching Evaluation
    #

    def test_query_no_vars(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <q><subj>MONKEY</subj><pred>LEGS</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)

        query_results = json.loads(result)
        query1_results = query_results[0]

        self.assertTrue(["subj", "MONKEY"] in query1_results)
        self.assertTrue(["pred", "LEGS"] in query1_results)
        self.assertTrue(["obj", "2"] in query1_results)

    def test_not_query_no_vars(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <notq><subj>MONKEY</subj><pred>LEGS</pred><obj>2</obj></notq>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)

        self.assertFalse([['subj', 'MONKEY'], ['pred', 'LEGS'], ['obj', '2']] in query_results)
        self.assertTrue([['subj', 'MONKEY'], ['pred', 'HASFUR'], ['obj', 'TRUE']] in query_results)
        self.assertTrue([['subj', 'ZEBRA'], ['pred', 'LEGS'], ['obj', '4']] in query_results)
        self.assertTrue([['subj', 'BIRD'], ['pred', 'LEGS'], ['obj', '2']] in query_results)
        self.assertTrue([['subj', 'ELEPHANT'], ['pred', 'TRUNK'], ['obj', 'TRUE']] in query_results)

    def test_query_var(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(2, len(query_results))
        self.assertTrue([["?x", "MONKEY"]] in query_results)
        self.assertTrue([["?x", "BIRD"]] in query_results)

    def test_not_query_var(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <notq><subj>?x</subj><pred>LEGS</pred><obj>2</obj></notq>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(3, len(query_results))
        self.assertTrue([["?x", "ZEBRA"]] in query_results)
        self.assertTrue([["?x", "ELEPHANT"]] in query_results)

    def test_query_multi_vars(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x ?y</vars>
                        <q><subj>?x</subj><pred>?y</pred><obj>2</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(2, len(query_results))
        self.assertTrue([["?x", "MONKEY"], ["?y", "LEGS"]] in query_results)
        self.assertTrue([["?x", "BIRD"], ["?y", "LEGS"]] in query_results)

    def test_query_vars_object(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?z</vars>
                        <q><subj>MONKEY</subj><pred>LEGS</pred><obj>?z</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(1, len(query_results))
        self.assertTrue([["?z", "2"]] in query_results)

    def test_query_var_multi_queries(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                        <q><subj>?x</subj><pred>HASFUR</pred><obj>true</obj></q>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(1, len(query_results))

        self.assertTrue([["?x", "MONKEY"]] in query_results)

    def test_query_var_mixed_queries(self):
        self._client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        self._client_context.brain.rdf.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        self._client_context.brain.rdf.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

        template = ET.fromstring("""
                <template>
                    <select>
                        <vars>?x</vars>
                        <q><subj>?x</subj><pred>LEGS</pred><obj>2</obj></q>
                        <notq><subj>?x</subj><pred>HASFUR</pred><obj>true</obj></notq>
                    </select>
                </template>
                """)

        ast = self._graph.parse_template_expression(template)

        result = ast.resolve(self._client_context)
        self.assertIsNotNone(result)
        query_results = json.loads(result)
        self.assertIsNotNone(query_results)
        self.assertEqual(2, len(query_results))

        self.assertTrue([["?x", "BIRD"]] in query_results)
        self.assertTrue([["?x", "MONKEY"]] in query_results)
