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
from programy.parser.pattern.nodes.wildcard import PatternWildCardNode
from programy.parser.pattern.nodes.zeroormore import PatternZeroOrMoreWildCardNode
from programy.parser.pattern.nodes.oneormore import PatternOneOrMoreWildCardNode
from programy.parser.pattern.nodes.word import PatternWordNode
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.topic import PatternTopicNode
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.pattern.nodes.template import PatternTemplateNode
from programy.parser.pattern.matcher import MatchContext, Match
from programy.dialog.sentence import Sentence


class MockPatternWildCardNode(PatternWildCardNode):

    def __init__(self, wildcard):
        PatternWildCardNode.__init__(self, wildcard)

    def matching_wildcards(self):
        return ["*"]


class PatternWildCardNodeTests(ParserTestsBaseClass):

    def test_wildcard(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)

        self.assertTrue(wildcard.is_wildcard())

        with self.assertRaises(ParserException):
            wildcard.can_add(PatternRootNode())

        wildcard.can_add(PatternWordNode("test"))

        self.assertEqual(["*"], wildcard.matching_wildcards())

    def test_invalid_topic_or_that(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        matches_added = 1

        self.assertTrue(wildcard.invalid_topic_or_that("", self._client_context, PatternTopicNode.TOPIC, context, matches_added))
        self.assertTrue(wildcard.invalid_topic_or_that("", self._client_context, PatternTopicNode.THAT, context, matches_added))

        self.assertFalse(wildcard.invalid_topic_or_that("", self._client_context, "TEST", context, matches_added))

    def test_check_child_is_wildcard_no_wildcard_children(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNone(match)

    def test_check_child_is_wildcard_hash(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._0ormore_hash = PatternZeroOrMoreWildCardNode('#')
        wildcard._0ormore_hash._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

    def test_check_child_is_wildcard_arrow(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._0ormore_arrow = PatternZeroOrMoreWildCardNode('^')
        wildcard._0ormore_arrow._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

    def test_check_child_is_wildcard_star(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._1ormore_star = PatternOneOrMoreWildCardNode('*')
        wildcard._1ormore_star._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0, Match.WORD, 0)
        self.assertIsNone(match)

    def test_check_child_is_wildcard_underline(self):

        wildcard = MockPatternWildCardNode("*")
        self.assertIsNotNone(wildcard)
        wildcard._1ormore_underline = PatternOneOrMoreWildCardNode('_')
        wildcard._1ormore_underline._template = PatternTemplateNode(TemplateNode())

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST SENTENCE")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNotNone(match)

        context = MatchContext(max_search_depth=100, max_search_timeout=-1, tokenizer=self._client_context.brain.tokenizer)
        sentence = Sentence(self._client_context.brain.tokenizer, "TEST")
        match = wildcard.check_child_is_wildcard("", self._client_context, context, sentence, 0,  Match.WORD, 0)
        self.assertIsNone(match)
