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
import os.path
import shutil

from programytest.storage.asserts.store.assert_twitter import TwitterStoreAsserts

from programy.storage.stores.file.store.twitter import FileTwitterStore
from programy.storage.stores.file.engine import FileStorageEngine
from programy.storage.stores.file.config import FileStorageConfiguration


class FileTwitterStoreTests(TwitterStoreAsserts):

    def setUp(self):
        self._tmpdir = os.path.dirname(__file__) + os.sep + "twitter"
        self._tmpfile = self._tmpdir + os.sep + "twitter.ids"

    def tearDown(self):
        if os.path.exists(self._tmpdir):
            shutil.rmtree(self._tmpdir)
        self.assertFalse(os.path.exists(self._tmpdir))

    def test_initialise(self):
        config = FileStorageConfiguration()

        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)
        self.assertEqual(store.storage_engine, engine)

    def test_twitter_storage(self):
        config = FileStorageConfiguration()

        config.twitter_storage._dirs = [self._tmpfile]
        config.twitter_storage._has_single_file = True

        engine = FileStorageEngine(config)
        engine.initialise()
        store = FileTwitterStore(engine)

        self.assert_twitter_storage(store)
