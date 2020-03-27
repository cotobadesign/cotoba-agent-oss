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
import shutil
import os

from programy.config.bot.conversations import BotConversationsConfiguration
from programy.dialog.convo_mgr import ConversationManager
from programy.dialog.question import Question

from programytest.client import TestClient


class ConversationManagerTests(unittest.TestCase):

    def test_init(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        self.assertEqual(mgr.configuration, config)
        self.assertIsNone(mgr.storage)
        self.assertEqual(mgr.conversations, {})

    def test_initialise(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)
        self.assertIsNotNone(mgr.storage)

    def test_conversation_operations(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")

        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)
        mgr.save_conversation(client_context)

        question2 = Question.create_from_text(client_context, "Hello There Again")
        question2.sentence(0).response = "Hi Again"
        conversation.record_dialog(question2)
        mgr.save_conversation(client_context)

        question3 = Question.create_from_text(client_context, "Hello There Again Again")
        question3.sentence(0).response = "Hi Again Again"
        conversation.record_dialog(question3)
        mgr.save_conversation(client_context)
        self.assertTrue(os.path.exists("./storage/conversations/testclient_user1.conv"))

        self.assertEqual(len(mgr.conversations), 1)
        mgr.empty()
        self.assertEqual(len(mgr.conversations), 0)

        conversation = mgr.get_conversation(client_context)
        self.assertEqual(len(mgr.conversations), 1)

        self.assertIsNotNone(conversation)
        self.assertEqual(len(conversation.questions), 3)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

    def test_get_conversation_multi_client(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)
        mgr.configuration._multi_client = True

        client_context = client.create_client_context("user1")

        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)
        mgr.save_conversation(client_context)

        conversation = mgr.get_conversation(client_context)
        self.assertEqual(len(mgr.conversations), 1)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

    def test_save_conversation_no_userid_data(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")
        mgr.get_conversation(client_context)
        self.assertEqual(len(mgr.conversations), 1)

        mgr.save_conversation(client_context)
        self.assertFalse(os.path.exists("./storage/conversations/testclient_user1.conv"))

    def test_save_conversation_invalid_userid(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")
        self.assertEqual(len(mgr.conversations), 0)
        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)
        mgr.save_conversation(client_context)
        self.assertTrue(os.path.exists("./storage/conversations/testclient_user1.conv"))

        client_context._userid = "user2"
        mgr.save_conversation(client_context)
        self.assertFalse(os.path.exists("./storage/conversations/testclient_user2.conv"))

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

    def test_remove_conversation_invalid_userid(self):
        config = BotConversationsConfiguration()
        mgr = ConversationManager(config)

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")

        client = TestClient()
        client.add_conversation_store("./storage/conversations")

        mgr.initialise(client.storage_factory)

        client_context = client.create_client_context("user1")
        self.assertEqual(len(mgr.conversations), 0)
        conversation = mgr.get_conversation(client_context)

        question1 = Question.create_from_text(client_context, "Hello There")
        question1.sentence(0).response = "Hi"
        conversation.record_dialog(question1)
        mgr.save_conversation(client_context)
        self.assertTrue(os.path.exists("./storage/conversations/testclient_user1.conv"))

        client_context._userid = "user2"
        mgr.remove_conversation(client_context)
        self.assertTrue(os.path.exists("./storage/conversations/testclient_user1.conv"))
        self.assertFalse(os.path.exists("./storage/conversations/testclient_user2.conv"))

        if os.path.exists("./storage/conversations"):
            shutil.rmtree("./storage/conversations")
