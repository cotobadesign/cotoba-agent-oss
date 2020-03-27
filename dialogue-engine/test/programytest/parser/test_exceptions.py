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
import xml.etree.ElementTree as ET

from programy.parser.exceptions import ParserException
from programy.parser.exceptions import DuplicateGrammarException
from programy.parser.exceptions import MatcherException


class ExceptionTests(unittest.TestCase):

    def test_parser_exception_basic(self):
        exception = ParserException("message")
        self.assertEqual("message", exception.message)
        exception.filename = "test.xml"
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("message in [test.xml]", exception.format_message())

    def test_parser_exception_filename(self):
        exception = ParserException("message", filename="test.xml")
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("message in [test.xml]", exception.format_message())

    def test_parser_exception_xml_as_string(self):
        element = ET.fromstring("<template />")
        exception = ParserException("message", filename="test.xml", xml_exception="xml_exception_error", xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("xml_exception_error", exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] : xml_exception_error", exception.format_message())

    def test_parser_exception_xml(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = ParserException("message", filename="test.xml", xml_exception=xml_exception, xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_parser_exception_via_sets(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = ParserException("message", filename="test.xml")
        exception.xml_exception = xml_exception
        self.assertEqual(xml_exception, exception.xml_exception)
        exception.xml_element = element
        self.assertEqual(element, exception.xml_element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_duplicate_grammar_exception_basic(self):
        exception = DuplicateGrammarException("duplicate")
        self.assertEqual("duplicate", exception.message)
        self.assertEqual("duplicate", exception.format_message())

    def test_duplicate_grammar_exception_filename(self):
        exception = DuplicateGrammarException("message", filename="test.xml")
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("message in [test.xml]", exception.format_message())

    def test_duplicate_grammar_exception_filename_set(self):
        exception = DuplicateGrammarException("duplicate")
        exception.filename = "test.xml"
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual("duplicate in [test.xml]", exception.format_message())

    def test_duplicate_grammar_exception_xml(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = ParserException("message", filename="test.xml", xml_exception=xml_exception, xml_element=element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_duplicate_grammar_exception_via_sets(self):
        element = ET.fromstring("<template />")
        xml_exception = ET.ParseError()
        xml_exception.position = []
        xml_exception.position.append(1)
        xml_exception.position.append(2)
        exception = DuplicateGrammarException("message", filename="test.xml")
        exception.xml_exception = xml_exception
        self.assertEqual(xml_exception, exception.xml_exception)
        exception.xml_element = element
        self.assertEqual(element, exception.xml_element)
        self.assertEqual("message", exception.message)
        self.assertEqual("test.xml", exception.filename)
        self.assertEqual(xml_exception, exception.xml_exception)
        self.assertEqual(element, exception._xml_element)
        self.assertEqual("message in [test.xml] at [line(1), column(2)]", exception.format_message())

    def test_matcher_exception(self):
        exception = MatcherException("matcher")
        self.assertEqual("matcher", exception.message)
