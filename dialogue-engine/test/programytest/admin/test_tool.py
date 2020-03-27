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

from programy.admin.tool import AdminTool


class MockAdminTool(AdminTool):
    pass


class AdminToolTests(unittest.TestCase):

    text = ""

    @staticmethod
    def display(text):
        AdminToolTests.text += text

    def setUp(self):
        AdminToolTests.text = ""

    def test_unknown_primary_command(self):
        tool = AdminTool()
        tool.run(['unknown'], AdminToolTests.display)
        self.assertIsNotNone(AdminToolTests.text)
        self.assertTrue(AdminToolTests.text.startswith("Unknown primary command [unknown]"))

    def test_missing_bot_name(self):
        tool = AdminTool()
        tool.run(['download'], AdminToolTests.display)
        self.assertIsNotNone(AdminToolTests.text)
        self.assertTrue(AdminToolTests.text.startswith("Missing bot name from download command"))
