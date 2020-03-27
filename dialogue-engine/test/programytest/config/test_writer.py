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

from programy.config.writer import ConfigurationWriter


class MockConfigurationWriter(ConfigurationWriter):

    def __init__(self):
        self.written_data = None

    def write_yaml(self, filename, data):
        self.written_data = data


class ConfigurationWriterTests(unittest.TestCase):

    def test_execute_all_with_defaults(self):

        args = unittest.mock.Mock()
        args.clients = ['all']
        args.defaults = True

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)

    def test_execute_all_without_defaults(self):

        args = unittest.mock.Mock()
        args.clients = ['all']
        args.defaults = False

        writer = MockConfigurationWriter()
        writer.execute(args)

        self.assertIsNotNone(writer.written_data)
