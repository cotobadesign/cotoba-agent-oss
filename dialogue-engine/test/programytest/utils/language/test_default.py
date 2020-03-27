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

from programy.utils.language.default import DefaultLangauge


class DefaultTests(unittest.TestCase):

    def test_split_into_sentences(self):
        sentences = DefaultLangauge.split_into_sentences("")
        self.assertEqual([], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello")
        self.assertEqual(["Hello"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello World")
        self.assertEqual(["Hello World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello, World")
        self.assertEqual(["Hello, World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello, World!")
        self.assertEqual(["Hello, World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello. World")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello? World")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("Hello. World.?!")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("!Hello. World")
        self.assertEqual(["Hello", "World"], sentences)

        sentences = DefaultLangauge.split_into_sentences("半宽韩文字母")
        self.assertEqual(["半宽韩文字母"], sentences)

        sentences = DefaultLangauge.split_into_sentences("半宽韩文字母. 半宽平假名")
        self.assertEqual(["半宽韩文字母", "半宽平假名"], sentences)

    def test_split_into_words(self):
        words = DefaultLangauge.split_into_words("")
        self.assertEqual([], words)

        words = DefaultLangauge.split_into_words("Hello")
        self.assertEqual(["Hello"], words)

        words = DefaultLangauge.split_into_words("Hello World")
        self.assertEqual(["Hello", "World"], words)

        words = DefaultLangauge.split_into_words("  Hello    World   ")
        self.assertEqual(["Hello", "World"], words)
