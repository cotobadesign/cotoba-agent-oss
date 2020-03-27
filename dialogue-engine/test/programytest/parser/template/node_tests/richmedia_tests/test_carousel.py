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

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.richmedia.carousel import TemplateCarouselNode
from programy.parser.template.nodes.richmedia.card import TemplateCardNode
from programy.parser.template.nodes.richmedia.button import TemplateButtonNode
from programy.parser.template.nodes.word import TemplateWordNode

from programytest.parser.base import ParserTestsBaseClass


class TemplateCarouselNodeTests(ParserTestsBaseClass):

    def test_carousel_node(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        carousel = TemplateCarouselNode()

        card = TemplateCardNode()
        card._image = TemplateWordNode("http://Servusai.com")
        card._title = TemplateWordNode("Servusai.com")
        card._subtitle = TemplateWordNode("The home of ProgramY")

        button = TemplateButtonNode()
        button._text = TemplateWordNode("More...")
        button._url = TemplateWordNode("http://Servusai.com/aiml")
        card._buttons.append(button)

        carousel._cards.append(card)

        root.append(carousel)

        resolved = root.resolve(self._client_context)

        self.assertIsNotNone(resolved)
        texts1 = "<carousel><card><image>http://Servusai.com</image><title>Servusai.com</title><subtitle>The home of ProgramY</subtitle>" + \
            "<button><text>More...</text><url>http://Servusai.com/aiml</url></button></card></carousel>"
        self.assertEqual(texts1, resolved)

        texts2 = "<carousel><card><image>http://Servusai.com</image><title>Servusai.com</title><subtitle>The home of ProgramY</subtitle>" + \
            "<button><text>More...</text><url>http://Servusai.com/aiml</url></button></card></carousel>"
        self.assertEqual(texts2, root.to_xml(self._client_context))
