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
from programy.processors.post.formatnumbers import FormatNumbersPostProcessor
from programy.context import ClientContext

from programytest.client import TestClient


class FormatNmbersTests(unittest.TestCase):

    def test_format_numbers(self):
        processor = FormatNumbersPostProcessor()

        context = ClientContext(TestClient(), "testid")

        result = processor.process(context, "23")
        self.assertIsNotNone(result)
        self.assertEqual("23", result)

        result = processor.process(context, "23.45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(context, "23. 45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(context, "23 . 45")
        self.assertIsNotNone(result)
        self.assertEqual("23.45", result)

        result = processor.process(context, "23,450")
        self.assertIsNotNone(result)
        self.assertEqual("23,450", result)

        result = processor.process(context, "23, 450")
        self.assertIsNotNone(result)
        self.assertEqual("23,450", result)

        result = processor.process(context, "23, 450, 000")
        self.assertIsNotNone(result)
        self.assertEqual("23,450,000", result)
