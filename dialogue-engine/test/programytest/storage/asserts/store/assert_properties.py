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


class PropertyStoreAsserts(unittest.TestCase):

    def assert_properties_storage(self, store):

        store.empty()

        properties = {"name1": "val1", "name2": "val2", "name3": "val3"}
        store.add_properties(properties)
        store.commit()

        new_properties = store.get_properties()
        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertTrue("name2" in new_properties)
        self.assertEqual("val2", new_properties["name2"])
        self.assertTrue("name3" in new_properties)
        self.assertEqual("val3", new_properties["name3"])
        self.assertFalse("name4" in new_properties)

        store.empty()
        new_properties = store.get_properties()
        self.assertEqual(0, len(new_properties.keys()))

    def assert_property_storage(self, store):

        store.empty()

        store.add_property("name1", "val1")

        new_properties = store.get_properties()

        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertFalse("name2" in new_properties)

        store.add_property("name2", "val2")
        store.commit()

        new_properties = store.get_properties()
        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        self.assertTrue("name2" in new_properties)
        self.assertEqual("val2", new_properties["name2"])
        self.assertFalse("name3" in new_properties)

    def assert_empty_properties(self, store):

        store.empty()

        store.add_property("name1", "val1")
        store.commit()

        store.add_property("name2", "val2")
        store.commit()

        new_properties = store.get_properties()
        self.assertTrue("name1" in new_properties)
        self.assertEqual("val1", new_properties["name1"])
        new_properties = store.get_properties()
        self.assertTrue("name2" in new_properties)
        self.assertEqual("val2", new_properties["name2"])

        store.empty_properties()

        new_properties = store.get_properties()
        self.assertFalse("name1" in new_properties)
