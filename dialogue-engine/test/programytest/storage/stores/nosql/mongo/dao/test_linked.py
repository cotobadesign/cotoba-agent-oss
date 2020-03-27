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

from programy.storage.stores.nosql.mongo.dao.linked import LinkedAccount


class LinkedAccountTests(unittest.TestCase):

    def test_init_no_id(self):
        linked = LinkedAccount(primary_userid='user1', linked_userid='user2')

        self.assertIsNotNone(linked)
        self.assertIsNone(linked.id)
        self.assertEqual('user1', linked.primary_userid)
        self.assertEqual('user2', linked.linked_userid)
        self.assertEqual({'linked_userid': 'user2', 'primary_userid': 'user1'}, linked.to_document())

    def test_init_with_id(self):
        linked = LinkedAccount(primary_userid='user1', linked_userid='user2')
        linked.id = '666'

        self.assertIsNotNone(linked)
        self.assertIsNotNone(linked.id)
        self.assertEqual('666', linked.id)
        self.assertEqual('user1', linked.primary_userid)
        self.assertEqual('user2', linked.linked_userid)
        self.assertEqual({'_id': '666', 'linked_userid': 'user2', 'primary_userid': 'user1'}, linked.to_document())

    def test_from_document(self):
        linked1 = LinkedAccount.from_document({'linked_userid': 'user2', 'primary_userid': 'user1'})
        self.assertIsNotNone(linked1)
        self.assertIsNone(linked1.id)
        self.assertEqual('user1', linked1.primary_userid)
        self.assertEqual('user2', linked1.linked_userid)

        linked2 = LinkedAccount.from_document({'_id': '666', 'linked_userid': 'user2', 'primary_userid': 'user1'})
        self.assertIsNotNone(linked2)
        self.assertIsNotNone(linked2.id)
        self.assertEqual('666', linked2.id)
        self.assertEqual('user1', linked2.primary_userid)
        self.assertEqual('user2', linked2.linked_userid)
