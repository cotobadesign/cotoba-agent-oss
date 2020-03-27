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

from programy.utils.language.chinese import ChineseLanguage


class ChineseTests(unittest.TestCase):

    def test_is_language(self):
        self.assertFalse(ChineseLanguage.is_language(""))
        self.assertFalse(ChineseLanguage.is_language("H"))
        self.assertTrue(ChineseLanguage.is_language("你"))

    def test_split_langauge(self):
        self.assertEqual([], ChineseLanguage.split_language(""))
        self.assertEqual(['X'], ChineseLanguage.split_language("X"))
        self.assertEqual(['你'], ChineseLanguage.split_language("你"))
        self.assertEqual(['你', '好'], ChineseLanguage.split_language("你好"))
        self.assertEqual(['X', '你', '好'], ChineseLanguage.split_language("X你好"))
        self.assertEqual(['X', '你', '好', 'Y'], ChineseLanguage.split_language("X你好Y"))

    def test_split_unicode(self):
        self.assertEqual([], ChineseLanguage.split_unicode(""))
        self.assertEqual(['X'], ChineseLanguage.split_unicode("X"))
        self.assertEqual(['你'], ChineseLanguage.split_unicode("你"))
        self.assertEqual(['你', '好'], ChineseLanguage.split_unicode("你好"))
        self.assertEqual(['X', '你', '好'], ChineseLanguage.split_unicode("X你好"))
        self.assertEqual(['X', '你', '好', 'Y'], ChineseLanguage.split_unicode("X你好Y"))

    def test_split_with_spaces(self):
        self.assertEqual('', ChineseLanguage.split_with_spaces([]))
        self.assertEqual('X', ChineseLanguage.split_with_spaces(['X']))
        self.assertEqual('你', ChineseLanguage.split_with_spaces(['你']))
        self.assertEqual('你  好', ChineseLanguage.split_with_spaces(['你', '好']))
        self.assertEqual('X  你  好', ChineseLanguage.split_with_spaces(['X', '你', '好']))
        self.assertEqual('X  你  好  Y', ChineseLanguage.split_with_spaces(['X', '你', '好', 'Y']))
