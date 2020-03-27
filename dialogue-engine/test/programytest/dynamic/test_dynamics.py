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

from programy.dynamic.dynamics import DynamicsCollection
from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.dynamic import BrainDynamicsConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class DynamicsCollectionTests(unittest.TestCase):

    def test_init(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)
        self.assertIsNotNone(collection.dynamic_sets)
        self.assertIsNotNone(collection.dynamic_maps)
        self.assertIsNotNone(collection.dynamic_vars)

    def test_load_from_configuration_no_data(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamics_config = BrainDynamicsConfiguration()
        dynamics_config.load_config_section(yaml, brain_config, ".")

        collection.load_from_configuration(dynamics_config)

        self.assertIsNotNone(collection.dynamic_sets)
        self.assertTrue(collection.is_dynamic_set("NUMBER"))

        self.assertIsNotNone(collection.dynamic_maps)
        self.assertTrue(collection.is_dynamic_map("PLURAL"))
        self.assertTrue(collection.is_dynamic_map("SINGULAR"))
        self.assertTrue(collection.is_dynamic_map("PREDECESSOR"))
        self.assertTrue(collection.is_dynamic_map("SUCCESSOR"))

        self.assertIsNotNone(collection.dynamic_vars)

    def test_load_from_configuration(self):
        collection = DynamicsCollection()
        self.assertIsNotNone(collection)

        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            dynamic:
                variables:
                    gettime: programy.dynamic.variables.datetime.GetTime
                sets:
                    roman: programy.dynamic.sets.roman.IsRomanNumeral
                maps:
                    romantodec: programy.dynamic.maps.roman.MapRomanToDecimal
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")

        dynamics_config = BrainDynamicsConfiguration()
        dynamics_config.load_config_section(yaml, brain_config, ".")

        collection.load_from_configuration(dynamics_config)

        self.assertIsNotNone(collection.dynamic_sets)
        self.assertTrue(collection.is_dynamic_set("ROMAN"))
        self.assertTrue(collection.is_dynamic_set("NUMBER"))

        self.assertIsNotNone(collection.dynamic_maps)
        self.assertTrue(collection.is_dynamic_map("ROMANTODEC"))
        self.assertTrue(collection.is_dynamic_map("PLURAL"))
        self.assertTrue(collection.is_dynamic_map("SINGULAR"))
        self.assertTrue(collection.is_dynamic_map("PREDECESSOR"))
        self.assertTrue(collection.is_dynamic_map("SUCCESSOR"))

        self.assertIsNotNone(collection.dynamic_vars)
        self.assertTrue(collection.is_dynamic_var("GETTIME"))
