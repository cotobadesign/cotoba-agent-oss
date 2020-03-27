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

from programy.storage.stores.sql.dao.usergroup import AuthoriseUser
from programy.storage.stores.sql.dao.usergroup import UserRole
from programy.storage.stores.sql.dao.usergroup import UserGroup
from programy.storage.stores.sql.dao.usergroup import AuthoriseGroup
from programy.storage.stores.sql.dao.usergroup import GroupGroup
from programy.storage.stores.sql.dao.usergroup import GroupRole
from programy.storage.stores.sql.dao.usergroup import GroupUser


class AuthoriseUserTests(unittest.TestCase):

    def test_init(self):
        authuser1 = AuthoriseUser(name='user1')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<AuthoriseUser(id='n/a', name='user1')>", str(authuser1))

        authuser2 = AuthoriseUser(id=1, name='user1')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<AuthoriseUser(id='1', name='user1')>", str(authuser2))


class UserRoleTests(unittest.TestCase):

    def test_init(self):
        authuser1 = UserRole(user='user1', role='admin')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<UserRole(id='n/a', user='user1', role='admin')>", str(authuser1))

        authuser2 = UserRole(id=1, user='user1', role='admin')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<UserRole(id='1', user='user1', role='admin')>", str(authuser2))


class UserGroupTests(unittest.TestCase):

    def test_init(self):
        authuser1 = UserGroup(user='user1', group='admin')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<UserGroup(id='n/a', user='user1', group='admin')>", str(authuser1))

        authuser2 = UserGroup(id=1, user='user1', group='admin')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<UserGroup(id='1', user='user1', group='admin')>", str(authuser2))


class AuthoriseGroupTests(unittest.TestCase):

    def test_init(self):
        authuser1 = AuthoriseGroup(name='group1', parent='group0')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<AuthoriseGroup(id='n/a', name='group1', parent='group0')>", str(authuser1))

        authuser2 = AuthoriseGroup(id=1, name='group1', parent='group0')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<AuthoriseGroup(id='1', name='group1', parent='group0')>", str(authuser2))


class GroupGroupTests(unittest.TestCase):

    def test_init(self):
        authuser1 = GroupGroup(group='group1', subgroup='group2')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<GroupGroup(id='n/a', group='group1', subgroup='group2')>", str(authuser1))

        authuser2 = GroupGroup(id=1, group='group1', subgroup='group2')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<GroupGroup(id='1', group='group1', subgroup='group2')>", str(authuser2))


class GroupRoleTests(unittest.TestCase):

    def test_init(self):
        authuser1 = GroupRole(group='group1', role='admin')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<GroupRole(id='n/a', group='group1', role='admin')>", str(authuser1))

        authuser2 = GroupRole(id=1, group='group1', role='admin')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<GroupRole(id='1', group='group1', role='admin')>", str(authuser2))


class GroupUserTests(unittest.TestCase):

    def test_init(self):
        authuser1 = GroupUser(group='group1', user='user1')
        self.assertIsNotNone(authuser1)
        self.assertEqual("<GroupUser(id='n/a', group='group1', user='user1')>", str(authuser1))

        authuser2 = GroupUser(id=1, group='group1', user='user1')
        self.assertIsNotNone(authuser2)
        self.assertEqual("<GroupUser(id='1', group='group1', user='user1')>", str(authuser2))
