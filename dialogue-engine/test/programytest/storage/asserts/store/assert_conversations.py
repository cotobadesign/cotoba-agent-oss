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

from programy.dialog.question import Question
from programy.dialog.conversation import Conversation

from programytest.client import TestClient


class ConverstionStoreAsserts(unittest.TestCase):

    def assert_conversation_storage(self, store, can_empty=True, test_load=True):

        if can_empty is True:
            store.empty()

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)
        store.commit()

        if test_load is True:
            conversation2 = Conversation(client_context)
            store.load_conversation(client_context, conversation2)

            self.assertEqual(1, len(conversation2.questions))
            self.assertEqual(1, len(conversation2.questions[0].sentences))
            self.assertEqual("Hello There", conversation2.questions[0].sentences[0].text())
            self.assertEqual("Hi", conversation2.questions[0].sentences[0].response)

    def assert_debug_conversation(self, store):

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.store_conversation(client_context, conversation)
        store.commit()

        debugInfo = store.debug_conversation_data(client_context)
        self.assertIsNotNone(debugInfo)
        self.assertIsNotNone(debugInfo['conversations'])
        conversations = debugInfo['conversations']
        self.assertIsNotNone(conversations['questions'])
        self.assertEqual(1, len(conversations['questions']))
        question = conversations['questions'][0]
        self.assertEqual(1, len(question['sentences']))
        sentence = question['sentences'][0]
        self.assertEqual("Hello There", sentence['question'])
        self.assertEqual("Hi", sentence['response'])

    def assert_modify_conversation_data(self, store):

        client = TestClient()
        client_context = client.create_client_context("user1")

        conversation = Conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)

        store.modify_conversation_data(client_context, conversation)
        store.commit()

        debugInfo = store.debug_conversation_data(client_context)
        self.assertIsNotNone(debugInfo)
        self.assertIsNotNone(debugInfo['conversations'])
        conversations = debugInfo['conversations']
        self.assertIsNotNone(conversations['questions'])
        self.assertEqual(1, len(conversations['questions']))
        question = conversations['questions'][0]
        self.assertEqual(1, len(question['sentences']))
        sentence = question['sentences'][0]
        self.assertEqual("Hello There", sentence['question'])
        self.assertEqual("Hi", sentence['response'])
