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
import unittest

from programy.dialog.sentence import Sentence
from programy.dialog.question import Question
from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration

from programytest.client import TestClient


class QuestionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        self._client_context = client.create_client_context("test1")
        bot_config = BotConfiguration()
        bot_config.conversations._max_histories = 3
        self._bot = Bot(bot_config, client)

    def test_question_no_sentences_empty(self):
        question = Question.create_from_text(self._client_context, "")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_no_sentences_blank(self):
        question = Question.create_from_text(self._client_context, " ")
        self.assertIsNotNone(question)
        self.assertEqual(0, len(question.sentences))

    def test_question_one_sentence(self):
        question = Question.create_from_text(self._client_context, "Hello There")
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))

    def test_question_multi_sentence(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertIsNotNone(question)
        self.assertEqual(2, len(question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text())
        self.assertEqual("How Are you", question.sentence(1).text())
        with self.assertRaises(Exception):
            question.sentence(2)

    def test_question_create_from_sentence(self):
        sentence = Sentence(self._client_context.brain.tokenizer, "One Two Three")
        question = Question.create_from_sentence(sentence)
        self.assertIsNotNone(question)
        self.assertEqual(1, len(question.sentences))
        self.assertEqual(sentence.text(), question.sentence(0).text())
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_question_create_from_question(self):
        question = Question.create_from_text(self._client_context, "Hello There")
        new_question = Question.create_from_question(question)
        self.assertIsNotNone(new_question)
        self.assertEqual(1, len(new_question.sentences))
        self.assertEqual("Hello There", question.sentence(0).text())
        with self.assertRaises(Exception):
            question.sentence(1)

    def test_combine_answers(self):
        question = Question()
        sentence1 = Sentence(self._client_context.brain.tokenizer, "Hi")
        sentence1._response = "Hello"
        question._sentences.append(sentence1)
        sentence2 = Sentence(self._client_context.brain.tokenizer, "Hi Again")
        question._sentences.append(sentence2)
        sentence2._response = "World"

        self.assertEqual(2, len(question._sentences))
        self.assertEqual(question._sentences[0]._response, "Hello")
        self.assertEqual(question._sentences[1]._response, "World")

        sentences = question.combine_sentences(self._client_context)
        self.assertEqual("Hi. Hi Again", sentences)

        combined = question.combine_answers(self._client_context)
        self.assertIsNotNone(combined)
        self.assertEqual(combined, "Hello. World")

    def test_next_previous_sentences(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text())
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text())

    def test_next_previous_nth_sentences(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("How Are you", question.current_sentence().text())
        self.assertEqual("How Are you", question.previous_nth_sentence(0).text())
        self.assertEqual("Hello There", question.previous_nth_sentence(1).text())

    def test_debug_info(self):
        question = Question.create_from_text(self._client_context, "Hello There. How Are you")
        self.assertEqual("Hello There = N/A, How Are you = N/A, ", question.debug_info())
