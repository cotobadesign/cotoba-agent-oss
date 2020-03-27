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

from programy.rdf.collection import RDFCollection


class RDFCollectionMatchingTests(unittest.TestCase):

    def add_data(self, collection):
        collection.add_entity("MONKEY", "LEGS", "2", "ANIMALS")
        collection.add_entity("MONKEY", "HASFUR", "true", "ANIMALS")
        collection.add_entity("ZEBRA", "LEGS", "4", "ANIMALS")
        collection.add_entity("BIRD", "LEGS", "2", "ANIMALS")
        collection.add_entity("ELEPHANT", "TRUNK", "true", "ANIMALS")

    def test_all_as_tuples(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()
        self.assertIsNotNone(all)
        self.assertEqual(5, len(all))
        self.assertTrue(["MONKEY", "LEGS", "2"] in all)
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in all)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in all)
        self.assertTrue(["BIRD", "LEGS", "2"] in all)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in all)

    def test_match_all_as_tuples(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples()
        self.assertIsNotNone(matched)
        self.assertEqual(5, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in matched)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in matched)
        self.assertTrue(["BIRD", "LEGS", "2"] in matched)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in matched)

    def test_match_all_as_tuples_subject(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in matched)

    def test_match_all_as_tuples_subject_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY", predicate="LEGS")
        self.assertIsNotNone(matched)
        self.assertEqual(1, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)

    def test_match_all_as_tuples_subject_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY", predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(1, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)

    def test_match_all_as_tuples_predicate(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(predicate="LEGS")
        self.assertIsNotNone(matched)
        self.assertEqual(3, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in matched)
        self.assertTrue(["BIRD", "LEGS", "2"] in matched)

    def test_match_all_as_tuples_predicate_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(predicate="LEGS", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(2, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)
        self.assertTrue(["BIRD", "LEGS", "2"] in matched)

    def test_match_as_tuples_subject_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        matched = collection.matched_as_tuples(subject="MONKEY", obj="2")
        self.assertIsNotNone(matched)
        self.assertEqual(1, len(matched))
        self.assertTrue(["MONKEY", "LEGS", "2"] in matched)

    def test_remove_subject(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY')
        self.assertIsNotNone(remains)
        self.assertEqual(3, len(remains))
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in remains)

    def test_remove_subject_predicate(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY', predicate="LEGS")
        self.assertIsNotNone(remains)
        self.assertEqual(4, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in remains)

    def test_remove_subject_object(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY', obj="2")
        self.assertIsNotNone(remains)
        self.assertEqual(4, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in all)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in all)
        self.assertTrue(["BIRD", "LEGS", "2"] in all)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in all)

    def test_remove_predicate(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, predicate='LEGS')
        self.assertIsNotNone(remains)
        self.assertEqual(2, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in remains)

    def test_remove_predicate_object(self):

        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, predicate='LEGS', obj="2")
        self.assertIsNotNone(remains)
        self.assertEqual(3, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in all)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in all)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in all)

    def test_remove_object(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, obj='2')
        self.assertIsNotNone(remains)
        self.assertEqual(3, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in remains)

    def test_remove_all_parameter(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all, subject='MONKEY', predicate="LEGS", obj='2')
        self.assertIsNotNone(remains)
        self.assertEqual(4, len(remains))
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in remains)

    def test_remove_all_no_target(self):
        collection = RDFCollection()
        self.assertIsNotNone(collection)

        self.add_data(collection)

        all = collection.all_as_tuples()

        remains = collection.remove(all)
        self.assertIsNotNone(remains)
        self.assertEqual(5, len(remains))
        self.assertTrue(["MONKEY", "LEGS", "2"] in remains)
        self.assertTrue(["MONKEY", "HASFUR", "TRUE"] in remains)
        self.assertTrue(["ZEBRA", "LEGS", "4"] in remains)
        self.assertTrue(["BIRD", "LEGS", "2"] in remains)
        self.assertTrue(["ELEPHANT", "TRUNK", "TRUE"] in remains)
