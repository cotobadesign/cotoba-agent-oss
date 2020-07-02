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
import os

from programy.clients.args import ClientArguments
from programy.clients.args import CommandLineClientArguments


class MockArguments(object):

    def __init__(self,
                 bot_root=".",
                 logging="logging.yaml",
                 config="config.yaml",
                 cformat="yaml",
                 noloop=False,
                 substitutions='subs.txt',
                 stdoutlog=False,
                 stderrlog=False
                 ):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop
        self.substitutions = substitutions
        self.stdoutlog = stdoutlog
        self.stderrlog = stderrlog


class MockArgumentParser(object):

    def add_argument(self, argument, dest=None, action=None, help=None, default=False):
        pass

    def parse_args(self):
        return MockArguments()


class MockClient(object):

    def get_description(self):
        return "MockClient"

    def add_client_arguments(self, parser):
        pass

    def parse_args(self, arguments, parsed_args):
        pass


class ClientArgumentsTests(unittest.TestCase):

    def test_init(self):
        client = MockClient()
        args = ClientArguments(client)
        self.assertIsNotNone(args)

        args.parse_args(client)

        self.assertIsNotNone(args.bot_root)
        self.assertIsNotNone(args.logging)
        self.assertIsNotNone(args.config_filename)
        self.assertIsNotNone(args.config_format)
        self.assertIsNotNone(args.noloop)
        self.assertIsNone(args.substitutions)
        self.assertIsNotNone(args.stdoutlog)
        self.assertIsNotNone(args.stderrlog)

        args.bot_root = os.sep + "tmp"
        self.assertIsNotNone(args.bot_root)
        self.assertEqual(os.sep + "tmp", args.bot_root)


class CommandLineClientArgumentsTests(unittest.TestCase):

    def test_init_mock_parser(self):
        client = MockClient()
        args = CommandLineClientArguments(client=client, parser=MockArgumentParser())
        self.assertIsNotNone(args)

        args.parse_args(client)

        self.assertEqual(args._bot_root, ".")
        self.assertEqual(args._logging, "logging.yaml")
        self.assertEqual(args._config_name, "config.yaml")
        self.assertEqual(args._config_format, "yaml")
        self.assertEqual(args._no_loop, False)
        self.assertEqual(args._substitutions, "subs.txt")
        self.assertEqual(args._stdoutlog, False)
        self.assertEqual(args._stderrlog, False)

    def test_init_command_line_parser(self):
        args = CommandLineClientArguments(client=MockClient())
        self.assertIsNotNone(args)

        self.assertIsNotNone(args._bot_root)
        self.assertIsNotNone(args._logging)
        self.assertIsNotNone(args._config_name)
        self.assertIsNotNone(args._config_format)
        self.assertIsNotNone(args._no_loop)
        self.assertIsNone(args.substitutions)
        self.assertIsNotNone(args.stdoutlog)
        self.assertIsNotNone(args.stderrlog)
