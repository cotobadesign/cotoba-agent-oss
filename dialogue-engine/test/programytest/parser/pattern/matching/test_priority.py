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

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherTests(PatternMatcherBaseClass):

    def test_priority_tree_matching_no_wildcards(self):

        self.add_pattern_to_graph(pattern="$A B D", topic="X", that="Y", template="1")
        self.add_pattern_to_graph(pattern="A B D", topic="X", that="Y", template="2")

        context = self.match_sentence("A B D", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
