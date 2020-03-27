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

from programy.utils.logging.ylogger import YLogger
import datetime
from dateutil.relativedelta import relativedelta
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.utils.text.text import TextUtils
from programy.parser.exceptions import ParserException


class TemplateIntervalNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._interval_format = None
        self._style = None
        self._interval_from = None
        self._interval_to = None

    @property
    def interval_format(self):
        return self._interval_format

    @interval_format.setter
    def interval_format(self, interval_format):
        self._interval_format = interval_format

    @property
    def interval_from(self):
        return self._interval_from

    @interval_from.setter
    def interval_from(self, interval_from):
        self._interval_from = interval_from

    @property
    def interval_to(self):
        return self._interval_to

    @interval_to.setter
    def interval_to(self, interval_to):
        self._interval_to = interval_to

    @property
    def style(self):
        return self._style

    @style.setter
    def style(self, style):
        self._style = style

    def resolve_to_string(self, client_context):
        format_str = self._interval_format.resolve(client_context)

        from_str = self.interval_from.resolve(client_context)
        from_time = datetime.datetime.strptime(from_str, format_str)

        to_str = self.interval_to.resolve(client_context)
        to_time = datetime.datetime.strptime(to_str, format_str)

        style = self._style.resolve(client_context)

        # diff = to_time - from_time
        difference = relativedelta(to_time, from_time)

        if style == "years":
            resolved = str(difference.years)
        elif style == "months":
            resolved = str(difference.months)
        elif style == "weeks":
            resolved = str(difference.weeks)
        elif style == "days":
            resolved = str(difference.days)
        elif style == "hours":
            resolved = str(difference.hours)
        elif style == "minutes":
            resolved = str(difference.minutes)
        elif style == "seconds":
            resolved = str(difference.seconds)
        elif style == "microseconds":
            resolved = str(difference.microseconds)
        elif style == "ymd":
            resolved = "%d years, %d months, %d days" % \
                       (difference.years, difference.months, difference.days)
        elif style == "hms":
            resolved = "%d hours, %d minutes, %d seconds" % \
                       (difference.hours, difference.minutes, difference.seconds)
        elif style == "ymdhms":
            resolved = "%d years, %d months, %d days, %d hours, %d minutes, %d seconds" % \
                       (difference.years, difference.months, difference.days,
                        difference.hours, difference.minutes, difference.seconds)
        else:
            YLogger.debug(client_context, "Unknown interval style [%s]", style)
            resolved = ""

        YLogger.debug(client_context, "[INTERVAL] resolved to [%s]", resolved)
        return resolved

    def to_string(self):
        return "[INTERVAL]"

    def to_xml(self, client_context):
        xml = '<interval'
        xml += ' format="%s"' % self._interval_format.to_xml(client_context)
        xml += ' style="%s"' % self._style.to_xml(client_context)
        xml += '>'
        xml += '<from>'
        xml += self._interval_from.to_xml(client_context)
        xml += '</from>'
        xml += '<to>'
        xml += self._interval_to.to_xml(client_context)
        xml += '</to>'
        xml += '</interval>'
        return xml

    #######################################################################################################
    # INTERVAL_EXPRESSION ::== <interval>
    # 							(DATE_ATTRIBUTE_TAGS)
    # 							<style>(TEMPLATE_EXPRESSION)</style>
    # 							<from>(TEMPLATE_EXPRESSION)</from>
    # 							<to>(TEMPLATE_EXPRESSION)</to>
    # 						</interval>

    def parse_expression(self, graph, expression):

        if 'format' in expression.attrib:
            self.interval_format = self.parse_attrib_value_as_word_node(graph, expression, 'format')

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'format':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self.interval_format = node

            elif tag_name == 'style':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self.style = node

            elif tag_name == 'from':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self.interval_from = node

            elif tag_name == 'to':
                node = graph.get_base_node()
                node.parse_text(graph, self.get_text_from_element(child))
                for sub_child in child:
                    graph.parse_tag_expression(sub_child, node)
                    node.parse_text(graph, self.get_text_from_element(child))
                self.interval_to = node
            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if self.interval_format is None or len(self.interval_format.children) == 0:
            YLogger.warning(self, "Interval node, format missing, defaulting to '%c'")
            self.interval_format = graph.get_word_node('%c')

        if self.style is None or len(self.style.children) == 0:
            raise ParserException("interval_style node missing", xml_element=expression, nodename='interval')
        elif len(self.style.children) == 1 and type(self.style.children[0]) is TemplateWordNode:
            style = self.style.children[0].word
            if style not in ["years", "months", "weeks", "days", "hours", "minutes", "seconds", "microseconds", "ymd", "hms", "ymdhms"]:
                raise ParserException(("invalid interval stile [%s]" % style), xml_element=expression, nodename='interval')

        if self.interval_from is None or len(self.interval_from.children) == 0:
            raise ParserException("interval_from node missing", xml_element=expression, nodename='interval')
        if self.interval_to is None or len(self.interval_to.children) == 0:
            raise ParserException("interval_to node missing", xml_element=expression, nodename='interval')
