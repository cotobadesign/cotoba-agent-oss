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
import xml.etree.ElementTree as ET

from programy.dialog.question import Question
from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.sraix import TemplateSRAIXNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.services.service import ServiceFactory
from programy.config.brain.brain import BrainConfiguration
from programy.config.brain.service import BrainServiceConfiguration
from programy.mappings.botnames import PublicBotInfo

from programytest.parser.base import ParserTestsBaseClass


class MockTemplateSRAIXNode(TemplateSRAIXNode):
    def __init__(self):
        TemplateSRAIXNode.__init__(self)

    def resolve_to_string(self, context):
        raise Exception("This is an error")


class TemplateSRAIXNodeTests(ParserTestsBaseClass):

    def set_collection_botnames(self):
        bot_info = PublicBotInfo("http://localhost/test", None)
        self._client_context.brain.botnames.add_botname("testbot", bot_info, "botnames.yaml", 0)

    def test_node_unsupported_attributes(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node.host = "http://somebot.org"
        node.botd = "1234567890"
        node.hint = "The usual"
        node.apikey = "ABCDEF"
        node.service = "api"

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[SRAIX (service=api)]", node.to_string())

    def test_node_GeneralRest(self):
        ServiceFactory.clear()

        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node._default = "unknown"

        node._host = TemplateWordNode("hostname")
        node._method = TemplateWordNode("POST")
        node._query = TemplateWordNode('"userid":"1234567890"')
        node._header = TemplateWordNode('"Content-Type":"application/json"')
        node._body = TemplateWordNode("Hello")

        self.assertEqual("hostname", node._host.word)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        self.assertEqual('[SRAIX (host=hostname, default=unknown, method=POST, ' +
                         'query={"userid":"1234567890"}, header={"Content-Type":"application/json"}, ' +
                         'body=Hello)]', node.to_string())

    def test_node_PublishedBot(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node._botName = "testbot"
        node._default = "unknown"

        node._locale = TemplateWordNode("ja-JP")
        node._time = TemplateWordNode("2019-01-01T00:00:00+09:00")
        node._userId = TemplateWordNode("1234567890")
        node._topic = TemplateWordNode("*")
        node._deleteVariable = TemplateWordNode("false")
        node._metadata = TemplateWordNode("1234567890")
        node._config = TemplateWordNode('{"config":{"logLevel":"debug"}}')
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("testbot", node.botName)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        self.assertEqual('[SRAIX (botName=testbot, default=unknown, locale=ja-JP, ' +
                         'time=2019-01-01T00:00:00+09:00, userId=1234567890, topic=*, ' +
                         'deleteVariable=false, metadata=1234567890, ' +
                         'config={"config":{"logLevel":"debug"}})]', node.to_string())

    def test_node_CustomService(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)
        node.service = "api"
        node._default = "unknown"

        self.assertEqual("api", node.service)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        self.assertEqual("[SRAIX (service=api, default=unknown)]", node.to_string())

    def test_node_no_service(self):
        root = TemplateNode()
        self.assertIsNotNone(root)
        self.assertIsNotNone(root.children)
        self.assertEqual(len(root.children), 0)

        node = TemplateSRAIXNode()
        self.assertIsNotNone(node)

        root.append(node)
        self.assertEqual(len(root.children), 1)

        self.assertEqual("[SRAIX ()]", node.to_string())

    def test_to_xml_GeneralRest(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()
        node._default = "unknown"
        root.append(node)

        node._host = TemplateWordNode("hostname")
        node._method = TemplateWordNode("POST")
        node._query = TemplateWordNode('"userid":"1234567890"')
        node._header = TemplateWordNode('"Content-Type":"application/json"')
        node._body = TemplateWordNode("Hello")

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix default="unknown"><host>hostname</host><method>POST</method><query>"userid":"1234567890"</query>' +
                         '<header>"Content-Type":"application/json"</header><body>Hello</body>' +
                         '</sraix></template>', xml_str)

    def test_to_xml_GeneralRest_only_host(self):
        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._host = TemplateWordNode("hostname")
        root.append(node)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix><host>hostname</host></sraix></template>', xml_str)

    def test_to_xml_PublishedBot(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._default = "unknown"
        root.append(node)

        node._locale = TemplateWordNode("ja-JP")
        node._time = TemplateWordNode("2019-01-01T00:00:00+09:00")
        node._userId = TemplateWordNode("1234567890")
        node._topic = TemplateWordNode("*")
        node._deleteVariable = TemplateWordNode("false")
        node._metadata = TemplateWordNode("1234567890")
        node._config = TemplateWordNode('{"config":{"logLevel":"debug"}}')
        node.append(TemplateWordNode("Hello"))

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix botName="testbot" default="unknown">' +
                         '<locale>ja-JP</locale><time>2019-01-01T00:00:00+09:00</time><userId>1234567890</userId>' +
                         '<topic>*</topic><deleteVariable>false</deleteVariable><metadata>1234567890</metadata>' +
                         '<config>{"config":{"logLevel":"debug"}}</config>Hello</sraix></template>',
                         xml_str)

    def test_to_xml_PublishedBot_only_botNmae(self):
        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode("1234567890")
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix botName="testbot"><userId>1234567890</userId>Hello</sraix></template>', xml_str)

    def test_to_xml_CustomService(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "api"
        node._default = "unknown"

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix default="unknown" service="api">Hello</sraix></template>', xml_str)

    def test_to_xml_CustomService_only_service(self):
        root = TemplateNode()
        node = TemplateSRAIXNode()
        node.service = "api"
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        with self.assertRaises(Exception):
            node.resolve_to_string(self._client_context)

        xml = root.xml_tree(self._client_context)
        self.assertIsNotNone(xml)
        xml_str = ET.tostring(xml, "utf-8").decode("utf-8")
        self.assertEqual('<template><sraix service="api">Hello</sraix></template>', xml_str)

    def test_to_xml_no_service(self):
        root = TemplateNode()

        node = TemplateSRAIXNode()

        root.append(node)
        node.append(TemplateWordNode("Hello"))

        result = node.resolve_to_string(self._client_context)
        self.assertEqual('', result)

    def test_call_GeneralRest(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDREST__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDREST__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._host = TemplateWordNode("hostname")
        node._method = TemplateWordNode("POST")
        node._query = TemplateWordNode('"userid":"1234567890"')
        node._header = TemplateWordNode('"Content-Type":"application/json"')
        node._body = TemplateWordNode("Hello")
        root.append(node)

        self.assertEqual("asked", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("asked", node.resolve(self._client_context))
        self.assertEqual("asked", question.property('__SUBAGENT_BODY__'))

    def test_call_GeneralRest_only_host(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDREST__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDREST__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._host = TemplateWordNode("hostname")
        root.append(node)

        self.assertEqual("asked", node.resolve(self._client_context))

    def test_call_GeneralRest_response_none(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDREST__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDREST__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._host = TemplateWordNode("hostname")
        root.append(node)

        service = ServiceFactory.get_service("__PUBLISHEDREST__")
        service.set_response(None)

        self.assertIsNone(node.resolve(self._client_context))

    def test_call_GeneralRest_response_empty(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDREST__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDREST__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._host = TemplateWordNode("hostname")
        root.append(node)

        service = ServiceFactory.get_service("__PUBLISHEDREST__")
        service.set_response("")

        self.assertEqual("", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("", node.resolve(self._client_context))

    def test_call_GeneralRest_response_default(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDREST__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDREST__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._host = TemplateWordNode("hostname")
        node._default = "unknown"
        root.append(node)

        service = ServiceFactory.get_service("__PUBLISHEDREST__")
        service.set_response("")

        self.assertEqual("unknown", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("unknown", node.resolve(self._client_context))
        self.assertEqual("unknown", question.property('__SUBAGENT_BODY__'))

    def test_call_PublishedBot(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._locale = TemplateWordNode('ja-JP')
        node._time = TemplateWordNode('2019-01-01T00:00:00+09:00')
        node._userId = TemplateWordNode('1234567890')
        node._topic = TemplateWordNode('*')
        node._deleteVariable = TemplateWordNode('false')
        node._metadata = TemplateWordNode('1234567890')
        node._config = TemplateWordNode('{"config":{"logLevel":"debug"}}')
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        self.set_collection_botnames()
        self.assertEqual("asked", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        service = ServiceFactory.get_service("__PUBLISHEDBOT__")
        service.set_response('{"response": "asked"}')

        self.assertEqual("asked", node.resolve(self._client_context))
        self.assertEqual('{"testbot": {"response": "asked"}}', question.property('__SUBAGENT_EXTBOT__'))

    def test_call_PublishedBot_only_botname(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config

        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()

        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode('1234567890')
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.set_collection_botnames()
        self.assertEqual("asked", node.resolve(self._client_context))

    def test_call_PublishedBot_topic(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config

        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode('1234567890')
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        conversation = self._client_context.bot.get_conversation(self._client_context)
        conversation.set_property('topic', 'morning')

        self.set_collection_botnames()
        self.assertEqual("asked", node.resolve(self._client_context))

        node._topic = TemplateWordNode("evening")
        self.assertEqual("asked", node.resolve(self._client_context))

    def test_call_PublishedBot_deleteValiables(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode('1234567890')
        node._deleteVariable = TemplateWordNode('true')
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        self.set_collection_botnames()
        self.assertEqual("asked", node.resolve(self._client_context))

    def test_call_PublishedBot_response_none(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode('1234567890')
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        service = ServiceFactory.get_service("__PUBLISHEDBOT__")
        service.set_response(None)

        self.set_collection_botnames()
        self.assertIsNone(node.resolve(self._client_context))

    def test_call_PublishedBot_response_empty(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode('1234567890')
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        service = ServiceFactory.get_service("__PUBLISHEDBOT__")
        service.set_response("")

        self.set_collection_botnames()
        self.assertEqual("", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("", node.resolve(self._client_context))

    def test_call_PublishedBot_response_default(self):
        service_config = BrainServiceConfiguration("__PUBLISHEDBOT__")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['__PUBLISHEDBOT__'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._botName = "testbot"
        node._userId = TemplateWordNode('1234567890')
        node._default = "unknown"
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        service = ServiceFactory.get_service("__PUBLISHEDBOT__")
        service.set_response("")

        self.set_collection_botnames()
        self.assertEqual("unknown", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("unknown", node.resolve(self._client_context))
        self.assertEqual("unknown", question.property('__SUBAGENT_EXTBOT__.testbot'))

    def test_call_CustomService(self):
        service_config = BrainServiceConfiguration("mock")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['mock'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._service = "mock"
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        self.assertEqual("asked", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("asked", node.resolve(self._client_context))
        self.assertEqual('asked', question.property('__SUBAGENT__.mock'))

    def test_call_CustomService_response_none(self):
        service_config = BrainServiceConfiguration("mock")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['mock'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._service = "mock"
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        service = ServiceFactory.get_service("mock")
        service.set_response(None)

        self.assertEqual(None, node.resolve(self._client_context))

    def test_call_CustomService_response_empty(self):
        service_config = BrainServiceConfiguration("mock")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['mock'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._service = "mock"
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        service = ServiceFactory.get_service("mock")
        service.set_response("")

        self.assertEqual("", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("", node.resolve(self._client_context))

    def test_call_CustomService_response_default(self):
        service_config = BrainServiceConfiguration("mock")
        service_config._classname = 'programytest.services.test_service.MockService'
        brain_config = BrainConfiguration()
        brain_config.services._services['mock'] = service_config
        ServiceFactory.preload_services(brain_config.services)

        root = TemplateNode()
        node = TemplateSRAIXNode()
        node._service = "mock"
        node._default = "unknown"
        node.append(TemplateWordNode("Hello"))
        root.append(node)

        service = ServiceFactory.get_service("mock")
        service.set_response("")

        self.assertEqual("unknown", node.resolve(self._client_context))

        conversation = self._client_context.bot.get_conversation(self._client_context)
        self.assertIsNotNone(conversation)
        question = Question.create_from_text(self._client_context, "Hello", self._client_context.bot.sentence_splitter)
        conversation.record_dialog(question)
        self.assertIsNotNone(conversation.current_question())

        self.assertEqual("unknown", node.resolve(self._client_context))
        self.assertEqual("unknown", question.property('__SUBAGENT__.mock'))

    def test_call_no_CustomService_exists(self):

        root = TemplateNode()

        node = TemplateSRAIXNode()
        node.service = "mock1"
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        with self.assertRaises(Exception):
            node.resolve(self._client_context)

    def test_call_no_service_defined(self):

        root = TemplateNode()

        node = TemplateSRAIXNode()
        root.append(node)
        node.append(TemplateWordNode("Hello"))

        self.assertEqual("", node.resolve(self._client_context))

    def test_node_exception_handling(self):
        root = TemplateNode()
        node = MockTemplateSRAIXNode()
        root.append(node)

        with self.assertRaises(Exception):
            root.resolve(self._client_context)
