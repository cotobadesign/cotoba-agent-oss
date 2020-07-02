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
import logging

from programy.utils.logging.ylogger import YLogger
from programy.utils.logging.ylogger import YLoggerSnapshot

from programytest.client import TestClient

from programy.config.bot.bot import BotConfiguration
from programy.bot import Bot
from programy.config.brain.brain import BrainConfiguration
from programy.brain import Brain
from programy.context import ClientContext


class YLoggerTests(unittest.TestCase):

    def setUp(self):
        YLogger.DEFAULT_LEVEL = None
        YLogger.IS_STDOUT = False
        YLogger.IS_STDERR = False

    def test_ylogger(self):
        client_context = ClientContext(TestClient(), "testid")

        snapshot = YLoggerSnapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(0) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.reset_snapshot()

        YLogger.critical(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(0) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.fatal(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(1) Error(0) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.error(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(0) Warning(0) Info(0), Debug(0)")

        YLogger.exception(client_context, "Test Message", Exception("Test error"))
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(0) Info(0), Debug(0)")

        YLogger.warning(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(1) Info(0), Debug(0)")

        YLogger.info(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(1) Info(1), Debug(0)")

        YLogger.debug(client_context, "Test Message")
        snapshot = YLogger.snapshot()
        self.assertIsNotNone(snapshot)
        self.assertEqual(str(snapshot), "Critical(1) Fatal(1) Error(1) Exception(1) Warning(1) Info(1), Debug(1)")

    def test_format_message_with_client(self):
        client = TestClient()

        msg = YLogger.format_message(client, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] - Test Message", msg)

    def test_format_message_with_client_and_bot(self):
        client = TestClient()

        config = BotConfiguration()
        config._section_name = "testbot"
        bot = Bot(config, client)

        msg = YLogger.format_message(bot, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] - Test Message", msg)

    def test_format_message_with_bot(self):
        config = BotConfiguration()
        config._section_name = "testbot"
        client = TestClient()
        bot = Bot(config, client)

        msg = YLogger.format_message(bot, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] - Test Message", msg)

    def test_format_message_with_client_and_bot_and_brain(self):
        client = TestClient()

        bot_config = BotConfiguration()
        bot_config._section_name = "testbot"
        bot = Bot(bot_config, client)

        brain_config = BrainConfiguration()
        brain_config._section_name = "testbrain"
        brain = Brain(bot, brain_config)

        msg = YLogger.format_message(brain, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] [testbrain] - Test Message", msg)

    def test_format_message_with_client_and_default_bot_and_brain(self):
        brain_config = BrainConfiguration()
        client = TestClient()
        context = client.create_client_context("testid")

        brain_config._section_name = "testbrain"
        brain = Brain(context.bot, brain_config)

        msg = YLogger.format_message(brain, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [bot] [testbrain] - Test Message", msg)

    def test_format_message_with_client_context(self):
        client = TestClient()

        bot_config = BotConfiguration()
        bot_config._section_name = "testbot"
        bot = Bot(bot_config, client)

        brain_config = BrainConfiguration()
        brain_config._section_name = "testbrain"
        brain = Brain(bot, brain_config)

        client_context = ClientContext(client, "testuser")
        client_context._bot = bot
        client_context._brain = brain

        msg = YLogger.format_message(client_context, "Test Message")
        self.assertIsNotNone(msg)
        self.assertEqual("[testclient] [testbot] [testbrain] [testuser] - Test Message", msg)

    def test_set_default_level(self):
        logging.getLogger().setLevel(level=logging.NOTSET)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'none')

        logging.getLogger().setLevel(level=logging.CRITICAL)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'error')
        logging.getLogger().setLevel(level=logging.FATAL)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'error')
        logging.getLogger().setLevel(level=logging.ERROR)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'error')

        logging.getLogger().setLevel(level=logging.WARNING)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'warning')

        logging.getLogger().setLevel(level=logging.INFO)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'info')

        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_default_level()
        self.assertEqual(YLogger.DEFAULT_LEVEL, 'debug')

    def test_check_loglevel_with_set_default(self):
        logging.getLogger().setLevel(level=logging.NOTSET)
        YLogger.set_default_level()
        self.assertFalse(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertFalse(YLogger.check_loglevel(None, logging.FATAL))
        self.assertFalse(YLogger.check_loglevel(None, logging.ERROR))
        self.assertFalse(YLogger.check_loglevel(None, logging.WARNING))
        self.assertFalse(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.ERROR)
        YLogger.set_default_level()
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertFalse(YLogger.check_loglevel(None, logging.WARNING))
        self.assertFalse(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.WARNING)
        YLogger.set_default_level()
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertFalse(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.INFO)
        YLogger.set_default_level()
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertTrue(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_default_level()
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertTrue(YLogger.check_loglevel(None, logging.INFO))
        self.assertTrue(YLogger.check_loglevel(None, logging.DEBUG))

    def test_check_loglevel_not_set_default(self):
        logging.getLogger().setLevel(level=logging.NOTSET)
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertTrue(YLogger.check_loglevel(None, logging.INFO))
        self.assertTrue(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.ERROR)
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertFalse(YLogger.check_loglevel(None, logging.WARNING))
        self.assertFalse(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.WARNING)
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertFalse(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.INFO)
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertTrue(YLogger.check_loglevel(None, logging.INFO))
        self.assertFalse(YLogger.check_loglevel(None, logging.DEBUG))

        logging.getLogger().setLevel(level=logging.DEBUG)
        self.assertTrue(YLogger.check_loglevel(None, logging.CRITICAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.FATAL))
        self.assertTrue(YLogger.check_loglevel(None, logging.ERROR))
        self.assertTrue(YLogger.check_loglevel(None, logging.WARNING))
        self.assertTrue(YLogger.check_loglevel(None, logging.INFO))
        self.assertTrue(YLogger.check_loglevel(None, logging.DEBUG))

    def test_check_loglevel_invalid_level(self):
        logging.getLogger().setLevel(level=logging.NOTSET)
        YLogger.set_default_level()
        self.assertFalse(YLogger.check_loglevel(None, 90))

    def test_check_loglevel_of_caller_level(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        client_context.log_level = "debug"

        logging.getLogger().setLevel(level=logging.ERROR)
        YLogger.set_default_level()
        self.assertTrue(YLogger.check_loglevel(client_context, logging.DEBUG))

    def test_check_log_not_output(self):
        logging.getLogger().setLevel(level=logging.NOTSET)
        YLogger.set_default_level()

        YLogger.critical(None, "Critical Log")
        YLogger.fatal(None, "Fatal Log")
        YLogger.error(None, "Error Log")
        YLogger.exception(None, "Exception Log", Exception("test"))
        YLogger.warning(None, "Warning Log")
        YLogger.info(None, "Info Log")
        YLogger.debug(None, "Debug Log")

    def test_set_stdout(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")

        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_stdout("True")

        YLogger.critical(client_context, "Critical Log")
        YLogger.fatal(client_context, "Fatal Log")
        YLogger.error(client_context, "Error Log")
        YLogger.exception(client_context, "Exception Log", Exception("test"))
        YLogger.warning(client_context, "Warning Log")
        YLogger.info(client_context, "Info Log")
        YLogger.debug(client_context, "Debug Log")

    def test_set_stdout_json(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")

        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_stdout("True")

        tmp_str = 'test'
        tmp_val = 99
        YLogger.debug(client_context, '{"key_a":"%s", "key_b": "%d"}', tmp_str, tmp_val)

        YLogger.debug(client_context, '{"key_a":"%s", "key_b": "%d"}')

        json_data1 = '{"key_a":"%s", "key_b": "%d"}' % (tmp_str, tmp_val)
        YLogger.debug(client_context, 'json_data : "%s"', json_data1)

        json_data2 = '{"key_a":"%s", "key_b": "%d"}'
        YLogger.debug(client_context, 'json_data : "%s"', json_data2)

    def test_exception_is_none_with_stdout(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_stdout("True")

        YLogger.exception(client_context, "Exception Log", None)

    def test_set_stderror(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")

        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_stderr("True")

        YLogger.critical(client_context, "Critical Log")
        YLogger.fatal(client_context, "Fatal Log")
        YLogger.error(client_context, "Error Log")
        YLogger.exception(client_context, "Exception Log", Exception("test"))
        YLogger.warning(client_context, "Warning Log")
        YLogger.info(client_context, "Info Log")
        YLogger.debug(client_context, "Debug Log")

    def test_set_stderror_json(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")

        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_stderr("True")

        tmp_str = 'test'
        tmp_val = 99
        YLogger.debug(client_context, '{"key_a":"%s", "key_b": "%d"}', tmp_str, tmp_val)

        YLogger.debug(client_context, '{"key_a":"%s", "key_b": "%d"}')

        json_data1 = '{"key_a":"%s", "key_b": "%d"}' % (tmp_str, tmp_val)
        YLogger.debug(client_context, 'json_data : "%s"', json_data1)

        json_data2 = '{"key_a":"%s", "key_b": "%d"}'
        YLogger.debug(client_context, 'json_data : "%s"', json_data2)

    def test_exception_is_none_with_stderror(self):
        client = TestClient()
        client_context = ClientContext(client, "testid")
        logging.getLogger().setLevel(level=logging.DEBUG)
        YLogger.set_stderr("True")

        YLogger.exception(client_context, "Exception Log", None)
