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
from programy.utils.language.japanese import JapaneseLanguage

import re


class TemplateMapNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def resolve_children(self, client_context):
        if self._children:
            return self.resolve_children_to_string(client_context)
        return ""

    def get_default_value(self, client_context):
        value = client_context.brain.properties.property("default-map")
        if value is None:
            value = client_context.brain.configuration.defaults.default_map
            if value is None:
                YLogger.debug(client_context, "No value for default-map defined, empty string returned")
                value = ""
        return value

    def resolve_to_string(self, client_context):
        name = self.name.resolve(client_context)
        name = JapaneseLanguage.zenhan_normalize(name)
        name = name.upper()

        targer_word = self.resolve_children(client_context)
        targer_word = JapaneseLanguage.zenhan_normalize(targer_word)
        var = targer_word.upper()

        if client_context.brain.dynamics.is_dynamic_map(name) is True:
            value = client_context.brain.dynamics.dynamic_map(client_context, name, var)
        else:
            if client_context.brain.maps.contains(name) is False:
                YLogger.debug(client_context, "No map defined for [%s], using default-map as value", var)
                value = self.get_default_value(client_context)
            else:
                the_map = client_context.brain.maps.map(name)
                if var in the_map:
                    value = the_map[var]
                else:
                    YLogger.debug(client_context, "No value defined for [%s], using default-map as value", var)
                    value = self.get_default_value(client_context)

        YLogger.debug(client_context, "MAP [%s] resolved to [%s] = [%s]", self.to_string(), name, value)
        return value

    def to_string(self):
        return "[MAP (%s)]" % (self.name.to_string())

    def to_xml(self, client_context):
        xml = "<map "
        xml += ' name="%s"' % self.name.resolve(client_context)
        xml += ">"
        xml += self.children_to_xml(client_context)
        xml += "</map>"
        return xml

    # ######################################################################################################
    # MAP_EXPRESSION ::=
    # <map name="WORD">TEMPLATE_EXPRESSION</map> |
    # <map><name>TEMPLATE_EXPRESSION</name>TEMPLATE_EXPRESSION</map>

    def parse_expression(self, graph, expression):

        name_found = False

        if 'name' in expression.attrib:
            name = self.parse_attrib_value_as_word_node(graph, expression, 'name')
            name_text = JapaneseLanguage.zenhan_normalize(name.children[0].word)
            map_name = name_text.upper()
            if graph.aiml_parser.brain.maps.storename(map_name) is None:
                if graph.aiml_parser.brain.dynamics.is_dynamic_map(map_name) is False:
                    raise ParserException("Map[%s] name not found" % map_name, xml_element=expression, nodename='map')
            self.name = name
            name_found = True

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'name':
                self.name = self.parse_children_as_word_node(graph, child)
                name_found = True

            else:
                graph.parse_tag_expression(child, self)

            self.parse_text(graph, self.get_tail_from_element(child))

        if name_found is False:
            raise ParserException("Name not found in map", xml_element=expression, nodename='map')
