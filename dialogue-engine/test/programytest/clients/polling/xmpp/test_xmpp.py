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
import unittest
import unittest.mock

from programy.clients.polling.xmpp.xmpp import XmppClient
from programy.clients.polling.xmpp.config import XmppConfiguration


class MockBotClient(object):

    def __init__(self):
        self._response = None

    def ask_question(self, userid, question):
        return self._response


class MockXmppClient(XmppClient):

    def __init__(self, bot_client, jid, password):
        self.registered = False
        self.server_url = None
        self.port_no = 0
        self.block = False
        self.event_handlers = []
        self.registered_plugins = []
        self.response = None
        self.userid = jid
        XmppClient.__init__(self, bot_client, jid, password)

    def add_event_handler(self, name, pointer):
        self.event_handlers.append(name)

    def register_xep_plugins(self, configuration):
        self.registered = True
        super(MockXmppClient, self).register_xep_plugins(configuration)

    def run(self, server, port, block=True):
        self.server_url = server
        self.port_no = port
        self.block = block

    def register_plugin(self, name):
        self.registered_plugins.append(name)

    def send_response(self, msg, response):
        self.response = response

    def get_userid(self, msg):
        return self.userid


class XmppClientTesst(unittest.TestCase):

    def test_xmpp_client_init(self):
        bot_client = MockBotClient()
        xmpp_client = MockXmppClient(bot_client, "userid", "password")
        self.assertIsNotNone(xmpp_client)
        self.assertTrue(bool("session_start" in xmpp_client.event_handlers))
        self.assertTrue(bool("message" in xmpp_client.event_handlers))

    def test_is_valid_message(self):
        bot_client = MockBotClient()
        xmpp_client = MockXmppClient(bot_client, "userid", "password")
        self.assertTrue(xmpp_client.is_valid_message({"type": "chat"}))
        self.assertTrue(xmpp_client.is_valid_message({"type": "normal"}))

    def test_get_question(self):
        bot_client = MockBotClient()
        xmpp_client = MockXmppClient(bot_client, "userid", "password")
        self.assertEqual("this is text", xmpp_client.get_question({"body": "this is text"}))

    def test_get_userid(self):
        bot_client = MockBotClient()
        xmpp_client = MockXmppClient(bot_client, "user123", "password")
        self.assertEqual("user123", xmpp_client.get_userid({"from": "user123"}))

    def test_register_plugins(self):
        bot_client = MockBotClient()
        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        client_configuration = XmppConfiguration()
        client_configuration._xep_0030 = True
        client_configuration._xep_0004 = True
        client_configuration._xep_0060 = True
        client_configuration._xep_0199 = True

        xmpp_client.register_xep_plugins(client_configuration)

        self.assertTrue(bool("xep_0030" in xmpp_client.registered_plugins))
        self.assertTrue(bool("xep_0004" in xmpp_client.registered_plugins))
        self.assertTrue(bool("xep_0060" in xmpp_client.registered_plugins))
        self.assertTrue(bool("xep_0199" in xmpp_client.registered_plugins))

    def test_message(self):
        bot_client = MockBotClient()
        bot_client._response = "Hiya"

        xmpp_client = MockXmppClient(bot_client, "userid", "password")

        xmpp_client.message({"type": "chat", "from": "user123", "body": "Hello"})
        self.assertIsNotNone(xmpp_client.response)
        self.assertEqual("Hiya", xmpp_client.response)
