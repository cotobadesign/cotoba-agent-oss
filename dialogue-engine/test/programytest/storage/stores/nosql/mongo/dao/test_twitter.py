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

from programy.storage.stores.nosql.mongo.dao.twitter import Twitter


class TwitterTests(unittest.TestCase):

    def test_init_no_id(self):
        twitter = Twitter(last_direct_message_id='1', last_status_id='2')

        self.assertIsNotNone(twitter)
        self.assertIsNone(twitter.id)
        self.assertEqual('1', twitter.last_direct_message_id)
        self.assertEqual('2', twitter.last_status_id)
        self.assertEqual({'last_direct_message_id': '1', 'last_status_id': '2'}, twitter.to_document())

    def test_init_with_id(self):
        twitter = Twitter(last_direct_message_id='1', last_status_id='2')
        twitter.id = '666'

        self.assertIsNotNone(twitter)
        self.assertIsNotNone(twitter.id)
        self.assertEqual('666', twitter.id)
        self.assertEqual('1', twitter.last_direct_message_id)
        self.assertEqual('2', twitter.last_status_id)
        self.assertEqual({'_id': '666', 'last_direct_message_id': '1', 'last_status_id': '2'}, twitter.to_document())

    def test_from_document(self):
        twitter1 = Twitter.from_document({'last_direct_message_id': '1', 'last_status_id': '2'})
        self.assertIsNone(twitter1.id)
        self.assertEqual('1', twitter1.last_direct_message_id)
        self.assertEqual('2', twitter1.last_status_id)

        twitter2 = Twitter.from_document({'_id': '666', 'last_direct_message_id': '1', 'last_status_id': '2'})
        self.assertIsNotNone(twitter2)
        self.assertIsNotNone(twitter2.id)
        self.assertEqual('666', twitter2.id)
        self.assertEqual('1', twitter2.last_direct_message_id)
        self.assertEqual('2', twitter2.last_status_id)
