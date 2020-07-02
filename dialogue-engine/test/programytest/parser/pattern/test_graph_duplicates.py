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

from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import DuplicateGrammarException
from programy.parser.pattern.graph import PatternGraph
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.pattern.nodes.bot import PatternBotNode
from programy.parser.pattern.nodes.word import PatternWordNode


class PatternGraphDuplicateTests(ParserTestsBaseClass):

    def set_collection_properties(self):
        self._client_context.brain.properties.add_property("A", "value")

    def set_collection_sets(self):
        set_dict = {"RED": [["RED"]]}
        values = {"RED": "red"}
        self._client_context.brain.sets.add_set("A", set_dict, "test_sets", False, values)

    def test_duplicate_pattern(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_same_topics(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>X Y</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>X Y</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_same_thats(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>X Y</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>X Y</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_different_topics(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>A B</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>X Y</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_pattern_different_thats(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>A B</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A # *</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>X Y</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_priority(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_priority_and_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_priority_and_word_otherwayround(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)

        pattern_element = ET.fromstring("<pattern>$A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_set(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.set_collection_sets()

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_set_and_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.set_collection_sets()

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_set_and_word_otherwayround(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.set_collection_sets()

        pattern_element = ET.fromstring("<pattern><set>A</set></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_bot(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.set_collection_properties()

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        with self.assertRaises(DuplicateGrammarException):
            graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_bot_and_word(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.set_collection_properties()

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def test_duplicate_bot_and_word_otherwayround(self):
        graph = PatternGraph(self._client_context.brain.aiml_parser)
        self.set_collection_properties()

        pattern_element = ET.fromstring("<pattern><bot>A</bot></pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        pattern_element = ET.fromstring("<pattern>A</pattern>")
        topic_element = ET.fromstring("<topic>*</topic>")
        that_element = ET.fromstring("<that>*</that>")
        template_node = TemplateNode()

        graph.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

        self.assertIsNotNone(graph.root.children)
        self.assertEqual(2, len(graph.root.children))
        self.assertIsInstance(graph.root.children[0], PatternWordNode)
        self.assertIsInstance(graph.root.children[1], PatternBotNode)

        self.assertEqual(1, len(graph.root._bot_properties))
        values = graph.root._bot_properties.values()

        self.assertIsInstance(list(values)[0][0], PatternBotNode)
