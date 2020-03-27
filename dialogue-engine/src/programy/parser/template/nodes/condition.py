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
import re

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.bot import TemplateBotNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException, LimitOverException
from programy.utils.text.text import TextUtils


class TemplateConditionValueNode(TemplateNode):

    def __init__(self, name=None, resolved=None):
        TemplateNode.__init__(self)
        self._name = name
        self._resolved = resolved

    @property
    def resolved(self):
        return self._resolved

    @resolved.setter
    def resolved(self, resolved):
        self._resolved = resolved

    def to_string(self):
        if self._resolved is not None:
            node_text = self._resolved
        else:
            node_text = ''
            for child in self.children:
                node_text += child.to_string()
        return node_text

    def to_xml(self, client_context):
        xml = self.children_to_xml(client_context)
        return xml


class TemplateConditionVariable(TemplateNode):

    DEFAULT = 0
    GLOBAL = 1
    DATA = 2
    LOCAL = 3
    BOT = 4
    MULTI = 9

    def __init__(self, name=None, value=None, var_type=GLOBAL, loop=False, regex=None):
        TemplateNode.__init__(self)
        self._name = name
        self._value = value
        self._var_type = var_type
        self._loop = loop
        self._regex = regex

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def var_type(self):
        return self._var_type

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, loop):
        self._loop = loop

    @property
    def regex(self):
        return self._regex

    @regex.setter
    def regex(self, regex):
        self._regex = regex


class TemplateConditionListItemNode(TemplateConditionVariable):

    def __init__(self, name=None, value=None, var_type=TemplateConditionVariable.GLOBAL, loop=False, regex=None):
        TemplateConditionVariable.__init__(self, name, value, var_type, loop, regex)
        self._cond_var_name = None
        self._cond_var_type = None

    @property
    def cond_var_name(self):
        return self._cond_var_name

    @cond_var_name.setter
    def cond_var_name(self, var_name):
        self._cond_var_name = var_name

    @property
    def cond_var_type(self):
        return self._cond_var_type

    @cond_var_type.setter
    def cond_var_type(self, var_type):
        self._cond_var_type = var_type

    def is_default(self):
        return bool(self.value is None and self.regex is None)

    def to_string(self):
        name = None
        var_type = None
        if self._cond_var_name is not None:
            name = self._cond_var_name.to_string()
            var_type = self._cond_var_type
        elif self.name is not None:
            name = self.name.to_string()
            var_type = self._var_type

        if name is not None:
            if var_type == TemplateConditionListItemNode.GLOBAL:
                type_name = 'name'
            elif var_type == TemplateConditionListItemNode.DATA:
                type_name = 'data'
            elif var_type == TemplateConditionListItemNode.LOCAL:
                type_name = 'var'
            elif var_type == TemplateConditionListItemNode.BOT:
                type_name = 'bot'
            elif var_type == TemplateConditionListItemNode.DEFAULT:
                type_name = 'default'
            else:
                type_name = 'unknown'

            if self.regex is not None:
                return '[CONDITIONLIST(%s="%s" regex="%s")]' % (type_name, name, self.regex.to_string())
            elif self.value is not None:
                return '[CONDITIONLIST(%s="%s" value="%s")]' % (type_name, name, self.value.to_string())

        if self.regex is not None:
            return "[CONDITIONLIST(%s)]" % self.regex.to_string()
        elif self.value is not None:
            return "[CONDITIONLIST(%s)]" % self.value.to_string()

        return "[CONDITIONLIST]"

    def to_xml(self, client_context):

        xml = '<li>'
        if self.name is not None:
            if self.var_type == TemplateConditionListItemNode.GLOBAL:
                xml += '<name>%s</name>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.DATA:
                xml += '<data>%s</data>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.LOCAL:
                xml += '<var>%s</var>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.BOT:
                xml += '<bot>%s</bot>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.DEFAULT:
                xml += '<default>%s</default>' % self.name.to_xml(client_context)
            else:
                xml += '<unknown>%s</unknown>' % self.name.to_xml(client_context)

        if self.regex is not None:
            xml += '<regex>'
            xml += self.regex.to_xml(client_context)
            xml += '</regex>'
        elif self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(client_context)
            xml += '</value>'

        xml += self.children_to_xml(client_context)

        if self.loop is True:
            xml += "<loop />"

        xml += '</li>'

        return xml


