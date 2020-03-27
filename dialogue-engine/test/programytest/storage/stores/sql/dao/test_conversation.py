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

from programy.storage.stores.sql.dao.conversation import Conversation


class ConversationTests(unittest.TestCase):

    def test_init(self):

        conversation1 = Conversation(clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response')
        self.assertIsNotNone(conversation1)
        texts1 = "<Conversation(id='n/a', clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response'>"
        self.assertEqual(texts1, str(conversation1))

        conversation2 = Conversation(id=1, clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response')
        self.assertIsNotNone(conversation2)
        texts2 = "<Conversation(id='1', clientid='clientid', userid='userid', botid='botid', brainid='brainid', question='question', sentence='sentence', response='response'>"
        self.assertEqual(texts2, str(conversation2))
