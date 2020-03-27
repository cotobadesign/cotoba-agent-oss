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

from programytest.client import TestClient


class XMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(XMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])


class XMLAIMLTests(unittest.TestCase):

    def setUp(self):
        client = XMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_basic_xml(self):
        response = self._client_context.bot.ask_question(self._client_context, "HELLO")
        self.assertEqual(response, "I said <b>how are you</b> ?")

    def test_html_link(self):
        response = self._client_context.bot.ask_question(self._client_context, "PICTURE")
        self.assertEqual(response, 'You can see my picture at <a href="http://someurl/image.png">Here</a>.')

    def test_html_link_with_star(self):
        response = self._client_context.bot.ask_question(self._client_context, "GOOGLE AIML")
        self.assertEqual(response, '<a target="_new" href="http://www.google.com/search?q=AIML">Google Search</a>.')

    def test_html_br(self):
        response = self._client_context.bot.ask_question(self._client_context, "TEST1")
        self.assertEqual(response, 'Line1\n\t\t\tLine2.')

        response = self._client_context.bot.ask_question(self._client_context, "TEST2")
        self.assertEqual(response, 'Line1 <br></br> Line2.')

        response = self._client_context.bot.ask_question(self._client_context, "TEST3")
        self.assertEqual(response, '日本国.')

        response = self._client_context.bot.ask_question(self._client_context, "TEST4")
        self.assertEqual(response, '日本国<br></br>Line1\n\t\t\tLine2.')
