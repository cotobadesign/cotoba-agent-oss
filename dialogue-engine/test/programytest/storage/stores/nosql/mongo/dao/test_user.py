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

from programy.storage.stores.nosql.mongo.dao.user import User


class UserTests(unittest.TestCase):

    def test_init_no_id(self):
        user = User(userid='user1', client='client1')

        self.assertIsNotNone(user)
        self.assertIsNone(user.id)
        self.assertEqual('user1', user.userid)
        self.assertEqual('client1', user.client)
        self.assertEqual({'client': 'client1', 'userid': 'user1'}, user.to_document())

    def test_init_with_id(self):
        user = User(userid='user1', client='client1')
        user.id = '666'

        self.assertIsNotNone(user)
        self.assertIsNotNone(user.id)
        self.assertEqual('666', user.id)
        self.assertEqual('user1', user.userid)
        self.assertEqual('client1', user.client)
        self.assertEqual({'_id': '666', 'client': 'client1', 'userid': 'user1'}, user.to_document())

    def test_from_document(self):
        user1 = User.from_document({'client': 'client1', 'userid': 'user1'})
        self.assertIsNotNone(user1)
        self.assertIsNone(user1.id)
        self.assertEqual('user1', user1.userid)
        self.assertEqual('client1', user1.client)

        user2 = User.from_document({'_id': '666', 'client': 'client1', 'userid': 'user1'})
        self.assertIsNotNone(user2)
        self.assertIsNotNone(user2.id)
        self.assertEqual('666', user2.id)
        self.assertEqual('user1', user2.userid)
        self.assertEqual('client1', user2.client)
