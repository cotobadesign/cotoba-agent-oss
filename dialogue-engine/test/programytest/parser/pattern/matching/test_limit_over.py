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
import datetime

from programy.parser.exceptions import LimitOverException

from programytest.parser.pattern.matching.base import PatternMatcherBaseClass


class PatternMatcherLimitExceededTests(PatternMatcherBaseClass):

    def test_base_consume_time_exceeded(self):

        self.add_pattern_to_graph(pattern="A B D E F", topic="X", that="Y", template="1")

        self._client_context.bot.configuration._max_search_timeout = 1
        self._client_context._question_start_time = datetime.datetime(2019, 4, 1, 9, 0, 0)

        with self.assertRaises(LimitOverException):
            self.match_sentence("A B D E F", topic="X", that="Z")

    def test_base_consume_depth_exceeded(self):

        self.add_pattern_to_graph(pattern="# F", topic="X", that="Y", template="1")

        self._client_context.bot.configuration._max_search_depth = 2

        with self.assertRaises(LimitOverException):
            self.match_sentence("A B C D E F", topic="X", that="Z")

    def test_zeroormore_consume_depth_exceeded(self):

        self.add_pattern_to_graph(pattern="A # F", topic="X", that="Y", template="1")

        self._client_context.bot.configuration._max_search_depth = 1

        with self.assertRaises(LimitOverException):
            self.match_sentence("A B C D E F", topic="X", that="Z")

    def test_oneormore_consume_depth_exceeded(self):

        self.add_pattern_to_graph(pattern="A * F", topic="X", that="Y", template="1")

        self._client_context.bot.configuration._max_search_depth = 1

        with self.assertRaises(LimitOverException):
            self.match_sentence("A B C D E F", topic="X", that="Z")
