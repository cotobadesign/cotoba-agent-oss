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

from programy.storage.stores.sql.dao.lookup import Denormal
from programy.storage.stores.sql.dao.lookup import Normal
from programy.storage.stores.sql.dao.lookup import Gender
from programy.storage.stores.sql.dao.lookup import Person
from programy.storage.stores.sql.dao.lookup import Person2


class DenormalTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Denormal(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Denormal(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Denormal(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Denormal(id='1', key='key', value='value')>", str(lookup2))


class NormalTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Normal(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Normal(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Normal(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Normal(id='1', key='key', value='value')>", str(lookup2))


class GenderTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Gender(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Gender(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Gender(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Gender(id='1', key='key', value='value')>", str(lookup2))


class PersonTests(unittest.TestCase):

    def test_init(self):
        lookup1 = Person(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Person(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Person(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Person(id='1', key='key', value='value')>", str(lookup2))


class Person2Tests(unittest.TestCase):

    def test_init(self):
        lookup1 = Person2(key="key", value="value")
        self.assertIsNotNone(lookup1)
        self.assertEqual("<Person2(id='n/a', key='key', value='value')>", str(lookup1))

        lookup2 = Person2(id=1, key="key", value="value")
        self.assertIsNotNone(lookup2)
        self.assertEqual("<Person2(id='1', key='key', value='value')>", str(lookup2))
