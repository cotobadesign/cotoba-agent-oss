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


class PatternMatcherISetTests(PatternMatcherBaseClass):

    def test_basic_iset_match(self):

        self.add_pattern_to_graph(pattern="I AM A <iset>MAN, WOMAN</iset>", topic="*", that="*", template="1")

        context = self.match_sentence("I AM A MAN", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("I AM A WOMAN", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

    def test_multiple_iset_match(self):

        self.add_pattern_to_graph(pattern="I LIKE TO <iset>PARTY, DRINK, SLEEP</iset> DURING THE DAY", topic="*", that="*", template="1")
        self.add_pattern_to_graph(pattern="I LIKE TO <iset>PARTY, DRINK, SLEEP</iset> DURING THE NIGHT", topic="*", that="*", template="2")

        context = self.match_sentence("I LIKE TO PARTY DURING THE DAY", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("I LIKE TO PARTY DURING THE NIGHT", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("2", context.template_node().template.word)

    def test_basic_iset_match_jp(self):

        self.add_pattern_to_graph(pattern="私は <iset>男性, 女性</iset>です", topic="*", that="*", template="1")

        context = self.match_sentence("私は男性です", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("私は女性です", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

    def test_multiple_iset_match_jp(self):

        self.add_pattern_to_graph(pattern="私は<iset>パーティ, お酒, 睡眠</iset>が趣味です", topic="*", that="*", template="1")
        self.add_pattern_to_graph(pattern="私は<iset>パーティ, お酒, 睡眠</iset>が好きです", topic="*", that="*", template="2")

        context = self.match_sentence("私はパーティが趣味です", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("私はパーティが好きです", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("2", context.template_node().template.word)

    def test_multiple_iset_match_jp_multiword(self):

        self.add_pattern_to_graph(pattern="私は<iset>千葉県, 東京, 神奈川県下</iset>の生まれです", topic="*", that="*", template="1")

        context = self.match_sentence("私は千葉県の生まれです", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("私は千葉の生まれです", topic="*", that="*")
        self.assertIsNone(context)

        context = self.match_sentence("私は東京の生まれです", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("私は東京都の生まれです", topic="*", that="*")
        self.assertIsNone(context)

        context = self.match_sentence("私は神奈川県下の生まれです", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        context = self.match_sentence("私は神奈川県の生まれです", topic="*", that="*")
        self.assertIsNone(context)
