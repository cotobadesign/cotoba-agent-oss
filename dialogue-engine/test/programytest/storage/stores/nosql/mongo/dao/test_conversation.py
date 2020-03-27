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

from programy.storage.stores.nosql.mongo.dao.conversation import Conversation

from programy.dialog.question import Question
from programy.dialog.conversation import Conversation as Convo

from programytest.client import TestClient


class ConversationTests(unittest.TestCase):

    def test_init_blank(self):
        conversation1 = Conversation(None, None)
        self.assertIsNotNone(conversation1)
        self.assertIsNone(conversation1.clientid)
        self.assertIsNone(conversation1.userid)
        self.assertIsNone(conversation1.botid)
        self.assertIsNone(conversation1.brainid)
        self.assertIsNone(conversation1.conversation)

    def test_init_context_and_converstion(self):

        client = TestClient()
        client_context = client.create_client_context("tesuser")

        convo = Convo(client_context)

        question = Question.create_from_text(client_context, "Hello world")
        question.current_sentence()._response = "Hello matey"
        convo.record_dialog(question)

        conversation = Conversation(client_context, convo)
        self.assertIsNotNone(conversation)

        self.assertEqual(client_context.client.id, conversation.clientid)
        self.assertEqual(client_context.userid, conversation.userid)
        self.assertEqual(client_context.bot.id, conversation.botid)
        self.assertEqual(client_context.brain.id, conversation.brainid)
        self.assertIsNotNone(conversation.conversation)

        doc = conversation.to_document()
        self.assertEqual({'botid': 'bot', 'brainid': 'brain', 'clientid': 'testclient', 'userid': 'tesuser',
                          'conversation': {
                             'categories': 0, 'data_properties': {}, 'exception': None, 'max_histories': 100,
                             'properties': {'topic': '*'}, 'user_categories': 0,
                             'client_context': {
                                'botid': 'bot', 'brainid': 'brain', 'clientid': 'testclient', 'depth': 0,
                                'userid': 'tesuser'},
                             'questions': [{
                                'data_properties': {}, 'exception': None, 'name_properties': {},
                                'srai': False, 'var_properties': {},
                                'sentences': [{
                                    'matched_node': {}, 'positivity': 0.0, 'question': 'Hello world',
                                    'response': 'Hello matey', 'subjectivity': 0.5}]}]
                            }},
                         doc)

        conversation2 = Conversation.from_document(client_context, doc)
        self.assertIsNotNone(conversation2)
        self.assertEqual(conversation2.clientid, conversation.clientid)
        self.assertEqual(conversation2.userid, conversation.userid)
        self.assertEqual(conversation2.botid, conversation.botid)
        self.assertEqual(conversation2.brainid, conversation.brainid)
