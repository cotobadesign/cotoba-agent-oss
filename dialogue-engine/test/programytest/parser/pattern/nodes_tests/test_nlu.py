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

from programy.parser.pattern.nodes.nlu import PatternNluNode
from programy.dialog.question import Question
from programy.dialog.sentence import Sentence
from programy.parser.exceptions import ParserException

from operator import gt, ge, eq, le, lt


class PatternNluNodeTests(ParserTestsBaseClass):

    def test_init_with_attribs_intent(self):
        node = PatternNluNode({"intent": "test1"}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertTrue(node.maxLikelihood)
        self.assertIsNone(node.score)
        self.assertIsNone(node.scoreOperator)

    def test_init_with_attribs_maxLikelihood(self):
        node = PatternNluNode({"intent": "test1", "maxLikelihood": "False"}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertFalse(node.maxLikelihood)
        self.assertIsNone(node.score)
        self.assertIsNone(node.scoreOperator)

    def test_init_with_attribs_scoreGt(self):
        node = PatternNluNode({"intent": "test1", "scoreGt": 0.9}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertFalse(node.maxLikelihood)
        self.assertEqual(node.score, 0.9)
        self.assertEqual(node.scoreOperator, gt)

    def test_init_with_attribs_scoreGe(self):
        node = PatternNluNode({"intent": "test1", "scoreGe": 0.8}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertFalse(node.maxLikelihood)
        self.assertEqual(node.score, 0.8)
        self.assertEqual(node.scoreOperator, ge)

    def test_init_with_attribs_score(self):
        node = PatternNluNode({"intent": "test1", "score": 0.7}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertFalse(node.maxLikelihood)
        self.assertEqual(node.score, 0.7)
        self.assertEqual(node.scoreOperator, eq)

    def test_init_with_attribs_scoreLe(self):
        node = PatternNluNode({"intent": "test1", "scoreLe": 0.6}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertFalse(node.maxLikelihood)
        self.assertEqual(node.score, 0.6)
        self.assertEqual(node.scoreOperator, le)

    def test_init_with_attribs_scoreLt(self):
        node = PatternNluNode({"intent": "test1", "scoreLt": 0.5}, None)
        self.assertIsNotNone(node)
        self.assertEqual("test1", node.intent)
        self.assertFalse(node.maxLikelihood)
        self.assertEqual(node.score, 0.5)
        self.assertEqual(node.scoreOperator, lt)

    def test_init_with_invalid_attribs(self):
        with self.assertRaises(ParserException) as raised:
            PatternNluNode({"unknwon": "test1"}, None)
        self.assertEqual(str(raised.exception), "Missing intent attribute")

    def test_init_with_nothing(self):
        with self.assertRaises(ParserException) as raised:
            PatternNluNode({}, None)
        self.assertEqual(str(raised.exception), "Missing intent attribute")

    def test_init(self):

        node = PatternNluNode({"intent": "test1"}, None)
        self.assertIsNotNone(node)

        self.assertFalse(node.is_root())
        self.assertFalse(node.is_priority())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_zero_or_more())
        self.assertFalse(node.is_one_or_more())
        self.assertFalse(node.is_bot())
        self.assertFalse(node.is_set())
        self.assertFalse(node.is_template())
        self.assertFalse(node.is_that())
        self.assertFalse(node.is_topic())
        self.assertFalse(node.is_wildcard())
        self.assertFalse(node.is_iset())
        self.assertTrue(node.is_nlu())

        self.assertTrue(node.equivalent(PatternNluNode({"intent": "test1"}, None)))
        self.assertFalse(node.equivalent(PatternNluNode({"intent": "test2"}, None)))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        sentence = Sentence(self._client_context.brain.tokenizer, "YEMPTY")

        self._client_context.match_nlu = True

        nlu_result = '{"intents": [{"intent": "test1", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)
        result = node.equals(self._client_context, sentence, 0)
        self.assertTrue(result.matched)
        self.assertEqual(0, result.word_no)

        nlu_result = '{"intents": [{"intent": "test2", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)
        result = node.equals(self._client_context, sentence, 0)
        self.assertFalse(result.matched)
        self.assertEqual(0, result.word_no)

        self.assertEqual(node.to_string(), "NLU [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[test1] score=[None]")
        self.assertEqual('<nlu intent="test1">\n</nlu>', node.to_xml(self._client_context))

    def test_to_xml(self):
        nlu1 = PatternNluNode({"intent": "intent1"}, None)
        self.assertEqual('<nlu intent="intent1">\n</nlu>', nlu1.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="*" intent="intent1">\n</nlu>', nlu1.to_xml(self._client_context, include_user=True))

        nlu2 = PatternNluNode({"intent": "intent2", "maxLikelihood": "false"}, None)
        self.assertEqual('<nlu intent="intent2" maxLikelihood="false">\n</nlu>', nlu2.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="*" intent="intent2" maxLikelihood="false">\n</nlu>', nlu2.to_xml(self._client_context, include_user=True))

        nlu3 = PatternNluNode({"intent": "intent3", "scoreGt": "0.9"}, None)
        self.assertEqual('<nlu intent="intent3" scoreGt="0.90">\n</nlu>', nlu3.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="*" intent="intent3" scoreGt="0.90">\n</nlu>', nlu3.to_xml(self._client_context, include_user=True))

        nlu4 = PatternNluNode({"intent": "intent4", "scoreGe": "0.8"}, None, userid="testid")
        self.assertEqual('<nlu intent="intent4" scoreGe="0.80">\n</nlu>', nlu4.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="testid" intent="intent4" scoreGe="0.80">\n</nlu>', nlu4.to_xml(self._client_context, include_user=True))

        nlu5 = PatternNluNode({"intent": "intent5", "score": "0.7"}, None, userid="testid")
        self.assertEqual('<nlu intent="intent5" score="0.70">\n</nlu>', nlu5.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="testid" intent="intent5" score="0.70">\n</nlu>', nlu5.to_xml(self._client_context, include_user=True))

        nlu6 = PatternNluNode({"intent": "intent6", "scoreLe": "0.6"}, None, userid="testid")
        self.assertEqual('<nlu intent="intent6" scoreLe="0.60">\n</nlu>', nlu6.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="testid" intent="intent6" scoreLe="0.60">\n</nlu>', nlu6.to_xml(self._client_context, include_user=True))

        nlu7 = PatternNluNode({"intent": "intent7", "scoreLt": "0.5"}, None, userid="testid")
        self.assertEqual('<nlu intent="intent7" scoreLt="0.50">\n</nlu>', nlu7.to_xml(self._client_context, include_user=False))
        self.assertEqual('<nlu userid="testid" intent="intent7" scoreLt="0.50">\n</nlu>', nlu7.to_xml(self._client_context, include_user=True))

    def test_to_string(self):
        nlu1 = PatternNluNode({"intent": "intent1"}, None)
        self.assertEqual('NLU intent=[intent1] score=[None]', nlu1.to_string(verbose=False))
        self.assertEqual('NLU [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent1] score=[None]', nlu1.to_string(verbose=True))

        nlu2 = PatternNluNode({"intent": "intent2", "maxLikelihood": "false"}, None)
        self.assertEqual('NLU intent=[intent2] score=[None] maxLikelihood=[False]', nlu2.to_string(verbose=False))
        self.assertEqual('NLU [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent2] score=[None] maxLikelihood=[False]', nlu2.to_string(verbose=True))

        nlu3 = PatternNluNode({"intent": "intent3", "scoreGt": "0.9"}, None)
        self.assertEqual('NLU intent=[intent3] score=[0.90 scoreGt]', nlu3.to_string(verbose=False))
        self.assertEqual('NLU [*] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent3] score=[0.90 scoreGt]', nlu3.to_string(verbose=True))

        nlu4 = PatternNluNode({"intent": "intent4", "scoreGe": "0.8"}, None, userid="testid")
        self.assertEqual('NLU intent=[intent4] score=[0.80 scoreGe]', nlu4.to_string(verbose=False))
        self.assertEqual('NLU [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent4] score=[0.80 scoreGe]', nlu4.to_string(verbose=True))

        nlu5 = PatternNluNode({"intent": "intent5", "score": "0.7"}, None, userid="testid")
        self.assertEqual('NLU intent=[intent5] score=[0.70 score]', nlu5.to_string(verbose=False))
        self.assertEqual('NLU [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent5] score=[0.70 score]', nlu5.to_string(verbose=True))

        nlu6 = PatternNluNode({"intent": "intent6", "scoreLe": "0.6"}, None, userid="testid")
        self.assertEqual('NLU intent=[intent6] score=[0.60 scoreLe]', nlu6.to_string(verbose=False))
        self.assertEqual('NLU [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent6] score=[0.60 scoreLe]', nlu6.to_string(verbose=True))

        nlu7 = PatternNluNode({"intent": "intent7", "scoreLt": "0.5"}, None, userid="testid")
        self.assertEqual('NLU intent=[intent7] score=[0.50 scoreLt]', nlu7.to_string(verbose=False))
        self.assertEqual('NLU [testid] [P(0)^(0)#(0)C(0)_(0)*(0)To(0)Th(0)Te(0)] intent=[intent7] score=[0.50 scoreLt]', nlu7.to_string(verbose=True))

    def test_equals_intent(self):
        nlu1 = PatternNluNode({"intent": "test"}, None)
        nlu2 = PatternNluNode({"intent": "test"}, None)
        nlu3 = PatternNluNode({"intent": "test"}, None, userid="testid")
        nlu4 = PatternNluNode({"intent": "test", "maxLikelihood": "false"}, "")
        nlu5 = PatternNluNode({"intent": "test", "score": "0.7"}, "")

        self.assertTrue(nlu1.equivalent(nlu2))
        self.assertFalse(nlu1.equivalent(nlu3))
        self.assertFalse(nlu1.equivalent(nlu4))
        self.assertFalse(nlu1.equivalent(nlu5))

    def test_equals_text(self):
        nlu1 = PatternNluNode({"intent": "test"}, "nlu1")
        nlu2 = PatternNluNode({"intent": "test"}, "nlu2")
        nlu3 = PatternNluNode({"intent": "test"}, "nlu1", userid="testid")

        self.assertTrue(nlu1.equivalent(nlu2))
        self.assertFalse(nlu1.equivalent(nlu3))

    def test_equivalent_intent(self):
        nlu1 = PatternNluNode({"intent": "test"}, None)
        nlu2 = PatternNluNode({"intent": "test"}, None, userid="testid")
        nlu3 = PatternNluNode({"intent": "test"}, None, userid="testid2")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        sentence = Sentence(self._client_context.brain.tokenizer, "YEMPTY")
        nlu_result = '{"intents": [{"intent": "test", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        self._client_context.match_nlu = True

        match1 = nlu1.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = nlu2.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = nlu3.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

    def test_equivalent_score(self):
        nlu1 = PatternNluNode({"intent": "test", "score": 0.9}, None)
        nlu2 = PatternNluNode({"intent": "test", "score": 0.9}, None, userid="testid")
        nlu3 = PatternNluNode({"intent": "test", "score": 0.9}, None, userid="testid2")
        nlu4 = PatternNluNode({"intent": "test", "scoreGt": 0.9}, None)
        nlu5 = PatternNluNode({"intent": "test", "scoreGe": 0.9}, None)
        nlu6 = PatternNluNode({"intent": "test", "scoreLe": 0.9}, None)
        nlu7 = PatternNluNode({"intent": "test", "scoreLt": 0.9}, None)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        sentence = Sentence(self._client_context.brain.tokenizer, "YEMPTY")
        nlu_result = '{"intents": [{"intent": "test", "score": 0.9}], "slots": []}'
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", nlu_result)

        self._client_context.match_nlu = True

        match1 = nlu1.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match1)
        self.assertTrue(match1.matched)

        match2 = nlu2.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match2)
        self.assertTrue(match2.matched)

        match3 = nlu3.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match3)
        self.assertFalse(match3.matched)

        match4 = nlu4.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match4)
        self.assertFalse(match4.matched)

        match5 = nlu5.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match5)
        self.assertTrue(match5.matched)

        match6 = nlu6.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match6)
        self.assertTrue(match6.matched)

        match7 = nlu7.equals(self._client_context, sentence, 0)
        self.assertIsNotNone(match7)
        self.assertFalse(match7.matched)
