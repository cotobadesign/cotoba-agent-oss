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


class TemplateSrNode(TemplateNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        conversation = client_context.bot.get_conversation(client_context)
        question = conversation.current_question()
        if question is not None:
            sentence = question.current_sentence()
            star = sentence.matched_context.star(1)
            if star is not None:
                try:
                    client_context.userInfo.userInfoPostProcessor(client_context)
                except Exception:
                    pass

                if conversation.internal_base is not None:
                    original_base = conversation.internal_base
                    base = original_base
                    if 'srai_histories' not in base:
                        base['srai_histories'] = []
                        srai_root = base['srai_histories']
                        srai_root.append({})
                        conversation.internal_base = srai_root[-1]

                resolved = client_context.bot.ask_question(client_context, star, srai=True)

                if conversation.internal_base is not None:
                    conversation.internal_base = original_base

                try:
                    client_context.userInfo.userInfoPreProcessor(client_context, True)
                except Exception:
                    pass

            else:
                YLogger.debug(client_context, "Sr node has no stars available")
                resolved = ""
        else:
            YLogger.debug(client_context, "Sr stars available (No question)")
            resolved = ""

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[SR]"

    def to_xml(self, client_context):
        xml = "<sr />"
        return xml

    #######################################################################################################
    # <sr/> |

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
        if self.children:
            raise ParserException("Node should not contain child text", xml_element=expression, nodename='sr')
