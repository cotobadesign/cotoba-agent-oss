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


class PatternMatcherSetTests(PatternMatcherBaseClass):

    def test_basic_set_match_as_text(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            set_dict = {"MAN": [["MAN"]], "WOMAN": [["WOMAN"]]}
            values = {"MAN": "MAN", "WOMAN": "WOMAN"}
            self._client_context.brain._sets_collection.add_set("SEX", set_dict, "teststore", False, values)

        self.add_pattern_to_graph(pattern="I AM A <set>sex</set>", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("MAN", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("WOMAN", context.star(1))

    def test_basic_set_match_as_name(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            set_dict = {"MAN": [["MAN"]], "WOMAN": [["WOMAN"]]}
            values = {"MAN": "MAN", "WOMAN": "WOMAN"}
            self._client_context.brain._sets_collection.add_set("SEX", set_dict, "teststore", False, values)

        self.add_pattern_to_graph(pattern='I AM A <set name="sex" />', topic="X", that="Y", template="1")

        context = self.match_sentence("I AM A MAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("MAN", context.star(1))

        context = self.match_sentence("I AM A WOMAN", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("WOMAN", context.star(1))

    def test_multi_word_set_match(self):

        set_dict = {"RED": [["RED"], ["RED", "AMBER"], ["RED", "BURNT", "OAK"], ["RED", "ORANGE"]]}
        values = {"RED": "RED", "RED AMBER": "RED AMBER", "RED BURNT OAK": "RED BURNT OAK", "RED ORANGE": "RED ORANGE"}
        self._client_context.brain._sets_collection.add_set("COLOR", set_dict, "teststore", False, values)

        self.add_pattern_to_graph(pattern="I LIKE <set>color</set> *", topic="*", that="*", template="1")

        context = self.match_sentence("I LIKE RED PAINT", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("RED", context.star(1))
        self.assertEqual("PAINT", context.star(2))

        context = self.match_sentence("I LIKE RED AMBER CARS", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("RED AMBER", context.star(1))
        self.assertEqual("CARS", context.star(2))

        context = self.match_sentence("I LIKE RED BURNT OAK MOTOR BIKES", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("RED BURNT OAK", context.star(1))
        self.assertEqual("MOTOR BIKES", context.star(2))

    def test_multi_word_match_value(self):

        set_dict = {"RED": [["RED"], ["RED", "AMBER"], ["RED", "BURNT", "OAK"], ["RED", "ORANGE"]]}
        values = {"RED": "red", "RED AMBER": "red amber", "RED BURNT OAK": "red burnt oak", "RED ORANGE": "red orange"}
        self._client_context.brain._sets_collection.add_set("COLOR", set_dict, "teststore", False, values)

        self.add_pattern_to_graph(pattern="i like <set>color</set> *", topic="*", that="*", template="1")

        context = self.match_sentence("I LIKE RED PAINT", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("red", context.star(1))
        self.assertEqual("PAINT", context.star(2))

        context = self.match_sentence("I LIKE RED AMBER CARS", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("red amber", context.star(1))
        self.assertEqual("CARS", context.star(2))

        context = self.match_sentence("I LIKE RED BURNT OAK MOTOR BIKES", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("red burnt oak", context.star(1))
        self.assertEqual("MOTOR BIKES", context.star(2))

    def test_basic_set_match_as_text_jp(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            set_dict = {"男": ["男", "男性"], "女": ["女", "女性"]}
            values = {"男": "男", "男性": "男性", "女": "女", "女性": "女性"}
            self._client_context.brain._sets_collection.add_set("SEX", set_dict, "teststore", True, values)

        self.add_pattern_to_graph(pattern="私は <set>sex</set>", topic="X", that="Y", template="1")

        context = self.match_sentence("私は男性", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("男性", context.star(1))

        context = self.match_sentence("私は女", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("女", context.star(1))

    def test_basic_set_match_as_name_jp(self):

        if self._client_context.brain.sets.contains("SEX") is False:
            set_dict = {"男": ["男", "男性"], "女": ["女", "女性"]}
            values = {"男": "男", "男性": "男性", "女": "女", "女性": "女性"}
            self._client_context.brain._sets_collection.add_set("SEX", set_dict, "teststore", True, values)

        self.add_pattern_to_graph(pattern='私は <set name="sex" />', topic="X", that="Y", template="1")

        context = self.match_sentence("私は男", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("男", context.star(1))

        context = self.match_sentence("私は女性", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("女性", context.star(1))

    def test_multi_word_set_match_jp(self):

        set_dict = {"赤": ["赤", "赤色", "赤黒い", "赤面", "赤に塗った"]}
        values = {"赤": "赤", "赤色": "赤色", "赤黒い": "赤黒い", "赤面": "赤面", "赤に塗った": "赤に塗った"}
        self._client_context.brain._sets_collection.add_set("COLOR", set_dict, "teststore", True, values)

        self.add_pattern_to_graph(pattern="私が好きなのは<set>color</set> *", topic="*", that="*", template="1")

        context = self.match_sentence("私が好きなのは赤系統", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("赤", context.star(1))
        self.assertEqual("系統", context.star(2))

        context = self.match_sentence("私が好きなのは赤黒い車", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("赤黒い", context.star(1))
        self.assertEqual("車", context.star(2))

        context = self.match_sentence("私が好きなのは赤に塗ったバイク", topic="*", that="*")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)
        self.assertEqual("赤に塗った", context.star(1))
        self.assertEqual("バイク", context.star(2))

    def test_basic_set_number_match(self):
        self._client_context.brain.dynamics.add_dynamic_set('number', "programy.dynamic.sets.numeric.IsNumeric", None)

        self.add_pattern_to_graph(pattern="I AM <set>number</set> YEARS OLD", topic="X", that="Y", template="1")

        context = self.match_sentence("I AM 49 YEARS OLD", topic="X", that="Y")
        self.assertIsNotNone(context)
        self.assertIsNotNone(context.template_node())
        self.assertEqual("1", context.template_node().template.word)

        self.assertEqual("49", context.star(1))
