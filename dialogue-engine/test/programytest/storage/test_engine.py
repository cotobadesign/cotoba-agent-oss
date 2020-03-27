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

from programy.storage.engine import StorageEngine


class StorageEngineTests(unittest.TestCase):

    def test_test_initialise_with_config_not_implemented(self):

        config = unittest.mock.Mock()

        engine = StorageEngine(config)
        self.assertIsNotNone(engine)
        self.assertIsNotNone(engine.configuration)
        self.assertEqual(engine.configuration, config)

    def test_user_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.user_store()

    def test_linked_account_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.linked_account_store()

    def test_link_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.link_store()

    def test_category_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.category_store()

    def test_errors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.errors_store()

    def test_duplicates_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.duplicates_store()

    def test_learnf_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.learnf_store()

    def test_conversation_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.conversation_store()

    def test_sets_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.sets_store()

    def test_maps_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.maps_store()

    def test_rdf_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.rdf_store()

    def test_denormal_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.denormal_store()

    def test_normal_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.normal_store()

    def test_gender_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.gender_store()

    def test_person_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.person_store()

    def test_person2_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.person2_store()

    def test_regex_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.regex_store()

    def test_property_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.property_store()

    def test_variables_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.variables_store()

    def test_twitter_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.twitter_store()

    def test_spelling_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.spelling_store()

    def test_license_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.license_store()

    def test_pattern_nodes_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.pattern_nodes_store()

    def test_template_nodes_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.template_nodes_store()

    def test_binaries_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.binaries_store()

    def test_braintree_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.braintree_store()

    def test_preprocessors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.preprocessors_store()

    def test_postprocessors_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.postprocessors_store()

    def test_usergroups_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.usergroups_store()

    def test_triggers_store_not_implemented(self):
        config = unittest.mock.Mock()
        engine = StorageEngine(config)
        with self.assertRaises(NotImplementedError):
            engine.triggers_store()
