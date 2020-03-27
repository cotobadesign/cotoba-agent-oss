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
import os

from programy.utils.substitutions.substitues import Substitutions


class SubstitutionsTests(unittest.TestCase):

    def test_basics(self):

        sub = Substitutions()

        sub.add_substitute("$FIRSTNAME", "Fred")
        sub.add_substitute("$SURNAME", "West")
        sub.add_substitute("$WIFE", "Mary")

        self.assertTrue(sub.has_substitute("$FIRSTNAME"))
        self.assertFalse(sub.has_substitute("$FRED"))

        self.assertEquals("Fred", sub.get_substitute("$FIRSTNAME"))
        self.assertEquals("West", sub.get_substitute("$SURNAME"))
        self.assertEquals("Mary", sub.get_substitute("$WIFE"))

        with self.assertRaises(ValueError):
            sub.get_substitute("$NUMBER")

        sub.empty()

        self.assertFalse(sub.has_substitute("$FIRSTNAME"))
        self.assertFalse(sub.has_substitute("$SURNAME"))
        self.assertFalse(sub.has_substitute("$WIFE"))

    def test_load(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "subs.txt")

        self.assertEquals("Fred", sub.get_substitute("$FIRSTNAME"))
        self.assertEquals("West", sub.get_substitute("$SURNAME"))
        self.assertEquals("Mary", sub.get_substitute("$WIFE"))

        with self.assertRaises(ValueError):
            sub.get_substitute("$NUMBER")

    def test_substitutions(self):

        sub = Substitutions()

        sub.load_substitutions(os.path.dirname(__file__) + os.sep + "subs.txt")

        self.assertEquals("My name is Fred West", sub.replace("My name is $FIRSTNAME $SURNAME"))
        self.assertEquals("My name is FredWest", sub.replace("My name is $FIRSTNAME$SURNAME"))
