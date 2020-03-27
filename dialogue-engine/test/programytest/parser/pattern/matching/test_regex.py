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
import re

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherRegexTests(PatternMatcherBaseClass):

    def test_basic_regex_match_as_text(self):

        self.add_pattern_to_graph(pattern="I AM <regex>^LEGION$</regex>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_pattern(self):

        self.add_pattern_to_graph(pattern='I AM <regex pattern="^LEGION$" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_template(self):

        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("^LEGION$", re.IGNORECASE))

        self.add_pattern_to_graph(pattern='I AM <regex template="LEGION" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNone(context)

    def test_part_word_regex_match_as_template(self):

        self._client_context.brain.regex_templates.add_regex("LEGION", re.compile("LEGION*", re.IGNORECASE))

        self.add_pattern_to_graph(pattern='I AM <regex template="LEGION" />', topic="*", that="*", template="1")

        context = self.match_sentence("I AM LEGION", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGION", context.star(1))

        context = self.match_sentence("I AM LEGIONAIRRE", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("LEGIONAIRRE", context.star(1))

    def test_regex_loaded_from_file(self):

        self._client_context.brain.regex_templates.add_regex("ANYINTEGER", re.compile('^\\d+$', re.IGNORECASE))

        self.add_pattern_to_graph(pattern='I AM <regex template="ANYINTEGER" /> YEARS OLD', topic="*", that="*", template="CORRECT")

        context = self.match_sentence("I AM 27 YEARS OLD", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("CORRECT", context.template_node().template.word)
        self.assertEqual("27", context.star(1))

    def test_basic_regex_match_as_form(self):

        self.add_pattern_to_graph(pattern='すみません<regex form="今[はわ]何時" />', topic="*", that="*", template="1")

        context = self.match_sentence("すみません今は何時", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("今は何時", context.star(1))

        context = self.match_sentence("すみません今何時", topic="*", that="*")
        self.assertIsNone(context)

    def test_basic_regex_match_as_form_multi_words(self):

        self.add_pattern_to_graph(pattern='<regex form="(デモ|でも)(ンストレーション)?" />スタート', topic="*", that="*", template="1")

        context1 = self.match_sentence("デモスタート", topic="*", that="*")
        self.assertIsNotNone(context1)
        self.assertIsNotNone(context1.template_node())
        self.assertEqual("1", context1.template_node().template.word)
        self.assertEqual("デモ", context1.star(1))

        context2 = self.match_sentence("でもスタート", topic="*", that="*")
        self.assertIsNotNone(context2)
        self.assertIsNotNone(context2.template_node())
        self.assertEqual("1", context2.template_node().template.word)
        self.assertEqual("でも", context2.star(1))

        context3 = self.match_sentence("デモンストレーションスタート", topic="*", that="*")
        self.assertIsNotNone(context3)
        self.assertIsNotNone(context3.template_node())
        self.assertEqual("1", context3.template_node().template.word)
        self.assertEqual("デモンストレーション", context3.star(1))

        context4 = self.match_sentence("でもンストレーションスタート", topic="*", that="*")
        self.assertIsNotNone(context4)
        self.assertIsNotNone(context4.template_node())
        self.assertEqual("1", context4.template_node().template.word)
        self.assertEqual("でもンストレーション", context4.star(1))

        context5 = self.match_sentence("デモンストレーション", topic="*", that="*")
        self.assertIsNone(context5)
