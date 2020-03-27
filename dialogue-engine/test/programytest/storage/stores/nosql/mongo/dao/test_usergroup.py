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

from programy.storage.stores.nosql.mongo.dao.usergroups import UserGroups


class UserGroupsTests(unittest.TestCase):

    def test_init_no_id(self):
        usergroups = UserGroups(usergroups={})

        self.assertIsNotNone(usergroups)
        self.assertIsNone(usergroups.id)
        self.assertEqual({'usergroups': {}}, usergroups.to_document())

    def test_init_with_id(self):
        usergroups = UserGroups(usergroups={})
        usergroups.id = '666'

        self.assertIsNotNone(usergroups)
        self.assertEqual('666', usergroups.id)
        self.assertEqual({'_id': '666', 'usergroups': {}}, usergroups.to_document())

    def test_from_document(self):
        usergroups1 = UserGroups.from_document({'usergroups': {}})
        self.assertIsNotNone(usergroups1)
        self.assertIsNone(usergroups1.id)
        self.assertEqual({}, usergroups1.usergroups)

        usergroups2 = UserGroups.from_document({'_id': '666', 'usergroups': {}})
        self.assertIsNotNone(usergroups2)
        self.assertEqual('666', usergroups2.id)
        self.assertEqual({}, usergroups2.usergroups)
