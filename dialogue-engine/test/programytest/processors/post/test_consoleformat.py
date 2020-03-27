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

from programy.processors.post.consoleformat import ConsoleFormatPostProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class RemoveHTMLTests(unittest.TestCase):

    def test_format_console(self):
        processor = ConsoleFormatPostProcessor()

        context = ClientContext(TestClient(), "testid")
        result = processor.process(context, "Hello World")
        self.assertIsNotNone(result)
        self.assertEqual("Hello World", result)

        texts = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio est virtus; Sed quid attinet de rebus tam apertis plura requirere?"
        result = processor.process(context, texts)
        self.assertIsNotNone(result)
        if os.name == 'posix':
            self.assertEqual(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio\nest virtus; Sed quid attinet de rebus tam apertis plura requirere?",
                result)
        elif os.name == 'nt':
            self.assertEqual(
                "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Rationis enim perfectio\r\nest virtus; Sed quid attinet de rebus tam apertis plura requirere?",
                result)
        else:
            raise Exception("Unknown os [%s]" % os.name)
