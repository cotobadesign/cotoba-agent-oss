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
import os.path
import re

from programy.mappings.person import PersonCollection


class PersonssStoreAsserts(unittest.TestCase):

    def assert_upload_from_file(self, store):
        person_collection = PersonCollection()

        store.upload_from_file(os.path.dirname(
            __file__) + os.sep + "data" + os.sep + "lookups" + os.sep + "text" + os.sep + "person.txt")

        store.load(person_collection)

        self.assertEqual(person_collection.person(" WITH YOU "),
                         [re.compile('(^WITH YOU | WITH YOU | WITH YOU$)', re.IGNORECASE), ' WITH ME2 '])
        self.assertEqual(person_collection.personalise_string("Is he with you"), "Is he with me2")
