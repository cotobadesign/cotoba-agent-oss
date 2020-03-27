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
"""
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.binaries import BinariesStore

try:
    import _pickle as pickle
except Exception:
    import pickle
import gc
import datetime


class RedisBinariesStore(RedisStore, BinariesStore):

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def create_key(self, type):
        return "{prefix}:{type}:binaries".format(prefix=self._storage_engine._prefix, type=type)

    def save_binary(self, aiml_parser):
        try:
            h_key = self.create_key("binaries")
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Saving binary brain to redis [%s]", s_key)
            start = datetime.datetime.now()

            data = pickle.dumps(aiml_parser)
            self.store(h_key, s_key, s_key, data, ex=self._storage_engine._expiretime)

            stop = datetime.datetime.now()
            diff = stop - start
            YLogger.debug(self, "Brain save took a total of %.2f sec", diff.total_seconds())

        except Exception as e:
            YLogger.exception(self, "Failed to save binaries to Redis [%s]", e, s_key)

    def load_binary(self):
        try:
            h_key = self.create_key("binaries")
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Loading binary brain from redis [%s]", s_key)

            start = datetime.datetime.now()
            gc.disable()

            YLogger.debug(self, "Fetching binaries [%s]", h_key)
            binaries = self.load(h_key)
            aiml_parser = pickle.loads(binaries)
            gc.enable()

            stop = datetime.datetime.now()
            diff = stop - start
            YLogger.debug(self, "Brain load took a total of %.2f sec", diff.total_seconds())
            return aiml_parser

        except Exception as excep:
            YLogger.exception(self, "Failed to load binary", excep)
            gc.enable()
            return None
