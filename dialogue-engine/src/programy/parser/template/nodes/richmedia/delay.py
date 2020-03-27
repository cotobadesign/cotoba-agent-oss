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
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.parser.template.nodes.base import TemplateNode
from programy.utils.text.text import TextUtils
from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.word import TemplateWordNode


class TemplateDelayNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._seconds = None

    def resolve_to_string(self, client_context):
        resolved = self._seconds.resolve(client_context)
        try:
            seconds = int(resolved)
            if seconds < 0:
                seconds = 0
        except Exception:
            seconds = 0

        str = "<delay>"
        str += "<seconds>%d</seconds>" % seconds
        str += "</delay>"
        return str

    def to_string(self):
        return "[DELAY %d]" % (len(self._children))

    def to_xml(self, client_context):
        return self.resolve_to_string(client_context)

    #######################################################################################################
    #

    def parse_expression(self, graph, expression):
        text_seconds = '0'
        if 'seconds' in expression.attrib:
            self._seconds = graph.get_word_node(expression.attrib['seconds'])
            text_seconds = self._seconds.word

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'seconds':
                self._seconds = self.parse_children_as_word_node(graph, child)
                if len(self._seconds.children) == 1 and type(self._seconds.children[0]) is TemplateWordNode:
                    text_seconds = self._seconds.children[0].word

            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self._seconds is None:
            raise ParserException("Missing seconds element", xml_element=expression, nodename='delay')

        if text_seconds != '0':
            try:
                seconds = int(text_seconds)
                if seconds < 0:
                    raise Exception()
            except Exception:
                raise ParserException("Seconds element is not valid integer", xml_element=expression, nodename='delay')
