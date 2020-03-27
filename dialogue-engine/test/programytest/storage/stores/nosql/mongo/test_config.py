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

from programy.storage.stores.nosql.mongo.config import MongoStorageConfiguration
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.clients.events.console.config import ConsoleConfiguration


class MongoStorgeConfigurationTests(unittest.TestCase):

    def test_initial_creation(self):
        config = MongoStorageConfiguration()
        self.assertIsNotNone(config)
        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, True)

    def test_initialise_with_config(self):

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
               mongo:
                    type:   mongo
                    config:
                        url: mongodb://localhost:27017/
                        database: programy
                        drop_all_first: true
                """, ConsoleConfiguration(), ".")

        mongo_config = yaml.get_section("mongo")

        config = MongoStorageConfiguration()
        config.load_config_section(yaml, mongo_config, ".")

        self.assertTrue(config.url.startswith('mongodb://localhost:'))
        self.assertEqual(config.database, "programy")
        self.assertEqual(config.drop_all_first, True)
