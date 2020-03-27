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

from programy.config.bot.redisstorage import BotConversationsRedisStorageConfiguration
from programy.dialog.storage.redis import ConversationRedisStorage
from programytest.client import TestClient
from programy.dialog.dialog import Conversation


class ConversationRedisStorageTests(unittest.TestCase):

    def test_persistence(self):

        storage_config = BotConversationsRedisStorageConfiguration("redis")
        redis = ConversationRedisStorage(storage_config)
        self.assertIsNotNone(redis)

        client = TestClient()
        client_context = client.create_client_context("testid")
        conversation1 = Conversation(client_context)
        conversation1.set_property("topic", "topic1")

        redis.save_conversation(conversation1, client_context.userid)

        conversation2 = Conversation(client_context)
        redis.load_conversation(conversation2, client_context.userid)
        self.assertIsNotNone(conversation2)
        self.assertIsNotNone(conversation2.properties)

        self.assertEqual(conversation1.properties, conversation2.properties)

