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
from unittest import TestCase

from programy.sentiment.scores import SentimentScores


class SentimentScoresTests(TestCase):

    def test_positivity(self):
        scorer = SentimentScores()

        self.assertEqual("EXTREMELY NEGATIVE", scorer.positivity(-1.0))

        self.assertEqual("VERY NEGATIVE", scorer.positivity(-0.8))

        self.assertEqual("QUITE NEGATIVE", scorer.positivity(-0.6))

        self.assertEqual("NEGATIVE", scorer.positivity(-0.4))

        self.assertEqual("SOMEWHAT NEGATIVE", scorer.positivity(-0.2))

        self.assertEqual("NEUTRAL", scorer.positivity(-0.09))
        self.assertEqual("NEUTRAL", scorer.positivity(0.0))
        self.assertEqual("NEUTRAL", scorer.positivity(0.09))

        self.assertEqual("SOMEWHAT POSITIVE", scorer.positivity(0.2))

        self.assertEqual("POSITIVE", scorer.positivity(0.4))

        self.assertEqual("QUITE POSITIVE", scorer.positivity(0.6))

        self.assertEqual("VERY POSITIVE", scorer.positivity(0.8))

        self.assertEqual("EXTREMELY POSITIVE", scorer.positivity(1.0))

    def test_subjectivity(self):
        scorer = SentimentScores()

        self.assertEqual("COMPLETELY OBJECTIVE", scorer.subjectivity(0.0))

        self.assertEqual("MOSTLY OBJECTIVE", scorer.subjectivity(0.01))
        self.assertEqual("MOSTLY OBJECTIVE", scorer.subjectivity(0.1))
        self.assertEqual("MOSTLY OBJECTIVE", scorer.subjectivity(0.2))

        self.assertEqual("SOMEWHAT OBJECTIVE", scorer.subjectivity(0.21))
        self.assertEqual("SOMEWHAT OBJECTIVE", scorer.subjectivity(0.3))
        self.assertEqual("SOMEWHAT OBJECTIVE", scorer.subjectivity(0.4))

        self.assertEqual("NEUTRAL", scorer.subjectivity(0.41))
        self.assertEqual("NEUTRAL", scorer.subjectivity(0.5))
        self.assertEqual("NEUTRAL", scorer.subjectivity(0.6))

        self.assertEqual("SOMEWHAT SUBJECTIVE", scorer.subjectivity(0.61))
        self.assertEqual("SOMEWHAT SUBJECTIVE", scorer.subjectivity(0.7))
        self.assertEqual("SOMEWHAT SUBJECTIVE", scorer.subjectivity(0.8))

        self.assertEqual("MOSTLY SUBJECTIVE", scorer.subjectivity(0.81))
        self.assertEqual("MOSTLY SUBJECTIVE", scorer.subjectivity(0.9))
        self.assertEqual("MOSTLY SUBJECTIVE", scorer.subjectivity(0.99))

        self.assertEqual("COMPLETELY SUBJECTIVE", scorer.subjectivity(1.0))
