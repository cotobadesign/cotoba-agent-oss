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

from programy.activate import Activatable


class ActivatableTests(unittest.TestCase):

    def test_init(self):
        activatable = Activatable()
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)
        self.assertTrue(activatable.is_active())

        activatable = Activatable(Activatable.ON)
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)
        self.assertTrue(activatable.is_active())

        activatable = Activatable(Activatable.OFF)
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.OFF, activatable.active)
        self.assertFalse(activatable.is_active())

    def test_on_off(self):
        activatable = Activatable()
        self.assertIsNotNone(activatable)
        self.assertEquals(Activatable.ON, activatable.active)

        activatable.active = Activatable.OFF
        self.assertEquals(Activatable.OFF, activatable.active)
        self.assertFalse(activatable.is_active())

        activatable.active = Activatable.ON
        self.assertEquals(Activatable.ON, activatable.active)
        self.assertTrue(activatable.is_active())
