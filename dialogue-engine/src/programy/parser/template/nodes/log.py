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

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.attrib import TemplateAttribNode


class TemplateLogNode(TemplateAttribNode):

    def __init__(self):
        TemplateAttribNode.__init__(self)
        self._level = "info"

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, level):
        self._level = level

    def resolve_to_string(self, client_context):
        resolved = self.resolve_children_to_string(client_context)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)

        if client_context.server_mode is True:
            conversation = client_context.bot.get_conversation(client_context)
            log_msg = {self._level: resolved}
            conversation.append_log(log_msg)
        else:
            if self._level == "debug":
                YLogger.debug(client_context, resolved)
            elif self._level == "warning":
                YLogger.warning(client_context, resolved)
            elif self._level == "error":
                YLogger.error(client_context, resolved)
            elif self._level == "info":
                YLogger.info(client_context, resolved)
            else:
                YLogger.debug(client_context, resolved)

        return ""

    def to_string(self):
        return "[LOG level=%s]" % (self._level)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'level':
            raise ParserException("Invalid attribute name %s" % attrib_name, nodename='log')
        if attrib_value not in ['debug', 'info', 'warning', 'error']:
            raise ParserException("Invalid attribute value %s for attribute %s" % (attrib_value, attrib_name), nodename='log')
        self._level = attrib_value

    def to_xml(self, client_context):
        xml = "<log"
        if self._level is not None:
            xml += ' level="%s"' % self._level
        xml += ">"
        xml += self.children_to_xml(client_context)
        xml += "</log>"
        return xml

    #######################################################################################################
    # LOG_EXPRESSION ::== <log>Message</log>
    #                           <log level="error|warning|debug|info">Message</log>
    #

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "level", "info")
