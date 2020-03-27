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

from programy.storage.stores.sql.dao.twitter import Twitter


class TwitterTests(unittest.TestCase):

    def test_init(self):
        twitter1 = Twitter(last_direct_message_id='66', last_status_id='99')
        self.assertIsNotNone(twitter1)
        self.assertEqual("<Twitter(id='n/a', last_direct_message_id='66', last_status_id='99')>", str(twitter1))

        twitter2 = Twitter(id=1, last_direct_message_id='66', last_status_id='99')
        self.assertIsNotNone(twitter2)
        self.assertEqual("<Twitter(id='1', last_direct_message_id='66', last_status_id='99')>", str(twitter2))
