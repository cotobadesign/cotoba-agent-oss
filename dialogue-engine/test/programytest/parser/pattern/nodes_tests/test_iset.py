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

from programy.parser.pattern.nodes.iset import PatternISetNode
from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException


class PatternISetNodeTests(ParserTestsBaseClass):

    def test_init_with_text(self):
        node = PatternISetNode({}, "test1, test2, test3")
        self.assertIsNotNone(node)
        self.assertFalse(node._is_CJK)
        self.assertTrue("TEST1" in node.words)
        self.assertTrue("TEST2" in node.words)
        self.assertTrue("TEST3" in node.words)

    def test_init_with_text_jp(self):
        node = PatternISetNode({}, "テスト１, テスト２, テスト３")
        self.assertIsNotNone(node)
        self.assertTrue(node._is_CJK)
        self.assertEqual(1, len(node.words))
        self.assertEqual(3, len(node.words["テ"]))
        self.assertTrue("テスト1" in node.words["テ"])
        self.assertTrue("テスト2" in node.words["テ"])
        self.assertTrue("テスト3" in node.words["テ"])

    def test_init_with_attribs(self):
        node = PatternISetNode({"words": "test1, test2, test3"}, "")
        self.assertIsNotNone(node)
        self.assertFalse(node._is_CJK)
        self.assertTrue("TEST1" in node.words)
        self.assertTrue("TEST2" in node.words)
        self.assertTrue("TEST3" in node.words)

    def test_init_with_attribs_jp(self):
        node = PatternISetNode({"words": "テスト１, テスト２, テスト３"}, "")
        self.assertIsNotNone(node)
        self.assertTrue(node._is_CJK)
        self.assertEqual(1, len(node.words))
        self.assertEqual(3, len(node.words["テ"]))
        self.assertTrue("テスト1" in node.words["テ"])
        self.assertTrue("テスト2" in node.words["テ"])
        self.assertTrue("テスト3" in node.words["テ"])

    def test_init_with_invalid_attribs(self):
        with self.assertRaises(ParserException) as raised:
            PatternISetNode({"unknwon": "test1"}, "")
        self.assertEqual(str(raised.exception), "No words specified as attribute or text")

    def test_init_with_nothing(self):
        with self.assertRaises(ParserException) as raised:
            PatternISetNode({}, "")
        self.assertEqual(str(raised.exception), "No words specified as attribute or text")

    def test_init(self):
        node = PatternISetNode({}, "test1, test2, test3")
        self.assertIsNotNone(node)
        self.assertFalse(node._is_CJK)

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
        self.assertTrue(node.is_iset())
        self.assertFalse(node.is_nlu())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertIsNotNone(node.words)
        self.assertEqual(3, len(node.words))
        self.assertTrue("TEST1" in node.words)
        self.assertTrue("TEST2" in node.words)
        self.assertTrue("TEST3" in node.words)

        self.assertTrue(node.equivalent(PatternISetNode({}, "test1, test2, test3")))

        sentence = Sentence(self._client_context.brain.tokenizer, "TEST1 TEST2 TEST3")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 1)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 2)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 3)
        self.assertFalse(result.matched)

    def test_parse_words(self):
        node = PatternISetNode({}, "test1")
        self.assertIsNotNone(node)
        self.assertFalse(node._is_CJK)
        self.assertIsNotNone(node.words)
        self.assertEqual(1, len(node.words))
        self.assertTrue("TEST1" in node.words)

        node = PatternISetNode({}, "test1,test2")
        self.assertIsNotNone(node)
        self.assertFalse(node._is_CJK)
        self.assertIsNotNone(node.words)
        self.assertEqual(2, len(node.words))
        self.assertTrue("TEST1" in node.words)
        self.assertTrue("TEST2" in node.words)

        node = PatternISetNode({}, " test1, test2 , test3 ")
        self.assertIsNotNone(node)
        self.assertIsNotNone(node.words)
        self.assertEqual(3, len(node.words))
        self.assertTrue("TEST1" in node.words)
        self.assertTrue("TEST2" in node.words)
        self.assertTrue("TEST3" in node.words)

    def test_init_jp(self):
        node = PatternISetNode({}, "テスト１, テスト２, テスト３")
        self.assertIsNotNone(node)
        self.assertTrue(node._is_CJK)

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
        self.assertTrue(node.is_iset())
        self.assertFalse(node.is_nlu())

        self.assertIsNotNone(node.children)
        self.assertFalse(node.has_children())

        self.assertIsNotNone(node.words)
        self.assertEqual(1, len(node.words))
        self.assertEqual(3, len(node.words["テ"]))
        self.assertTrue("テスト1" in node.words["テ"])
        self.assertTrue("テスト2" in node.words["テ"])
        self.assertTrue("テスト3" in node.words["テ"])

        self.assertTrue(node.equivalent(PatternISetNode({}, "テスト１, テスト２, テスト３")))

        sentence = Sentence(self._client_context.brain.tokenizer, "テスト１ テスト２ テスト３")

        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 2)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 4)
        self.assertTrue(result.matched)
        result = node.equals(self._client_context, sentence, 6)
        self.assertFalse(result.matched)

    def test_parse_words_jp(self):
        node = PatternISetNode({}, "テスト１")
        self.assertIsNotNone(node)
        self.assertTrue(node._is_CJK)
        self.assertIsNotNone(node.words)
        self.assertEqual(1, len(node.words))
        self.assertEqual(1, len(node.words["テ"]))
        self.assertTrue("テスト1" in node.words["テ"])

        node = PatternISetNode({}, "テスト１,テスト２")
        self.assertIsNotNone(node)
        self.assertTrue(node._is_CJK)
        self.assertIsNotNone(node.words)
        self.assertEqual(1, len(node.words))
        self.assertEqual(2, len(node.words["テ"]))
        self.assertTrue("テスト1" in node.words["テ"])
        self.assertTrue("テスト2" in node.words["テ"])

        node = PatternISetNode({}, " テスト１, テスト２, テスト３ ")
        self.assertIsNotNone(node)
        self.assertTrue(node._is_CJK)
        self.assertIsNotNone(node.words)
        self.assertEqual(1, len(node.words))
        self.assertEqual(3, len(node.words["テ"]))
        self.assertTrue("テスト1" in node.words["テ"])
        self.assertTrue("テスト2" in node.words["テ"])
        self.assertTrue("テスト3" in node.words["テ"])

    def test_to_xml(self):
        node1 = PatternISetNode({}, "test1, test2, test3")
        self.assertEqual('<iset words="TEST1, TEST2, TEST3"></iset>\n', node1.to_xml(self._client_context))

        node2 = PatternISetNode({}, "test1, test2, test3", userid="testid")
        self.assertEqual('<iset words="TEST1, TEST2, TEST3"></iset>\n', node2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<iset userid="testid" words="TEST1, TEST2, TEST3"></iset>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        node1 = PatternISetNode({}, "test1, test2, test3")
        self.assertEqual(node1.to_string(verbose=False), "ISET words=[TEST1,TEST2,TEST3]")
        self.assertEqual(node1.to_string(verbose=True), "ISET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[TEST1,TEST2,TEST3]")

        node2 = PatternISetNode({}, "test1, test2, test3", userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "ISET words=[TEST1,TEST2,TEST3]")
        self.assertEqual(node2.to_string(verbose=True), "ISET [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[TEST1,TEST2,TEST3]")

    def test_equivalent(self):
        node1 = PatternISetNode({}, "test1, test2, test3")
        node2 = PatternISetNode({}, "test1, test2, test3")
        node3 = PatternISetNode({}, "test1, test2, test3", userid="testid")
        node4 = PatternISetNode({}, "test1, test2, test3, test4")
        node5 = PatternISetNode({}, "test1, test2, test4")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))
        self.assertFalse(node1.equivalent(node4))
        self.assertFalse(node1.equivalent(node5))

    def test_to_xml_jp(self):
        node1 = PatternISetNode({}, "テスト１, テスト２, テスト３")
        self.assertEqual('<iset words="テスト1, テスト2, テスト3"></iset>\n', node1.to_xml(self._client_context))

        node2 = PatternISetNode({}, "テスト１, テスト２, テスト３", userid="testid")
        self.assertEqual('<iset words="テスト1, テスト2, テスト3"></iset>\n', node2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<iset userid="testid" words="テスト1, テスト2, テスト3"></iset>\n', node2.to_xml(self._client_context, include_user=True))

    def test_to_string_jp(self):
        node1 = PatternISetNode({}, "テスト１, テスト２, テスト３")
        self.assertEqual(node1.to_string(verbose=False), "ISET words=[テスト1,テスト2,テスト3]")
        self.assertEqual(node1.to_string(verbose=True), "ISET [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[テスト1,テスト2,テスト3]")

        node2 = PatternISetNode({}, "テスト１, テスト２, テスト３", userid="testid")
        self.assertEqual(node2.to_string(verbose=False), "ISET words=[テスト1,テスト2,テスト3]")
        self.assertEqual(node2.to_string(verbose=True), "ISET [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] words=[テスト1,テスト2,テスト3]")

    def test_equivalent_jp(self):
        node1 = PatternISetNode({}, "テスト１, テスト２, テスト３")
        node2 = PatternISetNode({}, "テスト１, テスト２, テスト３")
        node3 = PatternISetNode({}, "テスト１, テスト２, テスト３", userid="testid")
        node4 = PatternISetNode({}, "テスト１, テスト２, テスト３, テスト４")
        node5 = PatternISetNode({}, "テスト１, テスト２, テスト４")

        self.assertTrue(node1.equivalent(node2))
        self.assertFalse(node1.equivalent(node3))
        self.assertFalse(node1.equivalent(node4))
        self.assertFalse(node1.equivalent(node5))

    def test_equals(self):
        node1 = PatternISetNode({}, "test1, test2, test3")
        node2 = PatternISetNode({}, "test1, test2, test3", userid="testid")
        node3 = PatternISetNode({}, "test1, test2, test3", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'test1'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'test1'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'test1'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equals_jp(self):
        node1 = PatternISetNode({}, "テスト１, テスト２, テスト３")
        node2 = PatternISetNode({}, "テスト１, テスト２, テスト３", userid="testid")
        node3 = PatternISetNode({}, "テスト１, テスト２, テスト３", userid="testid2")

        match1 = node1.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'テスト１'), 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = node2.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'テスト１'), 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = node3.equals(self._client_context, Sentence(self._client_context.brain.tokenizer, 'テスト１'), 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)
