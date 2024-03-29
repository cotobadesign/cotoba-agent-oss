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

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils

import re


class TemplateDeleteVariableNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)
        self._var_type = 'data'
        self._regex = None
        self._regex_text = None

    @property
    def var_type(self):
        return self._var_type

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, regex):
        self._regex = regex

    @property
    def regex_text(self):
        return self._regex_text

    def resolve_to_string(self, client_context):
        resolved = ''

        if self._regex_text is not None and self._regex is None:
            regex_text = self._regex_text.resolve(client_context)
            try:
                regex = re.compile(regex_text)
            except Exception:
                YLogger.debug(client_context, "[%s] invalid regex format [%s]", self.to_string(), regex_text)
                return resolved
        else:
            regex = self._regex

        conversation = client_context.bot.get_conversation(client_context)

        if self._var_type == 'name':
            if regex is None:
                conversation.properties.clear()
            else:
                delete_list = []
                for key in conversation.properties.keys():
                    regex_match = regex.fullmatch(key)
                    if regex_match is not None:
                        delete_list.append(key)

                for key in delete_list:
                    del conversation.properties[key]
        else:
            if regex is None:
                conversation.data_properties.clear()
            else:
                delete_list = []
                for key in conversation.data_properties.keys():
                    regex_match = regex.fullmatch(key)
                    if regex_match is not None:
                        delete_list.append(key)

                for key in delete_list:
                    del conversation.data_properties[key]

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[DELETEVARIABLE (%s)]" % self._var_type

    def to_xml(self, client_context):
        xml = '<deletevariable'
        xml += ' type="%s"' % self._var_type
        if self._regex is not None:
            xml += ' regex="%s"' % self._regex_text
        xml += ' />'
        return xml

    def parse_expression(self, graph, expression):
        if 'type' in expression.attrib:
            var_type = expression.attrib['type']
            if var_type == 'name' or var_type == 'data':
                self._var_type = var_type
            else:
                raise ParserException("Invalid variable type", xml_element=expression, nodename='deletevariable')

        if 'regex' in expression.attrib:
            self._regex_text = expression.attrib['regex']
            if len(self._regex_text) == 0: 
                raise ParserException("Regex parameer empty", xml_element=expression, nodename='deletevariable')
            try:
                self._regex = re.compile(self._regex_text)
            except Exception:
                raise ParserException("Invalid regex format", xml_element=expression, nodename='deletevariable')

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'regex':
                self._regex_text = self.parse_children_as_word_node(graph, child)
                self._regex = None
                if len(self._regex_text.children) == 0: 
                    raise ParserException("Regex parameer empty", xml_element=expression, nodename='deletevariable')
