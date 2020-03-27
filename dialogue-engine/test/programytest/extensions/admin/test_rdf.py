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

from programytest.client import TestClient

from programy.extensions.admin.rdf import RDFAdminExtension
from programy.utils.substitutions.substitues import Substitutions


class RDFAdminExtensionClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(RDFAdminExtensionClient, self).load_configuration(arguments, subs)


class RDFAdminExtensionTests(unittest.TestCase):

    def test_subjects_list(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "SUBJECTS LIST")
        self.assertIsNotNone(result)
        self.assertEqual("<ul><li>MONKEY</li></ul>", result)

    def test_subjects_count(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "SUBJECTS COUNT")
        self.assertIsNotNone(result)
        self.assertEqual("1", result)

    def test_predicates(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMALS")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "PREDICATES MONKEY")
        self.assertIsNotNone(result)
        self.assertEqual("<ul><li>LEGS</li></ul>", result)

    def test_objects(self):

        client = RDFAdminExtensionClient()
        client_context = client.create_client_context("testid")

        client_context.brain.rdf.add_entity("MONKEY", "LEGS", "2", "ANIMAL")

        extension = RDFAdminExtension()
        self.assertIsNotNone(extension)

        result = extension.execute(client_context, "OBJECT MONKEY LEGS")
        self.assertIsNotNone(result)
        self.assertEqual("<ul><li>2</li></ul>", result)
