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
import json

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils


class TemplateGetNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._property_type = ''
        self._tuples = None

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

    @property
    def tuples(self):
        return self._tuples

    @tuples.setter
    def tuples(self, tuples):
        self._tuples = tuples

    @staticmethod
    def get_default_value(client_context):
        value = client_context.bot.brain.properties.property("default-get")
        if value is None:
            YLogger.debug(None, "No property defined for default-get, checking defaults")

            value = client_context.bot.brain.configuration.defaults.default_get
            if value is None:
                YLogger.debug(None, "No value defined for default default-get, returning 'unknown'")
                value = "unknown"

        return value

    @staticmethod
    def get_property_value(client_context, property_type, name):

        conversation = client_context.bot.get_conversation(client_context)

        value = None
        if property_type == 'var':
            if conversation.has_current_question():
                value = conversation.current_question().property(name)
        elif property_type == 'data':
            value = conversation.data_property(name)
        elif property_type == 'name':
            if name is not None and client_context.brain.dynamics.is_dynamic_var(name) is True:
                value = client_context.brain.dynamics.dynamic_var(client_context, name)
            else:
                value = conversation.property(name)

        if value is None:
            YLogger.debug(client_context, "No property for [%s]", name)

            value = TemplateGetNode.get_default_value(client_context)

        return value

    def resolve_variable(self, client_context):
        name = self.name.resolve(client_context)
        value = TemplateGetNode.get_property_value(client_context, self.property_type, name)
        YLogger.debug(client_context, "[%s] resolved to %s: [%s] <= [%s]", self.to_string(), self.property_type, name, value)
        return value

    def decode_tuples(self, tuples):
        if isinstance(tuples, str):
            return json.loads(tuples)
        else:
            return tuples

    def resolve_tuple(self, client_context):
        if self._name is None:
            variables = None
        else:
            variables = self._name.resolve(client_context).split(" ")

        raw_tuples = self._tuples.resolve(client_context)
        try:
            tuples = self.decode_tuples(raw_tuples)
        except Exception:
            tuples = []

        resolved = ""
        if tuples:

            if isinstance(tuples, list):  # Is tuples an array of results in the form [[[subj, val],[pred, val],[obj, val]], [[subj, val],[pred, val],[obj, val]]...]

                if variables:  # If we are asking for variables, pull out the vars
                    for atuple in tuples:
                        if isinstance(atuple[0], list) is True:
                            for pair in atuple:
                                for var in variables:
                                    if pair[0] == var:
                                        resolved += pair[1]
                                        resolved += " "
                        else:
                            for var in variables:
                                if atuple[0] == var:
                                    resolved += atuple[1]
                                    resolved += " "

                else:
                    for atuple in tuples:
                        resolved += atuple[0][1]
                        resolved += " "
                        resolved += atuple[1][1]
                        resolved += " "
                        resolved += atuple[2][1]
                        resolved += " "

        if resolved == "":
            YLogger.debug(client_context, "No tuples for [%s]", self._tuples)
            resolved = TemplateGetNode.get_default_value(client_context)
        else:
            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        return resolved

    def resolve_to_string(self, client_context):
        if self._tuples is None:
            value = self.resolve_variable(client_context)
        else:
            value = self.resolve_tuple(client_context)
        return value

    def to_string(self):
        if self.tuples is None:
            if self.name is None:
                name = "None"
            else:
                name = self.name.to_string()
            return "[GET [%s] - %s]" % (self.property_type, name)
        else:
            if self.name is None:
                return "[GET [Tuples] - (None)]"
            else:
                return "[GET [Tuples] - (%s)]" % self.name.to_string()

    def to_xml(self, client_context):
        if self.tuples is None:
            xml = "<get"
            xml += ' %s="%s"' % (self.property_type, self.name.resolve(client_context))
            xml += " />"
        else:
            xml = "<get"
            xml += ' tuples="%s"' % self.name.resolve(client_context)
            xml += " >"
            xml += self.tuples.to_xml(client_context)
            xml += "</get>"
        return xml

    # ######################################################################################################
    # GET_PREDICATE_EXPRESSION ::==
    # <get name="WORD"/> |
    # <get><name>TEMPLATE_EXPRESSION</name></get> |
    # <get var=”WORD”> |
    # <get><var>WORD</var></get>

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

            elif tag_name == "tuple":
                if mode_count == 0:
                    mode_count += 1
                self._tuples = self.parse_children_as_word_node(graph, child)

        if mode_count == 0:
            raise ParserException("Missing variable type", xml_element=expression, nodename='get')
        elif mode_count > 1:
            raise ParserException("Node has multiple variable types", xml_element=expression, nodename='get')
