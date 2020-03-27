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


class UserStoreAsserts(unittest.TestCase):

    def assert_user_storage(self, store):

        store.empty()

        store.add_user('1', "console")
        store.add_user('1', "facebook")
        store.add_user('2', "console")
        store.add_user('3', "twitter")
        store.add_user('4', "facebook")
        store.add_user('5', "console")
        store.commit()

        self.assertTrue(store.exists('1', "console"))
        self.assertFalse(store.exists('2', "facebook"))

        links = store.get_links('1')
        self.assertEquals(['console', "facebook"], links)

        links = store.get_links('999')
        self.assertEquals([], links)

        store.remove_user('1', "console")
        self.assertFalse(store.exists('1', "console"))

        store.add_user('1', "console")
        self.assertTrue(store.exists('1', "console"))
        self.assertTrue(store.exists('1', "facebook"))

        store.remove_user_from_all_clients('1')
        self.assertFalse(store.exists('1', "console"))
        self.assertFalse(store.exists('1', "facebook"))