class TemplateConditionNode(TemplateConditionVariable):

    BLOCK = 1
    SINGLE = 2
    MULTIPLE = 3

    def __init__(self, name=None, value=None, var_type=TemplateConditionVariable.GLOBAL, loop=False, condition_type=BLOCK, regex=None):
        TemplateConditionVariable.__init__(self, name, value, var_type, loop, regex)
        self._condition_type = condition_type

        self._max_search_condition = 0
        self._loop_count = 0

    def get_default(self):
        for child in self.children:
            if child.is_default() is True:
                return child
        return None

    #######################################################################################################
    # CONDITION_ITEM_COMPONENT ::== <name>TEMPLATE_EXPRESSION</name> | <value>TEMPLATE_EXPRESSION</value> | <loop/> | TEMPLATE_EXPRESSION
    # CONDITION_ITEM_EXPRESSION ::== <li( CONDITION_ATTRIBUTES)*>(CONDITION_ITEM_COMPONENT)*</li>
    # CONDITION_ATTRIBUTES ::== (name="NAME") | (value="NORMALIZED_TEXT")
    # CONDITION_EXPRESSION ::== <condition( CONDITION_ATTRIBUTES)>(CONDITION_ITEM_EXPRESSION)*</condition>
    #

    def make_sub_node(self, graph, child, name, attribute=False):
        sub_node = TemplateConditionValueNode(name)
        if attribute is True:
            word_class = graph.get_node_class_by_name('word')
            sub_node.append(word_class(child.attrib[name]))
        else:
            sub_node.parse_text(graph, self.get_text_from_element(child))
            for sub_pattern in child:
                graph.parse_tag_expression(sub_pattern, sub_node)
                tail_text = self.get_tail_from_element(sub_pattern)
                sub_node.parse_text(graph, tail_text)
        return sub_node

    def get_condition_name(self, graph, condition):
        var_name = None
        var_type = TemplateConditionVariable.DEFAULT
        var_count = 0

        if 'name' in condition.attrib:
            var_name = self.make_sub_node(graph, condition, 'name', True)
            var_type = TemplateConditionVariable.GLOBAL
            var_count += 1
        if 'data' in condition.attrib:
            var_name = self.make_sub_node(graph, condition, 'data', True)
            var_type = TemplateConditionVariable.DATA
            var_count += 1
        if 'var' in condition.attrib:
            var_name = self.make_sub_node(graph, condition, 'var', True)
            var_type = TemplateConditionVariable.LOCAL
            var_count += 1
        if 'bot' in condition.attrib:
            var_name = self.make_sub_node(graph, condition, 'bot', True)
            var_type = TemplateConditionVariable.BOT
            var_count += 1

        names = condition.findall('name')
        if names:
            if len(names) > 1:
                var_count += len(names)
            else:
                if var_count == 0:
                    var_name = self.make_sub_node(graph, names[0], 'name')
                    var_type = TemplateConditionVariable.GLOBAL
                var_count += 1

        datas = condition.findall('data')
        if datas:
            if len(datas) > 1:
                var_count += len(datas)
            else:
                if var_count == 0:
                    var_name = self.make_sub_node(graph, datas[0], 'data')
                    var_type = TemplateConditionVariable.DATA
                var_count += 1

        vars = condition.findall('var')
        if vars:
            if len(vars) > 1:
                var_count += len(vars)
            else:
                if var_count == 0:
                    var_name = self.make_sub_node(graph, vars[0], 'var')
                    var_type = TemplateConditionVariable.LOCAL
                var_count += 1

        bots = condition.findall('bot')
        if bots:
            is_variable = False
            tag_count = 0
            for bot in bots:
                if len(bot.attrib) == 0:
                    is_variable = True
                    tag_count += 1
            if is_variable is True:
                if tag_count > 1:
                    var_count += tag_count
                else:
                    if var_count == 0:
                        var_name = self.make_sub_node(graph, bots[0], 'bot')
                        var_type = TemplateConditionVariable.BOT
                    var_count += 1

        if var_count > 1:
            var_type = TemplateConditionVariable.MULTI

        return var_name, var_type

    def get_condition_value(self, graph, condition):

        value_node = None

        if 'value' in condition.attrib:
            value_node = self.make_sub_node(graph, condition, 'value', True)

        values = condition.findall('value')
        if values:
            if len(values) > 1:
                raise ParserException("Node has multiple value elements", xml_element=condition, nodename='condition')
            elif value_node is not None:
                raise ParserException("Node has multiple value elements", xml_element=condition, nodename='condition')
            else:
                value_node = self.make_sub_node(graph, values[0], 'value')

        return value_node

    def get_condition_regex(self, graph, condition):

        regex_node = None

        if 'regex' in condition.attrib:
            regex_node = self.make_sub_node(graph, condition, 'regex', True)

        regexs = condition.findall('regex')
        if regexs:
            if len(regexs) > 1:
                raise ParserException("Node has multiple regex elements", xml_element=condition, nodename='condition')
            elif regex_node is not None:
                raise ParserException("Node has multiple regex elements", xml_element=condition, nodename='condition')
            else:
                regex_node = self.make_sub_node(graph, regexs[0], 'regex')

        if regex_node is not None:
            if len(regex_node.children) == 1 and type(regex_node.children[0]) == TemplateWordNode:
                try:
                    re.compile(regex_node.children[0].word, re.IGNORECASE)
                except Exception:
                    raise ParserException("Invalid regex format", xml_element=condition, nodename='condition')

        return regex_node

    # Type 1
    # <condition name="property" value="v">X</condition>,
    # <condition name="property"><value>v</value>X</condition>,
    # <condition value="v"><name>property</name>X</condition>, and
    # <condition><name>property</name><value>v</value>X</condition>
    #

    # Type 2
    # <condition name="property">
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<li>Z</li>				        <- Optional default value if no condition met
    # </ condition>
    # <condition name="property">
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<loop />				        <- Loop if no condition met
    # </ condition>
    # <condition name="property">
    # 	<li value="a">X</li>
    # 	<li value="b">Y <loop /></li>   <- Loop if condition set
    # </ condition>
    # or
    #
    # <condition>
    #   <name>property</name>
    # 	<li value="a">X</li>
    # 	<li value="b">Y</li>
    # 	<li>Z</li>				        <- Optional default value if no condition met
    # </ condition>
    #

    # Type 3
    #  <condition>
    # 	<li name='1' value="a">X</li>
    # 	<li value="b"><name>1</name>Y</li>
    # 	<li name="1"><value>b</value>Z</li>
    # 	<li><name>1</name><value>b</value>Z</li>
    # 	<li>Z</li>				        <- Optional default value if no condition met
    #  </condition>
    #

    def parse_expression(self, graph, expression):

        name, var_type = self.get_condition_name(graph, expression)
        if var_type == TemplateConditionVariable.MULTI:
            raise ParserException("Node has multiple variable types", xml_element=expression, nodename='condition')

        value = self.get_condition_value(graph, expression)
        regex = self.get_condition_regex(graph, expression)

        if name is not None:
            self._name = name
            self._var_type = var_type
            if regex is not None:
                if value is not None:
                    raise ParserException("Value and regex elements exist", xml_element=expression, nodename='condition')
                self._condition_type = TemplateConditionNode.BLOCK
                self._regex = regex
                self.parse_type1_condition(graph, expression)
            elif value is not None:
                self._condition_type = TemplateConditionNode.BLOCK
                self._value = value
                self.parse_type1_condition(graph, expression)
            else:
                self._condition_type = TemplateConditionNode.SINGLE
                self.parse_type2_condition(graph, expression)
        else:
            self._condition_type = TemplateConditionNode.MULTIPLE
            self.parse_type3_condition(graph, expression)

    def parse_type1_condition(self, graph, expression):
        self.parse_text(graph, self.get_text_from_element(expression))

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name in ['name', 'data', 'var', 'bot', 'value', 'regex']:
                pass

            elif tag_name == 'li':
                raise ParserException("Li element not allowed as child", xml_element=expression, nodename='condition')

            elif tag_name == 'loop':
                raise ParserException("This type cannot have loop element", xml_element=expression, nodename='condition')

            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

    def parse_type2_condition(self, graph, expression):

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name in ['name', 'data', 'var', 'bot']:
                pass

            elif tag_name == 'li':

                list_item = TemplateConditionListItemNode()

                _, var_type = self.get_condition_name(graph, child)
                if var_type != TemplateConditionVariable.DEFAULT:
                    raise ParserException("Invalid li variable", xml_element=expression, nodename='condition')

                value = self.get_condition_value(graph, child)
                regex = self.get_condition_regex(graph, child)
                if regex is not None:
                    if value is not None:
                        raise ParserException("Value and regex elements exist", xml_element=expression, nodename='condition')
                    list_item._regex = regex
                else:
                    list_item._value = value
                list_item._var_type = self._var_type

                self.children.append(list_item)
                list_item.parse_text(graph, self.get_text_from_element(child))

                for sub_pattern in child:

                    if sub_pattern.tag in ['name', 'data', 'var', 'bot', 'value', 'regex']:
                        pass

                    elif sub_pattern.tag == 'loop':
                        list_item.loop = True

                    else:
                        graph.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    list_item.parse_text(graph, tail_text)

            else:
                raise ParserException("Invalid element <%s>" % tag_name, xml_element=expression, nodename='condition')

    def parse_type3_condition(self, graph, expression):
        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name in ['name', 'data', 'var', 'bot']:
                pass

            elif tag_name == 'li':
                list_item = TemplateConditionListItemNode()

                name, var_type = self.get_condition_name(graph, child)
                if var_type == TemplateConditionVariable.MULTI:
                    raise ParserException("Node has multiple variable types", xml_element=expression, nodename='condition')

                list_item._name = name
                list_item._var_type = var_type

                value = self.get_condition_value(graph, child)
                regex = self.get_condition_regex(graph, child)
                if regex is not None:
                    if value is not None:
                        raise ParserException("Value and regex elements exist", xml_element=expression, nodename='condition')
                    list_item._regex = regex
                else:
                    list_item._value = value

                if list_item._var_type == TemplateConditionVariable.DEFAULT and \
                   (list_item._value is not None or list_item._regex is not None):
                    raise ParserException("Li element missing variable", xml_element=expression, nodename='condition')
                if list_item._var_type != TemplateConditionVariable.DEFAULT and \
                   list_item._value is None and list_item._regex is None:
                    raise ParserException("Li element Missing value", xml_element=expression, nodename='condition')

                self.children.append(list_item)

                list_item.parse_text(graph, self.get_text_from_element(child))

                for sub_pattern in child:
                    if sub_pattern.tag in ['name', 'data', 'var', 'bot', 'value', 'regex']:
                        pass

                    elif sub_pattern.tag == 'loop':
                        list_item.loop = True

                    else:
                        graph.parse_tag_expression(sub_pattern, list_item)

                    tail_text = self.get_tail_from_element(sub_pattern)
                    list_item.parse_text(graph, tail_text)

            else:
                raise ParserException("Invalid element <%s>" % tag_name, xml_element=expression, nodename='condition')

    def to_string(self):
        text = "[CONDITION"
        if self.name is not None:
            if self.var_type == TemplateConditionListItemNode.GLOBAL:
                text += ' name="%s"' % self.name.to_string()
            elif self.var_type == TemplateConditionListItemNode.DATA:
                text += ' data="%s"' % self.name.to_string()
            elif self.var_type == TemplateConditionListItemNode.LOCAL:
                text += ' var="%s"' % self.name.to_string()
            elif self.var_type == TemplateConditionListItemNode.BOT:
                text += ' bot="%s"' % self.name.to_string()
            else:
                text += ' unknown="%s"' % self.name.to_string()

            if self.regex is not None:
                text += ' regex="%s"' % self.regex.to_string()
            elif self.value is not None:
                text += ' value="%s"' % self.value.to_string()
            else:
                text += ' value=default'
        else:
            text += ' default'

        text += "]"
        return text

    def to_xml(self, client_context):
        xml = "<condition>"

        if self.name is not None:
            if self.var_type == TemplateConditionListItemNode.GLOBAL:
                xml += '<name>%s</name>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.DATA:
                xml += '<data>%s</data>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.LOCAL:
                xml += '<var>%s</var>' % self.name.to_xml(client_context)
            elif self.var_type == TemplateConditionListItemNode.BOT:
                xml += '<bot>%s</bot>' % self.name.to_xml(client_context)
            else:
                xml += '<unknown>%s</unknown>' % self.name.to_xml(client_context)

        if self.regex is not None:
            xml += '<regex>'
            xml += self.regex.to_xml(client_context)
            xml += '</regex>'
        elif self.value is not None:
            xml += '<value>'
            xml += self.value.to_xml(client_context)
            xml += '</value>'

        xml += self.children_to_xml(client_context)

        xml += "</condition>"

        return xml

    def resolve(self, client_context):
        self._max_search_condition = client_context.bot.configuration.max_search_condition
        self._loop_count = 0

        return self._resolve_sub(client_context)

    def _resolve_sub(self, client_context):
        self._loop_count += 1
        if self._loop_count > self._max_search_condition:
            raise LimitOverException("Max search condition [%d] exceeded: %s" % (self._max_search_condition, self.to_string()))

        if self._condition_type == TemplateConditionNode.BLOCK:
            return self.resolve_type1_condition(client_context)
        elif self._condition_type == TemplateConditionNode.SINGLE:
            return self.resolve_type2_condition(client_context)
        elif self._condition_type == TemplateConditionNode.MULTIPLE:
            return self.resolve_type3_condition(client_context)
        return None

    def get_condition_variable_value(self, client_context, var_type, name):
        if var_type == TemplateConditionVariable.GLOBAL:
            return TemplateGetNode.get_property_value(client_context, 'name', name)
        elif var_type == TemplateConditionVariable.DATA:
            return TemplateGetNode.get_property_value(client_context, 'data', name)
        elif var_type == TemplateConditionVariable.LOCAL:
            return TemplateGetNode.get_property_value(client_context, 'var', name)
        elif var_type == TemplateConditionVariable.BOT:
            return TemplateBotNode.get_bot_variable(client_context, name)
        else:
            return "unknown"

    def resolve_type1_condition(self, client_context):
        try:
            self.name.resolved = self.name.resolve(client_context)
            value = self.get_condition_variable_value(client_context, self.var_type, self.name.resolved)

            if self.regex is not None:
                self.regex.resolved = self.regex.resolve(client_context)
                regex_pattern = re.compile(self.regex.resolved, re.IGNORECASE)
                regex_match = regex_pattern.fullmatch(value)
                if regex_match is not None:
                    resolved = client_context.brain.tokenizer.words_to_texts([child.resolve(client_context) for child in self.children])
                else:
                    resolved = ""
                YLogger.debug(client_context, "[%s] resolved (regex) to [%s]", self.to_string(), resolved)
                return resolved
            else:
                self.value.resolved = self.value.resolve(client_context)
                if value.upper() == self.value.resolved.upper():
                    resolved = client_context.brain.tokenizer.words_to_texts([child.resolve(client_context) for child in self.children])
                else:
                    resolved = ""

                YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
                return resolved

        except LimitOverException:
            raise
        except Exception:
            raise

    def resolve_type2_condition(self, client_context):
        try:
            self.name.resolved = self.name.resolve(client_context)
            value = self.get_condition_variable_value(client_context, self.var_type, self.name.resolved)

            for condition in self.children:
                if condition.is_default() is True:
                    continue

                condition.cond_var_name = self.name
                condition.cond_var_type = self.var_type

                if condition.regex is not None:
                    condition.regex.resolved = condition.regex.resolve(client_context)
                    regex_pattern = re.compile(condition.regex.resolved, re.IGNORECASE)
                    regex_match = regex_pattern.fullmatch(value)
                    if regex_match is not None:
                        resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in condition.children])
                        YLogger.debug(client_context, "[%s] resolved (regex) to [%s]", condition.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self._resolve_sub(client_context).strip()
                        return resolved
                else:
                    condition.value.resolved = condition.value.resolve(client_context)
                    if value.upper() == condition.value.resolved.upper():
                        resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in condition.children])
                        YLogger.debug(client_context, "[%s] resolved to [%s]", condition.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self._resolve_sub(client_context)

                        return resolved

            default = self.get_default()
            if default is not None:
                resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self._resolve_sub(client_context)
            else:
                resolved = ""

            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except LimitOverException:
            raise
        except Exception:
            raise

    def resolve_type3_condition(self, client_context):
        try:
            for condition in self.children:
                if condition.is_default() is True:
                    continue

                condition.name.resolved = condition.name.resolve(client_context)
                value = self.get_condition_variable_value(client_context, condition.var_type, condition.name.resolved)

                if condition.regex is not None:
                    condition.regex.resolved = condition.regex.resolve(client_context)
                    regex_pattern = re.compile(condition.regex.resolved, re.IGNORECASE)
                    regex_match = regex_pattern.fullmatch(value)
                    if regex_match is not None:
                        resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in condition.children])
                        YLogger.debug(client_context, "[%s] resolved (regex) to [%s]", condition.to_string(), resolved)

                        if condition.loop is True:
                            resolved = resolved.strip() + " " + self._resolve_sub(client_context).strip()
                        return resolved
                else:
                    if condition.value is not None:
                        condition.value.resolved = condition.value.resolve(client_context)
                        if value.upper() == condition.value.resolved.upper():
                            resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in condition.children])
                            YLogger.debug(client_context, "[%s] resolved to [%s]", condition.to_string(), resolved)

                            if condition.loop is True:
                                resolved = resolved.strip() + " " + self._resolve_sub(client_context).strip()

                            return resolved

            default = self.get_default()
            if default is not None:
                resolved = client_context.brain.tokenizer.words_to_texts([child_node.resolve(client_context) for child_node in default.children])

                if default.loop is True:
                    resolved = resolved.strip() + " " + self._resolve_sub(client_context).strip()

            else:
                resolved = ""

            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
            return resolved

        except LimitOverException:
            raise
        except Exception:
            raise
