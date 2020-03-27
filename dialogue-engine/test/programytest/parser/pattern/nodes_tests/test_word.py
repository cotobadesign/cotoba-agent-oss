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

from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.bot import PatternBotNode
from programy.dialog.sentence import Sentence


class PatternWordNodeTests(ParserTestsBaseClass):

    def test_init(self):
        node = PatternWordNode("test1")

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_iset())
        self.assertFalse(node.is_nlu())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        sentence = Sentence(self._client_context.brain.tokenizer, "test1 test")

        self.assertTrue(node.equivalent(PatternWordNode("test1")))
        self.assertFalse(node.equivalent(PatternWordNode("test2")))
        self.assertFalse(node.equivalent(PatternBotNode([], "test1")))

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 1)
        self.assertFalse(result.matched)
        self.assertEqual(node.to_string(), "WORD [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

        node.add_child(PatternWordNode("test2"))
        self.assertEqual(len(node.children), 1)
        self.assertEqual(node.to_string(), "WORD [*] [P(0)^(0)#(0)C(1)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]")

    def test_to_xml(self):
        word1 = PatternWordNode("test1")
        self.assertEqual('<word word="test1"></word>\n', word1.to_xml(self._client_context))
        self.assertEqual('<word userid="*" word="test1"></word>\n', word1.to_xml(self._client_context, include_user=True))

        word2 = PatternWordNode("test2", userid="testid")
        self.assertEqual('<word word="test2"></word>\n', word2.to_xml(self._client_context))
        self.assertEqual('<word userid="testid" word="test2"></word>\n', word2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        word1 = PatternWordNode("test1")
        self.assertEqual("WORD [test1]", word1.to_string(verbose=False))
        self.assertEqual("WORD [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test1]", word1.to_string(verbose=True))

        word2 = PatternWordNode("test2", "testid")
        self.assertEqual("WORD [test2]", word2.to_string(verbose=False))
        self.assertEqual("WORD [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] word=[test2]", word2.to_string(verbose=True))

    def test_equivalent(self):
        word1 = PatternWordNode("word")
        word2 = PatternWordNode("word")
        word3 = PatternWordNode("word", userid="testuser")

        self.assertTrue(word1.equivalent(word2))
        self.assertFalse(word1.equivalent(word3))

    def test_equals(self):
        word1 = PatternWordNode("word")
        word2 = PatternWordNode("word", userid="testid")
        word3 = PatternWordNode("word", userid="testid2")

        match1 = word1.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'word'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = word2.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'word'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = word3.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'word'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)
