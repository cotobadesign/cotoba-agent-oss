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

from programy.mappings.base import SingleStringCollection
from programy.mappings.base import DoubleStringCharSplitCollection
from programy.mappings.base import DoubleStringPatternSplitCollection


class MockSingleStringCollection(SingleStringCollection):

    def __init__(self, process_splits_success=False):
        SingleStringCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(MockSingleStringCollection, self).process_splits(splits, id)
        else:
            return False


class MockDoubleStringCharSplitCollection(DoubleStringCharSplitCollection):

    def __init__(self, process_splits_success=True):
        DoubleStringCharSplitCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(MockDoubleStringCharSplitCollection, self).process_splits(splits, id)
        else:
            return False


class MockDoubleStringPatternSplitCollection(DoubleStringPatternSplitCollection):

    def __init__(self, process_splits_success=True):
        DoubleStringPatternSplitCollection.__init__(self)
        self._process_splits_success = process_splits_success

    def process_splits(self, splits, id=None):
        if self._process_splits_success is True:
            return super(MockDoubleStringPatternSplitCollection, self).process_splits(splits, id)
        else:
            return False


class TestSingleStringCollection(unittest.TestCase):

    def test_single_strings_from_text(self):
        singles = SingleStringCollection()
        self.assertIsNotNone(singles)

        count = singles.load_from_text("""
        val1
        val2
        val3
        """)
        self.assertEqual(count, 3)
        self.assertIsNotNone(singles.strings)
        self.assertEqual(3, len(singles.strings))
        self.assertIn("val1", singles.strings)
        self.assertIn("val2", singles.strings)
        self.assertIn("val3", singles.strings)


class TestDoubleStringCharSplitCollection(unittest.TestCase):

    def test_double_strings_from_text(self):
        doubles = DoubleStringCharSplitCollection()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        key1,val1
        key2,val2
        key3,val3,val4
        """)
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_keyVal("key1"))
        self.assertEqual(doubles.value("key1"), "val1")

        self.assertTrue(doubles.has_keyVal("key2"))
        self.assertEqual(doubles.value("key2"), "val2")

        self.assertTrue(doubles.has_keyVal("key3"))
        self.assertEqual(doubles.value("key3"), "val3,val4")

        self.assertFalse(doubles.has_keyVal("key4"))
        doubles.add_value("key4", "val5")
        self.assertTrue(doubles.has_keyVal("key4"))
        self.assertEqual(doubles.value("key4"), "val5")
        doubles.set_value("key4", "val6")
        self.assertEqual(doubles.value("key4"), "val6")


class TestDoubleStringPatternSplitCollection(unittest.TestCase):

    def test_double_strings_from_text(self):
        doubles = DoubleStringPatternSplitCollection()
        self.assertIsNotNone(doubles)

        count = doubles.load_from_text("""
        "key1","val1"
        "key2","val2"
        "key3","val3,val4"
        """)
        self.assertEqual(count, 3)

        self.assertTrue(doubles.has_keyVal("key1"))

        self.assertTrue(doubles.has_keyVal("key2"))

        self.assertTrue(doubles.has_keyVal("key3"))

        self.assertFalse(doubles.has_keyVal("key4"))
