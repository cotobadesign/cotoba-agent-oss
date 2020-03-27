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

from programy.dialog.question import Question

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherNluTests(PatternMatcherBaseClass):

    NLU_RESULT = '{"intents": [' + \
                        '{"intent": "transportation", "score": 0.9},' + \
                        '{"intent": "aroundsearch", "score": 0.8}],' + \
                 '"slots": [' + \
                        '{"slot": "departure", "entity": "東京", "score": 0.85, "startOffset": 3, "endOffset": 5},' + \
                        '{"slot": "arrival", "entity": "京都", "score": 0.86, "startOffset": 8, "endOffset": 10},' + \
                        '{"slot": "departure_time", "entity": "2018/11/1 19:00", "score": 0.87, "startOffset": 12, "endOffset": 14},' + \
                        '{"slot": "arrival_time", "entity": "2018/11/1 11:00", "score": 0.88, "startOffset": 13, "endOffset": 18}]' + \
                 '}'

    def test_nlu_match_as_1st_match(self):

        self.add_pattern_to_graph(pattern='<nlu intent="transportation" />', topic="*", that="*", template="1")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", self.NLU_RESULT)

        self._client_context.match_nlu = True

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

    def test_nlu_match_as_2nd_no_match(self):

        self.add_pattern_to_graph(pattern='<nlu intent="aroundsearch" maxLikelihood="true" />', topic="*", that="*", template="1")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", self.NLU_RESULT)

        self._client_context.match_nlu = True

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNone(context)

    def test_nlu_match_as_2nd_match(self):

        self.add_pattern_to_graph(pattern='<nlu intent="aroundsearch" maxLikelihood="false"/>', topic="*", that="*", template="1")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", self.NLU_RESULT)

        self._client_context.match_nlu = True

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

    def test_nlu_match_as_no_question(self):

        self.add_pattern_to_graph(pattern='<nlu intent="transportation"/>', topic="*", that="*", template="1")

        self._client_context.match_nlu = True

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNone(context)

    def test_nlu_match_as_no_nlu_result(self):

        self.add_pattern_to_graph(pattern='<nlu intent="transportation"/>', topic="*", that="*", template="1")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNone(context)

    def test_nlu_match_as_invlid_nlu_result(self):

        invalid_result = '{"intent": "transportation", "score": 0.9, "slot": "departure", "entity": "東京"}'

        self.add_pattern_to_graph(pattern='<nlu intent="transportation" />', topic="*", that="*", template="1")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", invalid_result)

        self._client_context.match_nlu = True

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNone(context)

    def test_nlu_match_as_invlid_nlu_jsonform(self):

        invalid_result = '{"intent": "transportation", invalid, "score": 0.9, "slot": "departure", "entity": "東京"}'

        self.add_pattern_to_graph(pattern='<nlu intent="transportation" />', topic="*", that="*", template="1")

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        conversation.current_question().set_property("__SYSTEM_NLUDATA__", invalid_result)

        self._client_context.match_nlu = True

        context = self.match_sentence("YEMPTY", topic="*", that="*")
        self.assertIsNone(context)
