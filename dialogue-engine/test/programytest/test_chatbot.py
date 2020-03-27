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

from programy.chatbot import ProgramYChatbot

from programytest.clients.arguments import MockArgumentParser


class ChatBotTests(unittest.TestCase):

    def test_init(self):

        arguments = MockArgumentParser()
        chatbot = ProgramYChatbot(arguments)
        chatbot.add_local_properties()
        self.assertIsNotNone(chatbot)

        client_context = chatbot.create_client_context("console")
        self.assertIsNotNone(client_context)
        self.assertIsNotNone(client_context.brain)

        self.assertEqual(client_context.brain.properties.property("name"), "ProgramY")
        self.assertEqual(client_context.brain.properties.property("app_version"), "1.0.0")
        self.assertEqual(client_context.brain.properties.property("grammar_version"), "1.0.0")
        self.assertIsNotNone(client_context.brain.properties.property("birthdate"))
