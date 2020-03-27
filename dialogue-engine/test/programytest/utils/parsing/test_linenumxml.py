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
from programy.utils.parsing.linenumxml import LineNumberingParser
import xml.etree.ElementTree as ET

import os
import unittest


class LineNumberingParserTests(unittest.TestCase):

    def test_broken_xml(self):
        with self.assertRaises(ET.ParseError) as raised:
            ET.parse(os.path.dirname(__file__) + os.sep + "broken.xml", parser=LineNumberingParser())
        self.assertEqual(22, raised.exception.position[0])
        self.assertEqual(10, raised.exception.position[1])

    def test_working_xml(self):
        tree = ET.parse(os.path.dirname(__file__) + os.sep + "working.xml", parser=LineNumberingParser())
        aiml = tree.getroot()
        if hasattr(aiml, "_end_line_number"):
            self.assertEqual(28, aiml._end_line_number)
            self.assertEqual(0, aiml._end_column_number)

        patterns = aiml.findall('category')
        self.assertEqual(1, len(patterns))
        if hasattr(patterns[0], "_end_line_number"):
            self.assertEqual(26, patterns[0]._end_line_number)
            self.assertEqual(4, patterns[0]._end_column_number)
