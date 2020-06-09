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
from programy.storage.config import StorageConfiguration
from programy.clients.events.console.config import ConsoleConfiguration
from programy.storage.factory import StorageFactory


class StorageConfigurationTests(unittest.TestCase):

    def test_with_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            storage:
                entities:
                    users: sqlite
                    linked_accounts: sqlite
                    links: sqlite

                    categories: file
                    errors: file
                    duplicates: file
                    learnf: file

                    conversations: file

                    maps: file
                    sets: file
                    rdf: file

                    denormal: file
                    normal: file
                    gender: file
                    person: file
                    person2: file
                    regex_templates: file

                    properties: file
                    defaults: file

                    spelling_corpus: file

                    license_keys: file

                    template_nodes: file
                    pattern_nodes: file

                    binaries: file
                    braintree: file

                    preprocessors: file
                    postprocessors: file

                    usergroups: file

                    triggers: file

                stores:
                    sqlite:
                        type:   sql
                        config:
                            url: sqlite:///:memory
                            echo: false
                            encoding: utf-8
                            create_db: true
                            drop_all_first: true

                    mongo:
                        type:   mongo
                        config:
                            url: mongodb://localhost:27017/
                            database: programy
                            drop_all_first: true

                    redis:
                        type:   redis
                        config:
                            host: localhost
                            port: 6379
                            password: None
                            db: 0
                            prefix: programy
                            drop_all_first: True

                    file:
                        type:   file
                        config:
                            properties_storage:
                                file: ./storage/properties
                            conversations_storage:
                                dir: ./storage/conversations

                    logger:
                        type:   logger
                        config:
                            conversation_logger: conversation

        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        storage_config = StorageConfiguration()
        storage_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNotNone(storage_config.entity_store)
        self.assert_entity_store(storage_config)

        self.assertIsNotNone(storage_config.storage_configurations)
        self.assert_storage_configurations(storage_config)

    def test_with_no_data(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        console:
            storage:
        """, ConsoleConfiguration(), ".")

        bot_config = yaml.get_section("console")

        storage_config = StorageConfiguration()
        storage_config.load_config_section(yaml, bot_config, ".")

        self.assertIsNotNone(storage_config.entity_store)
        self.assert_entity_store(storage_config)

        self.assertIsNotNone(storage_config.storage_configurations)
        self.assert_storage_configurations(storage_config)

    def assert_entity_store(self, storage_config):

        self.assertEqual(storage_config.entity_store[StorageFactory.USERS], 'sqlite')
        self.assertEqual(storage_config.entity_store[StorageFactory.LINKED_ACCOUNTS], 'sqlite')
        self.assertEqual(storage_config.entity_store[StorageFactory.LINKS], 'sqlite')

        self.assertEqual(storage_config.entity_store[StorageFactory.CATEGORIES], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.ERRORS], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.DUPLICATES], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.LEARNF], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.CONVERSATIONS], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.MAPS], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.SETS], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.RDF], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.DENORMAL], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.NORMAL], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.GENDER], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.PERSON], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.PERSON2], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.REGEX_TEMPLATES], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.PROPERTIES], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.DEFAULTS], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.SPELLING_CORPUS], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.LICENSE_KEYS], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.TEMPLATE_NODES], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.PATTERN_NODES], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.BINARIES], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.BRAINTREE], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.PREPROCESSORS], 'file')
        self.assertEqual(storage_config.entity_store[StorageFactory.POSTPROCESSORS], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.USERGROUPS], 'file')

        self.assertEqual(storage_config.entity_store[StorageFactory.TRIGGERS], 'file')

    def assert_storage_configurations(self, storage_config):

        self.assertTrue('sqlite' in storage_config.storage_configurations)
        self.assertTrue('mongo' in storage_config.storage_configurations)
        self.assertTrue('redis' in storage_config.storage_configurations)
        self.assertTrue('file' in storage_config.storage_configurations)
        self.assertTrue('logger' in storage_config.storage_configurations)
