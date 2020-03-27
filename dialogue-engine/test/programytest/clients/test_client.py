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
import os

from programy.clients.client import BotClient
from programy.clients.client import DefaultBotSelector
from programy.clients.client import BotFactory
from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot

from programy.clients.config import ClientConfigurationData

from programytest.clients.arguments import MockArgumentParser


class MockClientConfiguration(ClientConfigurationData):

    def __init__(self):
        ClientConfigurationData.__init__(self, "mock")


class MockBotClient(BotClient):

    def __init__(self, argument_parser=None):
        BotClient.__init__(self, "mock", argument_parser)

    def get_description(self):
        return "ProgramY Test Client"

    def set_environment(self):
        self._bot_factory.select_bot().brain.properties.add_property("env", "Mock")

    def get_client_configuration(self):
        return MockClientConfiguration()

    def run(self):
        """For testing purposes we do nothing"""
        return


class DefaultBotSelectorTests(unittest.TestCase):

    def test_init(self):
        configuration = unittest.mock.Mock()

        selector = DefaultBotSelector(configuration)
        self.assertIsNotNone(selector)

        bot1 = unittest.mock.Mock()
        bot2 = unittest.mock.Mock()

        bots = {"one": bot1, "two": bot2}
        self.assertEqual(bot1, selector.select_bot(bots))


class BotFactoryTests(unittest.TestCase):

    def test_empty_config_init(self):
        arguments = MockArgumentParser()
        client = MockBotClient(arguments)

        configuration = unittest.mock.Mock()

        configuration.configurations = []

        configuration.bot_selector = "programy.clients.client.DefaultBotSelector"

        factory = BotFactory(client, configuration)
        self.assertIsNotNone(factory)

        bot = factory.select_bot()
        self.assertIsNone(bot)

    def test_config_init(self):
        arguments = MockArgumentParser()
        client = MockBotClient(arguments)

        configuration = unittest.mock.Mock()

        configuration.configurations = [BotConfiguration()]

        configuration.bot_selector = "programy.clients.client.DefaultBotSelector"

        factory = BotFactory(client, configuration)
        self.assertIsNotNone(factory)

        bot = factory.select_bot()
        self.assertIsNotNone(bot)
        self.assertIsInstance(bot, Bot)


class BotClientTests(unittest.TestCase):

    def test_client_init(self):
        arguments = MockArgumentParser()
        with self.assertRaises(Exception):
            BotClient("test", arguments)

    def get_config_files(self):
        if os.name == 'posix':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.yaml"
            self.assertTrue(os.path.exists(logging_file))
            config_file = os.path.dirname(__file__) + os.sep + "config.yaml"
            self.assertTrue(os.path.exists(config_file))
        elif os.name == 'nt':
            logging_file = os.path.dirname(__file__) + os.sep + "logging.windows.yaml"
            self.assertTrue(os.path.exists(logging_file))
            config_file = os.path.dirname(__file__) + os.sep + "config.windows.yaml"
            self.assertTrue(os.path.exists(config_file))
        else:
            raise Exception("Unknown os [%s]" % os.name)

        return config_file, logging_file

    def get_commandline_args(self, config_file=None, logging_file=None):
        return MockArgumentParser(bot_root=None,
                                  logging=logging_file,
                                  config=config_file,
                                  cformat="yaml",
                                  noloop=False)

    def test_sub_classed_client(self):

        _, logging_file = self.get_config_files()

        arguments = self.get_commandline_args(None, logging_file)

        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

        self.assertIsNotNone(client.arguments)
        self.assertEqual("ProgramY Test Client", client.get_description())

        client.run()
        client.log_response(None, None)
        client.log_unknown_response(None)

    def test_sub_classed_client_no_bot_root(self):

        config_file, logging_file = self.get_config_files()

        arguments = self.get_commandline_args(config_file, logging_file)

        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

    def test_sub_classed_client_no_bot_root_no_config(self):

        _, logging_file = self.get_config_files()

        arguments = self.get_commandline_args(None, logging_file)

        client = MockBotClient(arguments)
        self.assertIsNotNone(client)
        self.assertIsNotNone(client.arguments)

    def test_scheduler(self):

        config_file, logging_file = self.get_config_files()

        arguments = self.get_commandline_args(config_file, logging_file)

        client = MockBotClient(arguments)

        self.assertIsNotNone(client.scheduler)

    def test_trigger_manager(self):

        config_file, logging_file = self.get_config_files()

        arguments = self.get_commandline_args(config_file, logging_file)

        client = MockBotClient(arguments)

        self.assertIsNotNone(client.trigger_manager)

        client.startup()
        client.shutdown()
