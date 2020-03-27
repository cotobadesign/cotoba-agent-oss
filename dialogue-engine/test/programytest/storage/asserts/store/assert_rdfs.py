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

from programy.rdf.collection import RDFCollection
from programy.storage.entities.store import Store


class RDFStoreAsserts(unittest.TestCase):

    def assert_rdf_storage(self, store):

        store.empty()

        store.add_rdf("ACTIVITY", "ACT", "hasPurpose", "to entertain by performing")
        store.add_rdf("ACTIVITY", "ACT", "hasSize", "0")
        store.add_rdf("ACTIVITY", "ACT", "hasSyllables", "1")
        store.add_rdf("ACTIVITY", "ACT", "isa", "Activity0")
        store.add_rdf("ACTIVITY", "ACT", "lifeArea", "Recreation")
        store.commit()

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_from_text(self, store):

        store.empty()

        store.upload_from_text("ACTIVITY", """
            ACT:hasPurpose:to entertain by performing
            ACT:hasSize:0
            ACT:hasSyllables:1
            ACT:isa:Activity
            ACT:lifeArea:Recreation
            ADVENTURE:hasPurpose:to provide new experience
            ADVENTURE:hasSize:0
            ADVENTURE:hasSyllables:3
            ADVENTURE:isa:Activity
            ADVENTURE:lifeArea:Recreation
            FISHING:hasPurpose:to hunt for fish
            FISHING:hasSize:0
            FISHING:hasSyllables:2
            FISHING:isa:Activity
            FISHING:lifeArea:Recreation
            """)

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_from_text_file(self, store):
        store.empty()

        store.upload_from_file(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"text"+os.sep+"activity.rdf")

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_text_files_from_directory_no_subdir(self, store):

        store.empty()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"text", subdir=False)

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_from_csv_file(self, store):

        store.empty()

        store.upload_from_file(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"csv"+os.sep+"activity.csv", format=Store.CSV_FORMAT)

        rdf_collection = RDFCollection()
        store.load(rdf_collection, "ACTIVITY")

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

    def assert_upload_csv_files_from_directory_with_subdir(self, store):

        store.empty()

        store.upload_from_directory(os.path.dirname(__file__)+os.sep+"data"+os.sep+"rdfs"+os.sep+"csv", subdir=True, format=Store.CSV_FORMAT)

        rdf_collection = RDFCollection()
        store.load_all(rdf_collection)

        self.assertTrue(rdf_collection.contains("ACTIVITY"))
        self.assertTrue(rdf_collection.has_subject('ACT'))
        self.assertTrue(rdf_collection.has_predicate('ACT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ACT', "hasPurpose", "to entertain by performing"))

        self.assertTrue(rdf_collection.contains("ANIMAL"))
        self.assertTrue(rdf_collection.has_subject('ANT'))
        self.assertTrue(rdf_collection.has_predicate('ANT', "hasPurpose"))
        self.assertTrue(rdf_collection.has_object('ANT', "hasPurpose", "to make anthills"))
