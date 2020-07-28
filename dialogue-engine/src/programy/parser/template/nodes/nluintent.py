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
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
import json


class TemplateNluIntentNode(TemplateNode):

    VARIABLE_TYPE = ['name', 'data', 'var']
    VAR_NLU_DATA = '__SUBAGENT_NLU__'

    def __init__(self):
        TemplateNode.__init__(self)
        self._intentName = None
        self._itemName = None
        self._index = None

        self._varName = None
        self._varType = None
        self._keys = None

    def resolve_children(self, client_context):
        if self._children:
            return self.resolve_children_to_string(client_context)
        return ""

    def resolve_to_string(self, client_context):
        resolved = ""
        conversation = client_context.bot.get_conversation(client_context)
        intentName = self._intentName.resolve(client_context)
        itemName = self._itemName.resolve(client_context)
        try:
            intentIndex = int(self._index.resolve(client_context))
        except Exception:
            intentIndex = 0

        try:
            if self._varName is None:
                value = conversation.current_question().property("__SYSTEM_NLUDATA__")
                if value is None:
                    YLogger.error(self, "TemplateNluintentNode __SYSTEM_NLUDATA__ is None")
                    resolved = TemplateGetNode.get_default_value(client_context)
                    return resolved
            else:
                if self._varType == 'name':
                    value = conversation.property(self._varName)
                elif self._varType == 'data':
                    value = conversation.data_property(self._varName)
                else:
                    value = conversation.current_question().property(self._varName)
                if value is None:
                    YLogger.error(self, "TemplateNluintentNode %s is None" % self._varName)
                    resolved = TemplateGetNode.get_default_value(client_context)
                    return resolved
        except Exception:
            YLogger.error(self, "TemplateNluintentNode failed to load NLU result")
            resolved = TemplateGetNode.get_default_value(client_context)
            return resolved

        intents = None
        try:
            json_dict = json.loads(value)
            if self._keys is not None:
                first = True
                for key in self._keys:
                    if first:
                        first = False
                        continue
                    json_dict = json_dict[key]
                    if key == self._keys[-1]:
                        break
            intents = json_dict["intents"]
        except Exception:
            YLogger.error(self, "TemplateNluintentNode intents not found in target data")
            resolved = TemplateGetNode.get_default_value(client_context)
            return resolved

        intentsKeyName = "intent"
        intentsKey = [intent.get(intentsKeyName) for intent in intents]
        if itemName == "count":
            if intentName == "*":
                resolved = str(len(intentsKey))
            else:
                resolved = str(intentsKey.count(intentName))

            YLogger.debug(client_context, "nluintent [%s] resolved to [%s]", itemName, resolved)
            return resolved

        index = None
        try:
            if intentName == "*":
                index = 0
                if intentIndex != 0:
                    index = intentIndex
            else:
                if intentIndex != 0:
                    intentCounter = 0
                    counter = 0
                    for name in intentsKey:
                        if name == intentName:
                            if counter == intentIndex:
                                index = intentCounter
                            counter += 1
                        intentCounter += 1
                else:
                    index = intentsKey.index(intentName)
        except Exception:
            YLogger.debug(client_context, "nluintent non search keys:%s", intentName)

        if index is not None:
            YLogger.debug(client_context, "nluintent index[%s]", index)
            try:
                if itemName in intents[index]:
                    resolved = str(intents[index].get(itemName))
            except Exception:
                YLogger.debug(client_context, "nluintent non search item:%s", itemName)

        if resolved == '':
            YLogger.debug(client_context, "nluintent  failed intent=[%s] item=[%s]", intentName, itemName)
            resolved = TemplateGetNode.get_default_value(client_context)

        YLogger.debug(client_context, "nluintent  [%s] resolved to [%s:%s]", intentName, itemName, resolved)

        return resolved

    def to_string(self):
        return "[nluintent]"

    def to_xml(self, client_context):
        xml = "<nluintent"
        if self._varName is not None:
            xml += ' target="%s"' % self._varName
            xml += ' type="%s"' % self._varType
        xml += ">"
        xml += "<name>"
        xml += self._intentName.to_xml(client_context)
        xml += "</name>"
        xml += "<item>"
        xml += self._itemName.to_xml(client_context)
        xml += "</item>"
        if self._index is not None:
            xml += "<index>"
            xml += self._index.to_xml(client_context)
            xml += "</index>"
        xml += self.children_to_xml(client_context)
        xml += "</nluintent>"
        return xml

    # ######################################################################################################
    # JSON_PREDICATE_EXPRESSION ::==
    # <json name="JSONName">TEMPLATE_EXPRESSION</json> |

    def parse_expression(self, graph, expression):

        if 'name' in expression.attrib:
            self._intentName = self.parse_attrib_value_as_word_node(graph, expression, 'name')

        if 'item' in expression.attrib:
            self._itemName = self.parse_attrib_value_as_word_node(graph, expression, 'item')

        if 'index' in expression.attrib:
            self._index = self.parse_attrib_value_as_word_node(graph, expression, 'index')

        if 'target' in expression.attrib:
            var_name = expression.attrib['target']
            if var_name != '':
                self._varName = var_name
        if 'type' in expression.attrib:
            var_type = expression.attrib['type']
            if var_type in self.VARIABLE_TYPE:
                self._varType = var_type
            else:
                raise ParserException("Invalid variable type [%s]" % var_type, xml_element=expression, nodename='nluintent')

        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tagName = TextUtils.tag_from_text(child.tag)

            if tagName == 'name':
                self._intentName = self.parse_children_as_word_node(graph, child)
            if tagName == 'item':
                self._itemName = self.parse_children_as_word_node(graph, child)
            if tagName == 'index':
                self._index = self.parse_children_as_word_node(graph, child)
            else:
                graph.parse_tag_expression(child, self)
                self.parse_text(graph, self.get_tail_from_element(child))

        if self._intentName is None or self._itemName is None:
            raise ParserException("Missing either intent or item", xml_element=expression, nodename='nluintent')

        if self._varName is None:
            self._varType = None
        else:
            if self._varType is None:
                self._varType = 'var'

        if self._varType == 'var':
            keys = self._varName.split('.')
            if keys[0] == self.VAR_NLU_DATA and len(keys) == 2:
                self._varName = keys[0]
                self._keys = keys
