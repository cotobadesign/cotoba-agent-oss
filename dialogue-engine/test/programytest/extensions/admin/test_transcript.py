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

from programy.extensions.admin.transcript import TranscriptAdminExtension
from programy.dialog.sentence import Sentence
from programy.dialog.question import Question
from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class TranscriptAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(TranscriptAdminExtensionClient, self).load_configuration(arguments, subs)


class TranscriptAdminExtensionTests(unittest.TestCase):

    def test_transcripts_no_questions_without_props(self):
        client = TranscriptAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.bot.get_conversation(client_context)

        extension = TranscriptAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "")
        self.assertIsNotNone(result)
        self.assertEqual("Questions:<br /><ul></ul><br />", result)

    def test_transcripts_questions_without_props(self):
        client = TranscriptAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question.create_from_sentence(Sentence(client_context.brain.tokenizer, "Hello World"))
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)

        extension = TranscriptAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "")
        self.assertIsNotNone(result)
        self.assertEqual("Questions:<br /><ul><li>Hello World - </li></ul><br />", result)

    def test_transcripts_questions_with_props(self):
        client = TranscriptAdminExtensionClient()
        client_context = client.create_client_context("testid")

        question = Question.create_from_sentence(Sentence(client_context.brain.tokenizer, "Hello World"))
        conversation = client_context.bot.get_conversation(client_context)
        conversation.record_dialog(question)

        extension = TranscriptAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "PROPERTIES")
        self.assertIsNotNone(result)
        self.assertEqual("Questions:<br /><ul><li>Hello World - </li></ul><br />Properties:<br /><ul><li>topic = *</li></ul><br />", result)
