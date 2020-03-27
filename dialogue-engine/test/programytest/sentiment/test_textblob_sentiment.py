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

from programy.sentiment.textblob_sentiment import TextBlobSentimentAnalyser


class TestTextBlobSentimentAnalyser(unittest.TestCase):

    def test_analyse_each(self):
        analyser = TextBlobSentimentAnalyser()
        results = analyser.analyse_each("Programy-Y is awesome. I love it")
        self.assertEquals([(1.0, 1.0), (0.5, 0.6)], results)

    def test_analyse_all(self):
        analyser = TextBlobSentimentAnalyser()
        results = analyser.analyse_all("Programy-Y is awesome. I love it")
        self.assertEquals((0.75, 0.8), results)
