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

from programy.config.brain.nlu import BrainNluConfiguration
from programy.nlu.nlu import NluRequest


class NluRequestTests(unittest.TestCase):

    def test_nlu_initiate(self):

        nlu_config = BrainNluConfiguration()
        nlu_request = NluRequest(nlu_config)
        self.assertIsNotNone(nlu_request)
        self.assertIsInstance(nlu_request, NluRequest)

    def test_nluCall(self):

        nlu_config = BrainNluConfiguration()
        nlu_request = NluRequest(nlu_config)
        self.assertIsNotNone(nlu_request)
        self.assertIsInstance(nlu_request, NluRequest)

        with self.assertRaises(NotImplementedError):
            nlu_request.nluCall(None, "http://test_nlu.co.jp", "apikey", "Test")

    def test_load_nlu(self):

        nlu_config = BrainNluConfiguration()
        nlu = NluRequest.load_nlu(nlu_config)
        self.assertIsNotNone(nlu)
        self.assertIsInstance(nlu, NluRequest)

    def test_load_nlu_no_classname(self):

        nlu_config = BrainNluConfiguration()
        nlu_config._classname = None
        nlu = NluRequest.load_nlu(nlu_config)
        self.assertIsNone(nlu)
