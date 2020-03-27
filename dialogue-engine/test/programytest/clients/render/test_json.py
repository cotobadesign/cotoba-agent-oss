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
import unittest.mock

from programy.clients.render.json import JSONRenderer


class MockConsoleBotClient(object):

    def __init__(self):
        self._response = None

    def process_response(self, client_context, response):
        self._response = response
        return response


class JSONRendererTests(unittest.TestCase):

    def test_text_only(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "Hello world")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'text': 'Hello world', 'type': 'text'}, mock_console._response)

    def test_url_button(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><url>http://click.me</url></button>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'postback': None, 'text': 'Hello', 'type': 'button', 'url': 'http://click.me'}, mock_console._response)

    def test_postback_button(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<button><text>Hello</text><postback>HELLO</postback></button>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'postback': 'HELLO', 'text': 'Hello', 'type': 'button', 'url': None}, mock_console._response)

    def test_link(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<link><text>Hello</text><url>http://click.me</url></link>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'text': 'Hello', 'type': 'link', 'url': 'http://click.me'}, mock_console._response)

    def test_image(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<image>http://servusai.com/aiml.png</image>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'type': 'image', 'url': 'http://servusai.com/aiml.png'}, mock_console._response)

    def test_video(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<video>http://servusai.com/aiml.mov</video>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'type': 'video', 'url': 'http://servusai.com/aiml.mov'}, mock_console._response)

    def test_card(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        texts = '<card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle>' + \
            '<button><text>Hello</text><url>http://click.me</url></button></card>'
        renderer.render("testuser", texts)

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'buttons': [{'postback': None, 'text': 'Hello', 'type': 'button', 'url': 'http://click.me'}],
                         'image': 'http://servusai.com/aiml.png', 'subtitle': 'Home of ProgramY', 'title': 'Servusai', 'type': 'card'},
                         mock_console._response)

    def test_carousel(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        texts = '<carousel><card><image>http://servusai.com/aiml.png</image><title>Servusai</title><subtitle>Home of ProgramY</subtitle>' + \
            '<button><text>Hello</text><url>http://click.me</url></button></card></carousel>'
        renderer.render("testuser", texts)

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'cards': [{'buttons': [{'postback': None, 'text': 'Hello', 'type': 'button', 'url': 'http://click.me'}],
                         'image': 'http://servusai.com/aiml.png', 'subtitle': 'Home of ProgramY', 'title': 'Servusai', 'type': 'card'}], 'type': 'carousel'},
                         mock_console._response)

    def test_reply_with_postback(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text><postback>HELLO</postback></reply>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'postback': 'HELLO', 'text': 'Hello', 'type': 'reply'}, mock_console._response)

    def test_reply_without_postback(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<reply><text>Hello</text></reply>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'postback': None, 'text': 'Hello', 'type': 'reply'}, mock_console._response)

    def test_delay(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<delay><seconds>0</seconds></delay>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'seconds': '0', 'type': 'delay'}, mock_console._response)

    def test_split(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<split />")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'type': 'split'}, mock_console._response)

    def test_list(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<list><item>Item1</item><item>Item2</item></list>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'items': [{'text': 'Item1', 'type': 'text'}, {'text': 'Item2', 'type': 'text'}], 'type': 'list'}, mock_console._response)

    def test_olist(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<olist><item>Item1</item><item>Item2</item></olist>")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'items': [{'text': 'Item1', 'type': 'text'}, {'text': 'Item2', 'type': 'text'}], 'type': 'list'}, mock_console._response)

    def test_location(self):
        mock_console = MockConsoleBotClient()
        renderer = JSONRenderer(mock_console)
        self.assertIsNotNone(renderer)

        renderer.render("testuser", "<location />")

        self.assertIsNotNone(mock_console._response)
        self.assertEqual({'type': 'location'}, mock_console._response)
