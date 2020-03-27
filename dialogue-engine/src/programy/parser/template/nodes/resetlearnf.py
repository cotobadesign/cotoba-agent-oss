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
from programy.storage.factory import StorageFactory
from programy.parser.template.nodes.resetlearn import TemplateResetLearnNode


class TemplateResetLearnfNode(TemplateResetLearnNode):

    def __init__(self):
        TemplateNode.__init__(self)

    def resolve_to_string(self, client_context):
        YLogger.debug(client_context, "Removing all learn nodes created by [%s]", client_context.userid)
        self._delete_category(client_context)
        self.delete_learnf(client_context)
        return ""

    def to_string(self):
        return "[RESETLEARNF]"

    def to_xml(self, client_context):
        return "<resetlearnf />"

    #######################################################################################################
    # RESETLEARNF_EXPRESSION ::== <resetlearnf />>

    def parse_expression(self, graph, expression):
        self._parse_node(graph, expression)
        if self.children:
            raise ParserException("Node should not contains child text", xml_element=expression, nodename='resetlearnf')

    def delete_learnf(self, client_context):

        if client_context.bot.client.storage_factory.entity_storage_engine_available(StorageFactory.LEARNF) is True:
            YLogger.debug(self, "Delete binary brain to [%s]", StorageFactory.LEARNF)

            storage_engine = client_context.bot.client.storage_factory.entity_storage_engine(StorageFactory.LEARNF)
            learnf_storage = storage_engine.learnf_store()
            learnf_storage.delete_learnf(client_context)
