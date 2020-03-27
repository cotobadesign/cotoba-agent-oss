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
import datetime


class LinkStoreAsserts(unittest.TestCase):

    def assert_links_storage(self, store):

        store.empty()

        store.create_link('user1', 'Password123', 'ABCDEF', expires=datetime.datetime.now())
        store.create_link('user2', 'Password123', 'ABCDEF', expires=datetime.datetime.now())

        self.assertTrue(store.link_exists('user1', 'Password123', 'ABCDEF'))
        self.assertFalse(store.link_exists('user99', 'Password123', 'ABCDEF'))

        link = store.get_link('user1')
        self.assertIsNotNone(link)
        self.assertEqual('user1', link.primary_user)
        self.assertEqual('Password123', link.provided_key)
        self.assertEqual('ABCDEF', link.generated_key)

        link = store.get_link('user2')
        self.assertIsNotNone(link)
        self.assertEqual('user2', link.primary_user)
        self.assertEqual('Password123', link.provided_key)
        self.assertEqual('ABCDEF', link.generated_key)

        store.remove_link('user1')
        store.commit()
        link = store.get_link('user1')
        self.assertIsNone(link)

        link = store.get_link('user2')
        self.assertIsNotNone(link)
        self.assertEqual('user2', link.primary_user)
        self.assertEqual('Password123', link.provided_key)
        self.assertEqual('ABCDEF', link.generated_key)

        link.expired = True
        store.update_link(link)
