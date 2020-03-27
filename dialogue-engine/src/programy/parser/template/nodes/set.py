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

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
from programy.parser.template.nodes.get import TemplateGetNode


class TemplateSetNode(TemplateNode):
    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._property_type = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def property_type(self):
        return self._property_type

    @property_type.setter
    def property_type(self, property_type):
        self._property_type = property_type

    def resolve_children(self, client_context):
        if self._children:
            return self.resolve_children_to_string(client_context)
        return ""

    def resolve_to_string(self, client_context):

        conversation = client_context.bot.get_conversation(client_context)
        name = self.name.resolve(client_context)
        value = self.resolve_children(client_context)

        if self.property_type == 'var':
            YLogger.debug(client_context, "[%s] resolved to var: [%s] => [%s]", self.to_string(), name, value)
            conversation.current_question().set_property(name, value)
        elif self.property_type == 'data':
            YLogger.debug(client_context, "[%s] resolved to data: [%s] => [%s]", self.to_string(), name, value)
            conversation.set_data_property(name, value)
        elif self.property_type == 'name':
            YLogger.debug(client_context, "[%s] resolved to name: [%s] => [%s]", self.to_string(), name, value)
            value = conversation.set_property(name, value)

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), value)

        if value == '':
            value = TemplateGetNode.get_default_value(client_context)
        return value

    def to_string(self):
        return "[SET [%s] - %s]" % (self.property_type, self.name.to_string())

    def to_xml(self, client_context):
        xml = "<set"
        xml += ' %s="%s"' % (self.property_type, self.name.resolve(client_context))
        xml += ">"
        xml += self.children_to_xml(client_context)
        xml += "</set>"
        return xml

    # ######################################################################################################
    # SET_PREDICATE_EXPRESSION ::==
    # <set name="WORD">TEMPLATE_EXPRESSION</set> |
    # <set><name>TEMPLATE_EXPRESSION</name>TEMPLATE_EXPRESSION</set> |
    # <set var="WORD">TEMPLATE_EXPRESSION</set> |
    # <set><var>TEMPLATE_EXPRESSION</var>TEMPLATE_EXPRESSION</set>

    def parse_expression(self, graph, expression):
        mode_count = 0

        if 'name' in expression.attrib:
            mode_count += 1
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'name')
            self.property_type = 'name'

        if 'data' in expression.attrib:
            mode_count += 1
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'data')
            self.property_type = 'data'

        if 'var' in expression.attrib:
            mode_count += 1
            self.name = self.parse_attrib_value_as_word_node(graph, expression, 'var')
            self.property_type = 'var'

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'name':
                mode_count += 1
                self.name = self.parse_children_as_word_node(graph, child)
                self.property_type = 'name'

            elif tag_name == 'data':
                mode_count += 1
                self.name = self.parse_children_as_word_node(graph, child)
                self.property_type = 'data'

            elif tag_name == 'var':
                mode_count += 1
                self.name = self.parse_children_as_word_node(graph, child)
                self.property_type = 'var'

            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if mode_count == 0:
            raise ParserException("Missing variable type", xml_element=expression, nodename='set')
        elif mode_count > 1:
            raise ParserException("Node has mulitple variable types", xml_element=expression, nodename='set')
