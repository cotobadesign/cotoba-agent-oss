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

from programy.storage.stores.nosql.mongo.dao.rdf import RDF


class RDFTests(unittest.TestCase):

    def test_init_no_id(self):
        rdf = RDF(name="TEST", subject="subj", predicate="pred", object="obj")

        self.assertIsNotNone(rdf)
        self.assertIsNone(rdf.id)
        self.assertEqual("TEST", rdf.name)
        self.assertEqual("subj", rdf.subject)
        self.assertEqual("pred", rdf.predicate)
        self.assertEqual("obj", rdf.object)
        self.assertEqual({'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'}, rdf.to_document())

    def test_init_with_id(self):
        rdf = RDF(name="TEST", subject="subj", predicate="pred", object="obj")
        rdf.id = '666'

        self.assertIsNotNone(rdf)
        self.assertIsNotNone(rdf.id)
        self.assertEqual('666', rdf.id)
        self.assertEqual("TEST", rdf.name)
        self.assertEqual("subj", rdf.subject)
        self.assertEqual("pred", rdf.predicate)
        self.assertEqual("obj", rdf.object)
        self.assertEqual({'_id': '666', 'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'}, rdf.to_document())

    def test_from_document(self):
        rdf1 = RDF.from_document({'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'})
        self.assertIsNotNone(rdf1)
        self.assertIsNone(rdf1.id)
        self.assertEqual("TEST", rdf1.name)
        self.assertEqual("subj", rdf1.subject)
        self.assertEqual("pred", rdf1.predicate)
        self.assertEqual("obj", rdf1.object)

        rdf2 = RDF.from_document({'_id': '666', 'name': 'TEST', 'object': 'obj', 'predicate': 'pred', 'subject': 'subj'})
        self.assertIsNotNone(rdf2)
        self.assertIsNotNone(rdf2.id)
        self.assertEqual('666', rdf2.id)
        self.assertEqual("TEST", rdf2.name)
        self.assertEqual("subj", rdf2.subject)
        self.assertEqual("pred", rdf2.predicate)
        self.assertEqual("obj", rdf2.object)
