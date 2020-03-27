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

from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.pattern.nodes.root import PatternRootNode
from programy.parser.pattern.nodes.word import PatternWordNode


class PatternFactoryTests(unittest.TestCase):

    def test_init(self):
        factory = PatternNodeFactory()
        self.assertIsNotNone(factory)
        self.assertEqual({}, factory._nodes_config)
        self.assertEqual("Pattern", factory._type)

    def assert_nodes(self, factory):
        self.assertEqual(12, len(factory._nodes_config))

        self.assertTrue("root" in factory._nodes_config)
        instance = factory._nodes_config["root"]
        root = instance()
        self.assertIsInstance(root, PatternRootNode)

        self.assertTrue("word" in factory._nodes_config)
        instance = factory._nodes_config["word"]
        word = instance("test")
        self.assertIsInstance(word, PatternWordNode)
