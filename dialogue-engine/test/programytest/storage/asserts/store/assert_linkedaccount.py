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


class LinkedAccountStoreAsserts(unittest.TestCase):

    def assert_linkedaccounts_storage(self, store):

        store.empty()

        store.link_accounts("user1", "user2")
        store.link_accounts("user1", "user3")
        store.commit()

        accounts = store.linked_accounts("user1")
        self.assertIsNotNone(accounts)
        self.assertEqual(2, len(accounts))
        self.assertTrue("user2" in accounts)
        self.assertTrue("user3" in accounts)

        accounts = store.primary_account("user2")
        self.assertIsNotNone(accounts)
        self.assertTrue("user1" in accounts)

        accounts = store.primary_account("user3")
        self.assertIsNotNone(accounts)
        self.assertTrue("user1" in accounts)

        store.unlink_accounts("user1")
        store.commit()
        accounts = store.linked_accounts("user1")
        self.assertIsNotNone(accounts)
        self.assertEqual(0, len(accounts))
