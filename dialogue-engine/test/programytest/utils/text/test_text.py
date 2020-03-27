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

from programy.utils.text.text import TextUtils


class TextUtilsTests(unittest.TestCase):

    def test_get_tabs(self):
        tabs = TextUtils.get_tabs(0)
        self.assertEqual(tabs, "")

        tabs = TextUtils.get_tabs(1, tabs="\t")
        self.assertEqual(tabs, "\t")

        tabs = TextUtils.get_tabs(5, tabs="\t")
        self.assertEqual(tabs, "\t\t\t\t\t")

    def test_strip_whitespace(self):
        self.assertEqual("", TextUtils.strip_whitespace(""))
        self.assertEqual("", TextUtils.strip_whitespace(" "))
        self.assertEqual("", TextUtils.strip_whitespace("\t"))
        self.assertEqual("", TextUtils.strip_whitespace("\n"))
        self.assertEqual("", TextUtils.strip_whitespace("\r"))
        self.assertEqual("", TextUtils.strip_whitespace("\r\t\n"))
        self.assertEqual("test", TextUtils.strip_whitespace("\r\t\ntest\r\t\n"))
        self.assertEqual("test test", TextUtils.strip_whitespace("\r\t\ntest test\r\t\n"))
        self.assertEqual("test test", TextUtils.strip_whitespace("\r\t\ntest\n\r\ttest\r\t\n"))

    def test_strip_all_whitespace(self):
        self.assertEqual("", TextUtils.strip_all_whitespace(""))
        self.assertEqual("", TextUtils.strip_all_whitespace(" "))
        self.assertEqual("", TextUtils.strip_all_whitespace("\t"))
        self.assertEqual("", TextUtils.strip_all_whitespace("\n"))
        self.assertEqual("", TextUtils.strip_all_whitespace("\r"))
        self.assertEqual("", TextUtils.strip_all_whitespace("\r\t\n"))
        self.assertEqual("test", TextUtils.strip_all_whitespace("\r\t\ntest\r\t\n"))
        self.assertEqual("testtest", TextUtils.strip_all_whitespace("\r\t\ntest test\r\t\n"))
        self.assertEqual("testtest", TextUtils.strip_all_whitespace("\r\t\ntest\n\r\ttest\r\t\n"))

    def test_strip_all_punctuation(self):
        self.assertEqual("", TextUtils.strip_all_punctuation(""))
        self.assertEqual("", TextUtils.strip_all_punctuation(" "))
        self.assertEqual("x y z", TextUtils.strip_all_punctuation("x! y? z."))
        self.assertEqual("a b c", TextUtils.strip_all_punctuation("!a b c?"))

    def test_urlify(self):
        self.assertEqual("", TextUtils.urlify(""))
        self.assertEqual("%20", TextUtils.urlify(" "))
        self.assertEqual("Hello%20World", TextUtils.urlify("Hello World"))

    def test_strip_html(self):
        self.assertEqual("", TextUtils.strip_html(""))
        self.assertEqual("", TextUtils.strip_html("<html></html>"))
        self.assertEqual("Hello World", TextUtils.strip_html("<html>Hello <b>World</b></html>"))

    def test_replace_path_seperator(self):
        self.assertEqual("", TextUtils.replace_path_seperator(""))
        self.assertEqual(" ", TextUtils.replace_path_seperator(" "))
        self.assertEqual(os.sep, TextUtils.replace_path_seperator("/"))
        self.assertEqual(".."+os.sep, TextUtils.replace_path_seperator("../"))
        self.assertEqual("\\", TextUtils.replace_path_seperator("/", "/", "\\"))

    def test_html_escape(self):
        self.assertEqual("", TextUtils.html_escape(""))
        self.assertEqual(" ", TextUtils.html_escape(" "))
        self.assertEqual("&lt;&gt;", TextUtils.html_escape("<>"))
        self.assertEqual("&lt;regex/&gt;", TextUtils.html_escape("<regex/>"))

    def test_tag_and_namespace_from_text(self):
        tag, name = TextUtils.tag_and_namespace_from_text("")
        self.assertIsNotNone(tag)
        self.assertEqual("", tag)
        self.assertIsNone(name)

        tag, name = TextUtils.tag_and_namespace_from_text("text")
        self.assertIsNotNone(tag)
        self.assertEqual("text", tag)
        self.assertIsNone(name)

        tag, name = TextUtils.tag_and_namespace_from_text("{http://alicebot.org/2001/AIML}aiml ")
        self.assertIsNotNone(tag)
        self.assertEqual("aiml", tag)
        self.assertIsNotNone(name)
        self.assertEqual("{http://alicebot.org/2001/AIML}", name)
