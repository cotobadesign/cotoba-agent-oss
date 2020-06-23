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

import json
import ast

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.services.service import ServiceFactory
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils


class TemplateSRAIXSubNode(TemplateNode):

    def __init__(self, name=None, value=None):
        TemplateNode.__init__(self)
        self._name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    def to_string(self):
        return self._name

    def to_xml(self, client_context):
        xml = self.children_to_xml(client_context)
        return xml


class TemplateSRAIXNode(TemplateNode):

    SERVICE_PUBLISHED_REST = '__PublishedREST__'
    SERVICE_PUBLISHED_BOT = '__PublishedBot__'
    SRAIX_CHILD_IN = '\uF010'
    SRAIX_CHILD_OUT = '\uF011'

    def __init__(self):
        TemplateNode.__init__(self)

        self._host = None
        self._method = None
        self._query = None
        self._header = None
        self._body = None

        self._botId = None
        self._botHost = None
        self._locale = None
        self._time = None
        self._userId = None
        self._topic = None
        self._deleteVariable = None
        self._metadata = None
        self._config = None

        self._service = None

        self._default = None

    @property
    def botId(self):
        return self._botId

    @property
    def botHost(self):
        return self._botHost

    @property
    def service(self):
        return self._service

    @property
    def default(self):
        return self._default

    @botId.setter
    def botId(self, botId):
        self._botId = botId

    @botHost.setter
    def botHost(self, botHost):
        self._botHost = botHost

    @service.setter
    def service(self, service):
        self._service = service

    def _delete_shift_code(self, text):
        if self.SRAIX_CHILD_IN in text:
            rep_text = text.replace(self.SRAIX_CHILD_IN, '')
            rep_text = rep_text.replace(self.SRAIX_CHILD_OUT, '')
        else:
            rep_text = text
        return rep_text

    def _published_REST_interface(self, client_context):
        self.method = None
        self.query = None
        self.header = None
        self.body = None

        self.host = self._host.resolve(client_context)
        if self._method is None:
            self.method = 'GET'
        else:
            self.method = self._method.resolve(client_context)
        if self._query is not None:
            shift_text = self._query.resolve(client_context)
            self.query = self._delete_shift_code(shift_text)
        if self._header is not None:
            shift_text = self._header.resolve(client_context)
            self.header = self._delete_shift_code(shift_text)
        if self._body is not None:
            self.body = self._body.resolve(client_context)

        resolved = self.resolve_children_to_string(client_context)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        bot_service = ServiceFactory.get_service(self.SERVICE_PUBLISHED_REST)
        bot_service.host = self.host
        bot_service.method = self.method
        try:
            if self.query is None:
                bot_service.query = self.query
            else:
                bot_service.query = ast.literal_eval("{" + self.query + "}")
            if self.header is None:
                bot_service.header = self.header
            else:
                bot_service.header = ast.literal_eval("{" + self.header + "}")
            bot_service.body = self.body
            response = bot_service.ask_question(client_context, resolved)
            YLogger.debug(client_context, "SRAIX host [%s] return [%s]", self.host, response)
        except Exception:
            YLogger.debug(client_context, "SRAIX Rest parameter convet failed")
            response = ''

        conversation = client_context.bot.get_conversation(client_context)
        status_code = ''
        try:
            status_code = bot_service.get_status_code()
        except NotImplementedError:
            pass
        if conversation.has_current_question() is True:
            conversation.current_question().set_property('__SUBAGENT_STATUS_CODE__', status_code)

        if response is not None:
            if response == '' and self.default is not None:
                response = self.default
            variableName = "__SUBAGENT_BODY__"
            if conversation.has_current_question() is True:
                conversation.current_question().set_property(variableName, response)
        return response

    def _published_Bot_interface(self, client_context):
        self.locale = None
        self.time = None
        self.userId = None
        self.topic = None
        self.deleteVariable = None
        self.metadata = None
        self.config = None

        conversation = client_context.bot.get_conversation(client_context)

        if self._locale is not None:
            self.locale = self._locale.resolve(client_context)
        if self._time is not None:
            self.time = self._time.resolve(client_context)
        if self._userId is not None:
            self.userId = self._userId.resolve(client_context)
        if self._topic is not None:
            self.topic = self._topic.resolve(client_context)
        if self._topic is None or self.topic == '*':
            if conversation.property('topic') != '*':
                self.topic = conversation.property('topic')
        if self._deleteVariable is None:
            self.deleteVariable = None
        else:
            self.deleteVariable = self._deleteVariable.resolve(client_context)
            if self.deleteVariable.upper() == 'TRUE':
                self.deleteVariable = True
            else:
                self.deleteVariable = False
        if self._metadata is not None:
            self.metadata = self._metadata.resolve(client_context)
        if self._config is not None:
            shift_text = self._config.resolve(client_context)
            self.config = self._delete_shift_code(shift_text)

        resolved = self.resolve_children_to_string(client_context)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        bot_service = ServiceFactory.get_service(self.SERVICE_PUBLISHED_BOT)
        bot_service.botId = self.botId
        bot_service.botHost = self.botHost
        bot_service.locale = self.locale
        bot_service.time = self.time
        bot_service.userId = self.userId
        bot_service.topic = self.topic
        bot_service.deleteVariable = self.deleteVariable
        bot_service.metadata = self.metadata
        bot_service.config = self.config
        response = bot_service.ask_question(client_context, resolved)
        YLogger.debug(client_context, "SRAIX botid [%s] return [%s]", self._botId, response)

        status_code = ''
        try:
            status_code = bot_service.get_status_code()
        except NotImplementedError:
            pass
        if conversation.has_current_question() is True:
            conversation.current_question().set_property('__SUBAGENT_STATUS_CODE__', status_code)

        if response is not None:
            if conversation.has_current_question() is False:
                if response == '' and self.default is not None:
                    response = self.default
            else:
                variableName = "__SUBAGENT_EXTBOT__"
                if response != '':
                    try:
                        response_dic = json.loads(response)
                        save_dic = {self._botId: response_dic}
                        conversation.current_question().set_property(variableName, json.dumps(save_dic))
                        response_data = response_dic['response']
                        if type(response_data) is dict:
                            response = json.dumps(response_data)
                        else:
                            response = response_data
                    except Exception:
                        if self.default is not None:
                            response = self.default
                        else:
                            response = ''
                else:
                    if self.default is not None:
                        response = self.default
                    variableName += ".%s" % self._botId
                    conversation.current_question().set_property(variableName, response)
        return response

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)
        if conversation.has_current_question() is True:
            conversation.current_question().set_property('__SUBAGENT_STATUS_CODE__', '')

        if self._service is not None:
            resolved = self.resolve_children_to_string(client_context)
            YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

            bot_service = ServiceFactory.get_service(self.service)
            response = bot_service.ask_question(client_context, resolved)
            YLogger.debug(client_context, "SRAIX service [%s] return [%s]", self.service, response)

            status_code = ''
            try:
                status_code = bot_service.get_status_code()
            except NotImplementedError:
                pass
            if conversation.has_current_question() is True:
                conversation.current_question().set_property('__SUBAGENT_STATUS_CODE__', status_code)

            if response is not None:
                if conversation.has_current_question() is False:
                    if self.default is not None:
                        response = self.default
                else:
                    variableName = "__SUBAGENT__"
                    if response != '':
                        try:
                            response_json = json.loads(response)
                            save_dic = {self.service: response_json}
                            conversation.current_question().set_property(variableName, json.dumps(save_dic))
                        except Exception:
                            variableName += ".%s" % self.service
                            conversation.current_question().set_property(variableName, response)
                    else:
                        if self.default is not None:
                            response = self.default
                        variableName += ".%s" % self.service
                        conversation.current_question().set_property(variableName, response)
            return response

        elif self._botId is not None:
            response = self._published_Bot_interface(client_context)
            return response

        elif self._host is not None:
            response = self._published_REST_interface(client_context)
            return response

        else:
            YLogger.debug(client_context, "Sorry SRAIX does not currently have an implementation for [%s]", self._service)
            return ''

    def to_string(self):
        if self._service is not None:
            texts = "[SRAIX (service=%s" % self.service
            if self._default is not None:
                texts += ", default=%s" % self.default
            texts += ")]"
            return texts
        elif self._botId is not None:
            texts = "[SRAIX (botID=%s" % self.botId
            if self._botHost is not None:
                texts += ", host=%s" % self.botHost
            if self._default is not None:
                texts += ", default=%s" % self.default
            if self._locale is not None:
                texts += ", locale=%s" % self.locale
            if self._time is not None:
                texts += ", time=%s" % self.time
            if self._userId is not None:
                texts += ", userId=%s" % self.userId
            if self._topic is not None:
                texts += ", topic=%s" % self.topic
            if self._deleteVariable is not None:
                texts += ", deleteVariable=%s" % str(self.deleteVariable).lower()
            if self._metadata is not None:
                texts += ", metadata=%s" % self.metadata
            if self._config is not None:
                texts += ", config=%s" % self.config
            texts += ")]"
            return texts
        elif self._host is not None:
            texts = "[SRAIX (host=%s" % self.host
            if self._default is not None:
                texts += ", default=%s" % self.default
            if self._method is not None:
                texts += ", method=%s" % self.method
            if self._query is not None:
                texts += ", query={%s}" % self.query
            if self._header is not None:
                texts += ", header={%s}" % self.header
            if self._body is not None:
                texts += ", body=%s" % self.body
            texts += ")]"
            return texts

        return "[SRAIX ()]"

    def to_xml(self, client_context):
        xml = '<sraix'
        if self._service is not None:
            xml += ' service="%s"' % self._service
            if self._default is not None:
                xml += ' default="%s"' % self._default
            xml += '>'
        elif self._botId is not None:
            xml += ' botId="%s"' % self._botId
            if self._botHost is not None:
                xml += ' host="%s"' % self._botHost
            if self._default is not None:
                xml += ' default="%s"' % self._default
            xml += '>'
            if self._locale is not None:
                xml += '<locale>%s</locale>' % self._locale.to_xml(client_context)
            if self._time is not None:
                xml += '<time>%s</time>' % self._time.to_xml(client_context)
            if self._userId is not None:
                xml += '<userId>%s</userId>' % self._userId.to_xml(client_context)
            if self._topic is not None:
                xml += '<topic>%s</topic>' % self._topic.to_xml(client_context)
            if self._deleteVariable is not None:
                xml += '<deleteVariable>%s</deleteVariable>' % self._deleteVariable.to_xml(client_context)
            if self._metadata is not None:
                xml += '<metadata>%s</metadata>' % self._metadata.to_xml(client_context)
            if self._config is not None:
                xml += '<config>%s</config>' % self._config.to_xml(client_context)
        elif self._host is not None:
            if self._default is not None:
                xml += ' default="%s"' % self._default
            xml += '>'
            xml += '<host>%s</host>' % self._host.to_xml(client_context)
            if self._method is not None:
                xml += '<method>%s</method>' % self._method.to_xml(client_context)
            if self._query is not None:
                xml += '<query>%s</query>' % self._query.to_xml(client_context)
            if self._header is not None:
                xml += '<header>%s</header>' % self._header.to_xml(client_context)
            if self._body is not None:
                xml += '<body>%s</body>' % self._body.to_xml(client_context)
        else:
            xml += '>'

        xml += self.children_to_xml(client_context)
        xml += '</sraix>'
        return xml

    #######################################################################################################
    # SRAIX_ATTRIBUTES ::= host="HOSTNAME" | botid="BOTID" | hint="TEXT" | apikey="APIKEY" | service="SERVICE"
    # SRAIX_ATTRIBUTE_TAGS ::= <host>TEMPLATE_EXPRESSION</host> | <botid>TEMPLATE_EXPRESSION</botid> |
    # <hint>TEMPLATE_EXPRESSION</hint> | <apikey>TEMPLATE_EXPRESSION</apikey> | <service>TEMPLATE_EXPRESSION</service>
    # SRAIX_EXPRESSION ::== <sraix( SRAIX_ATTRIBUTES)*>TEMPLATE_EXPRESSION</sraix> |

    def _parse_template_node(self, graph, child, name, add_shift):
        sub_node = TemplateSRAIXSubNode(name)
        base_node = graph.get_base_node()
        base_node.append(graph.get_word_node(name))
        sub_node.parse_text(graph, self.get_text_from_element(child))
        for sub_pattern in child:
            if add_shift is True:
                self._set_child_mark(graph, sub_node, self.SRAIX_CHILD_IN)
            graph.parse_tag_expression(sub_pattern, sub_node)
            if add_shift is True:
                self._set_child_mark(graph, sub_node, self.SRAIX_CHILD_OUT)
            tail_text = self.get_tail_from_element(sub_pattern)
            sub_node.parse_text(graph, tail_text)
        return sub_node

    def _set_child_mark(self, graph, child, shiftCode):
        word_class = graph.get_node_class_by_name('word')
        word_node = word_class(shiftCode)
        child.append(word_node)

    def parse_expression(self, graph, expression):
        mode_count = 0

        if 'host' in expression.attrib:
            self._botHost = expression.attrib['host']
        if 'method' in expression.attrib:
            YLogger.warning(self, "'method' attrib not supported in sraix, moved to config, see documentation")
        if 'query' in expression.attrib:
            YLogger.warning(self, "'query' attrib not supported in sraix, moved to config, see documentation")
        if 'header' in expression.attrib:
            YLogger.warning(self, "'header' attrib not supported in sraix, moved to config, see documentation")
        if 'body' in expression.attrib:
            YLogger.warning(self, "'body' attrib not supported in sraix, moved to config, see documentation")

        if 'botId' in expression.attrib:
            mode_count += 1
            self._botId = expression.attrib['botId']
        if 'apiKey' in expression.attrib:
            YLogger.warning(self, "'apiKey' attrib not supported in sraix, moved to config, see documentation")
        if 'locale' in expression.attrib:
            YLogger.warning(self, "'locale' attrib not supported in sraix, moved to config, see documentation")
        if 'time' in expression.attrib:
            YLogger.warning(self, "'time' attrib not supported in sraix, moved to config, see documentation")
        if 'userId' in expression.attrib:
            YLogger.warning(self, "'userId' attrib not supported in sraix, moved to config, see documentation")
        if 'topic' in expression.attrib:
            YLogger.warning(self, "'topic' attrib not supported in sraix, moved to config, see documentation")
        if 'deleteVariable' in expression.attrib:
            YLogger.warning(self, "'deleteVariable' attrib not supported in sraix, moved to config, see documentation")
        if 'metadata' in expression.attrib:
            YLogger.warning(self, "'metadata' attrib not supported in sraix, moved to config, see documentation")
        if 'config' in expression.attrib:
            YLogger.warning(self, "'config' attrib not supported in sraix, moved to config, see documentation")

        if 'service' in expression.attrib:
            mode_count += 1
            self._service = expression.attrib['service']

        if 'default' in expression.attrib:
            self._default = expression.attrib['default']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'host':
                mode_count += 1
                self._host = self._parse_template_node(graph, child, 'host', False)
            elif tag_name == 'method':
                self._method = self._parse_template_node(graph, child, 'method', False)
            elif tag_name == 'query':
                self._query = self._parse_template_node(graph, child, 'query', True)
            elif tag_name == 'header':
                self._header = self._parse_template_node(graph, child, 'header', True)
            elif tag_name == 'body':
                self._body = self._parse_template_node(graph, child, 'body', False)

            elif tag_name == 'botId':
                YLogger.warning(self, "'botId' element not supported in sraix, moved to config, see documentation")
            elif tag_name == 'apiKey':
                YLogger.warning(self, "'apiKey' element not supported in sraix, moved to config, see documentation")
            elif tag_name == 'locale':
                self._locale = self._parse_template_node(graph, child, 'locale', False)
            elif tag_name == 'time':
                self._time = self._parse_template_node(graph, child, 'time', False)
            elif tag_name == 'userId':
                self._userId = self._parse_template_node(graph, child, 'userId', False)
            elif tag_name == 'topic':
                self._topic = self._parse_template_node(graph, child, 'topic', False)
            elif tag_name == 'deleteVariable':
                self._deleteVariable = self._parse_template_node(graph, child, 'deleteVariable', False)
            elif tag_name == 'metadata':
                self._metadata = self._parse_template_node(graph, child, 'metadata', False)
            elif tag_name == 'config':
                self._config = self._parse_template_node(graph, child, 'config', True)

            elif tag_name == 'service':
                YLogger.warning(self, "'service' element not supported in sraix, moved to config, see documentation")

            elif tag_name == 'default':
                YLogger.warning(self, "'default' element not supported in sraix, moved to config, see documentation")

            else:
                graph.parse_tag_expression(child, self)

            tail_text = self.get_tail_from_element(child)
            self.parse_text(graph, tail_text)

        if mode_count == 0:
            raise ParserException("Missing type attribute or host element", xml_element=expression, nodename='sraix')
        elif mode_count > 1:
            raise ParserException("Node has Multiple type attribute or host element", xml_element=expression, nodename='sraix')
