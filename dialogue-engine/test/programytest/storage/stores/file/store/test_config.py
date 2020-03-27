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

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.storage.stores.file.config import FileStoreConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class FileStoreConfigurationTests(unittest.TestCase):

    def test_with_files_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                sets:
                    dirs: $BOT_ROOT/sets
                    extension: .txt
                    subdirs: false
                    format: text
                    encoding: utf-8
                    delete_on_start: true
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        sets_config = FileStoreConfiguration("sets")
        sets_config.load_config_section(yaml, files_config, ".")

        self.assertFalse(sets_config.has_single_file())
        self.assertTrue(sets_config.has_multiple_dirs())

        self.assertEqual(["./sets"], sets_config.dirs)
        self.assertEqual(".txt", sets_config.extension)
        self.assertFalse(sets_config.subdirs)

        self.assertEqual("utf-8", sets_config.encoding)
        self.assertEqual("text", sets_config.format)

        self.assertTrue(sets_config.delete_on_start)

    def test_with_file_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            files:
                sets:
                    file: $BOT_ROOT/sets/test.txt
                    format: text
                    encoding: utf-8
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        files_config = yaml.get_section("files", brain_config)
        self.assertIsNotNone(files_config)

        sets_config = FileStoreConfiguration("sets")
        sets_config.load_config_section(yaml, files_config, ".")

        self.assertTrue(sets_config.has_single_file())
        self.assertFalse(sets_config.has_multiple_dirs())

        self.assertEqual(["./sets/test.txt"], sets_config.dirs)
        self.assertEqual("text", sets_config.format)
        self.assertEqual("utf-8", sets_config.encoding)
