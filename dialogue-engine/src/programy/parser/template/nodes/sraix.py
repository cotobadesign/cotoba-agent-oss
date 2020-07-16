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
import copy

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.services.service import ServiceFactory
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
from programy.mappings.resttemplates import RestParameters


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

        self._template = None
        self._host = None
        self._method = None
        self._query = None
        self._header = None
        self._body = None

        self._botName = None
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
    def botName(self):
        return self._botName

    @property
    def template(self):
        return self._template

    @property
    def service(self):
        return self._service

    @property
    def default(self):
        return self._default

    @botName.setter
    def botName(self, botName):
        self._botName = botName

    @template.setter
    def template(self, template):
        self._template = template

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
        self.host = None
        self.method = None
        self.query = None
        self.header = None
        self.body = None

        if self._host is not None:
            self.host = self._host.resolve(client_context)
        if self._method is not None:
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

        error_msg = None
        if self._template is None:
            exec_params = RestParameters(self.host)
            if exec_params.host is None:
                error_msg = "sraix subagent-rest : invalid host parameter [%s]" % self.host
            if error_msg is None and self.body is not None:
                exec_params.set_body(self.body)
            if error_msg is None and self.method is not None:
                if exec_params.set_method(self.method) is False:
                    error_msg = "sraix subagent-rest : invalid method parameter [%s]" % self.method
            if error_msg is None and self.query is not None:
                if exec_params.set_query(self.query) is False:
                    error_msg = "sraix subagent-rest : invalid query parameter [%s]" % self.query
            if error_msg is None and self.header is not None:
                if exec_params.set_header(self.header) is False:
                    error_msg = "sraix subagent-rest : invalid locale parameter [%s]" % self.header
        else:
            restParams = client_context.brain.rest_templates.rest_template(self._template)
            if restParams is None:
                error_msg = "sraix subagent-rest : REST-Template[%s] not found" % self._template
                YLogger.debug(client_context, error_msg)
                raise Exception(error_msg)

            exec_params = copy.copy(restParams)
            if self.host is not None:
                if exec_params.change_host(self.host) is False:
                    error_msg = "sraix subagent-rest : invalid host parameter [%s]" % self.host
            if error_msg is None and self.body is not None:
                exec_params.join_body(self.body)
            if error_msg is None and self.method is not None:
                if exec_params.set_method(self.method) is False:
                    error_msg = "sraix subagent-rest : invalid method parameter [%s]" % self.method
            if error_msg is None and self.query is not None:
                if exec_params.join_query(self.query) is False:
                    error_msg = "sraix subagent-rest : invalid query parameter [%s]" % self.query
            if error_msg is None and self.header is not None:
                if exec_params.join_header(self.header) is False:
                    error_msg = "sraix subagent-rest : invalid header parameter [%s]" % self.header

        if error_msg is not None:
            YLogger.debug(client_context, error_msg)
            raise Exception(error_msg)

        rest_service = ServiceFactory.get_service(self.SERVICE_PUBLISHED_REST)
        rest_service.params = exec_params
        response = rest_service.ask_question(client_context, resolved)
        YLogger.debug(client_context, "SRAIX host [%s] return [%s]", exec_params.host, response)

        conversation = client_context.bot.get_conversation(client_context)
        status_code = ''
        try:
            status_code = rest_service.get_status_code()
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

        if self._userId is not None:
            self.userId = self._userId.resolve(client_context)
        if self._locale is not None:
            self.locale = self._locale.resolve(client_context)
        if self._time is not None:
            self.time = self._time.resolve(client_context)
        if self._topic is not None:
            self.topic = self._topic.resolve(client_context)
        if self._deleteVariable is not None:
            self.deleteVariable = self._deleteVariable.resolve(client_context)
        if self._config is not None:
            shift_text = self._config.resolve(client_context)
            self.config = self._delete_shift_code(shift_text)
        if self._metadata is not None:
            self.metadata = self._metadata.resolve(client_context)

        bot_service = ServiceFactory.get_service(self.SERVICE_PUBLISHED_BOT)

        botInfo = client_context.brain.botnames.botInfo(self.botName)
        if botInfo is None:
            error_msg = "sraix subagent-bot : botName[%s] not found" % self.botName
            YLogger.debug(client_context, error_msg)
            raise Exception(error_msg)

        conversation = client_context.bot.get_conversation(client_context)
        exec_botInfo = copy.copy(botInfo)

        error_msg = None
        if self.userId is None or self.userId == '':
            self.userId = conversation.current_question().property('__USER_USERID__')
        if self.userId is None or self.userId == '':
            error_msg = "sraix subagent-bot : no userId parameter"
        if error_msg is None and self.locale is not None:
            if exec_botInfo.set_locale(self.locale) is False:
                error_msg = "sraix subagent-bot : invalid locale parameter [%s]" % self.locale
        if error_msg is None and self.time is not None:
            if exec_botInfo.set_time(self.time) is False:
                error_msg = "sraix subagent-bot : invalid time parameter [%s]" % self.time
        if error_msg is None and self.topic is not None:
            if exec_botInfo.set_topic(self.topic) is False:
                error_msg = "sraix subagent-bot : invalid topic parameter [%s]" % self.topic
        if error_msg is None and self.deleteVariable is not None:
            if exec_botInfo.set_deleteVariable(self.deleteVariable) is False:
                error_msg = "sraix subagent-bot : invalid deleteVariable parameter [%s]" % self.deleteVariable
        if error_msg is None and self.config is not None:
            if exec_botInfo.set_config(self.config) is False:
                error_msg = "sraix subagent-bot : invalid config parameter [%s]" % self.config
        if error_msg is None and self.metadata is not None:
            if exec_botInfo.join_metadata(self.metadata) is False:
                error_msg = "sraix subagent-bot : invalid metadata parameter [%s]" % self.metadata

        if error_msg is not None:
            YLogger.debug(client_context, error_msg)
            raise Exception(error_msg)

        resolved = self.resolve_children_to_string(client_context)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        bot_service.botInfo = exec_botInfo
        bot_service.userId = self.userId
        response = bot_service.ask_question(client_context, resolved)
        YLogger.debug(client_context, "SRAIX botName [%s] return [%s]", self._botName, response)

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
                        save_dic = {self._botName: response_dic}
                        conversation.current_question().set_property(variableName, json.dumps(save_dic, ensure_ascii=False))
                        response_data = response_dic['response']
                        if type(response_data) is dict:
                            response = json.dumps(response_data, ensure_ascii=False)
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
                    variableName += ".%s" % self._botName
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

        elif self._botName is not None:
            response = self._published_Bot_interface(client_context)
            return response

        elif self._host is not None or self._template is not None:
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
        elif self._botName is not None:
            texts = "[SRAIX (botName=%s" % self.botName
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
        elif self._template is not None or self._host is not None:
            texts = "[SRAIX ("
            if self._template is not None:
                texts += "template=%s" % self.template
                if self._host is not None:
                    texts += ", host=%s" % self.host
            else:
                texts += "host=%s" % self.host
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
        elif self._botName is not None:
            xml += ' botName="%s"' % self._botName
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
        elif self._template is not None or self._host is not None:
            if self._template is not None:
                xml += ' template="%s"' % self.template
            if self._default is not None:
                xml += ' default="%s"' % self._default
            xml += '>'
            if self._host is not None:
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
    # SRAIX_ATTRIBUTES ::= host="HOSTNAME" | botName="BOTNAME" | hint="TEXT" | apikey="APIKEY" | service="SERVICE"
    # SRAIX_ATTRIBUTE_TAGS ::= <host>TEMPLATE_EXPRESSION</host> | <botName>TEMPLATE_EXPRESSION</botName> |
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

        if 'template' in expression.attrib:
            template = expression.attrib['template']
            if graph.aiml_parser.brain.rest_templates.rest_template(template) is None:
                raise ParserException("REST=Template[%s] not found" % template, xml_element=expression, nodename='sraix')
            mode_count += 1
            self._template = template
        if 'method' in expression.attrib:
            YLogger.warning(self, "'method' attrib not supported in sraix, moved to config, see documentation")
        if 'query' in expression.attrib:
            YLogger.warning(self, "'query' attrib not supported in sraix, moved to config, see documentation")
        if 'header' in expression.attrib:
            YLogger.warning(self, "'header' attrib not supported in sraix, moved to config, see documentation")
        if 'body' in expression.attrib:
            YLogger.warning(self, "'body' attrib not supported in sraix, moved to config, see documentation")

        if 'botName' in expression.attrib:
            bot_name = expression.attrib['botName']
            if graph.aiml_parser.brain.botnames.botInfo(bot_name) is None:
                raise ParserException("BotName[%s] not found" % bot_name, xml_element=expression, nodename='sraix')
            mode_count += 1
            self._botName = bot_name
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
            service_name = expression.attrib['service']
            if ServiceFactory.service_exists(service_name) is False:
                raise ParserException("Service[%s] not found" % service_name, xml_element=expression, nodename='sraix')
            mode_count += 1
            self._service = service_name

        if 'default' in expression.attrib:
            self._default = expression.attrib['default']

        head_text = self.get_text_from_element(expression)
        self.parse_text(graph, head_text)

        for child in expression:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'host':
                if self._template is None or self._host is not None:
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

            elif tag_name == 'botName':
                YLogger.warning(self, "'botName' element not supported in sraix, moved to config, see documentation")
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
