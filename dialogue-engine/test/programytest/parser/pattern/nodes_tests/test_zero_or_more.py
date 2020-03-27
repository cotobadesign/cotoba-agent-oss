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
from programytest.parser.base import ParserTestsBaseClass

from programy.parser.exceptions import ParserException
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.dialog.sentence import Sentence


class PatternZeroOrMoreWildCardNodeTests(ParserTestsBaseClass):

    def test_invalid_wildcard(self):
        with self.assertRaises(ParserException):
            node = PatternZeroOrMoreWildCardNode("X")
            self.assertIsNone(node)

    def test_hash(self):
        node = PatternZeroOrMoreWildCardNode("#")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())
        self.assertFalse(node.is_iset())
        self.assertFalse(node.is_nlu())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context.brain.tokenizer, "*")

        self.assertEqual(node.wildcard, "#")
        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("#")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ZEROORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[#]")
        self.assertEqual('<zerormore wildcard="#">\n</zerormore>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternWordNode("test")))

    def test_arrow(self):
        node = PatternZeroOrMoreWildCardNode("^")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertTrue(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertTrue(node.is_wildcard())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context.brain.tokenizer, "*")

        self.assertEqual(node.wildcard, "^")
        self.assertTrue(node.equivalent(PatternZeroOrMoreWildCardNode("^")))
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "ZEROORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]")
        self.assertEqual('<zerormore wildcard="^">\n</zerormore>\n', node.to_xml(self._client_context))

        self.assertFalse(node.equivalent(PatternWordNode("test")))

    def test_to_xml(self):
        node1 = PatternZeroOrMoreWildCardNode("^")
        self.assertEqual('<zerormore wildcard="^">\n</zerormore>\n', node1.to_xml(self._client_context))
        self.assertEqual('<zerormore userid="*" wildcard="^">\n</zerormore>\n', node1.to_xml(self._client_context, include_user=True))

        node2 = PatternZeroOrMoreWildCardNode("^", userid="testid")
        self.assertEqual('<zerormore wildcard="^">\n</zerormore>\n', node2.to_xml(self._client_context))
        self.assertEqual('<zerormore userid="testid" wildcard="^">\n</zerormore>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternZeroOrMoreWildCardNode("^")
        self.assertEqual("ZEROORMORE [^]", node1.to_string(verbose=False))
        self.assertEqual("ZEROORMORE [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]", node1.to_string(verbose=True))

        node1 = PatternZeroOrMoreWildCardNode("^", userid="testid")
        self.assertEqual("ZEROORMORE [^]", node1.to_string(verbose=False))
        self.assertEqual("ZEROORMORE [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] wildcard=[^]", node1.to_string(verbose=True))

    def test_equivalent_userid(self):
        node1 = PatternZeroOrMoreWildCardNode("^")
        node2 = PatternZeroOrMoreWildCardNode("^")
        node3 = PatternZeroOrMoreWildCardNode("^", userid="testuser")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))
