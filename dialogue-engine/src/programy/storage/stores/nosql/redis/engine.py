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

import redis

from programy.utils.logging.ylogger import YLogger
from programy.storage.engine import StorageEngine
from programy.storage.stores.nosql.redis.store.binaries import RedisBinariesStore
from programy.storage.stores.nosql.redis.store.braintree import RedisBraintreeStore
from programy.storage.stores.nosql.redis.store.conversations import RedisConversationStore
from programy.storage.stores.nosql.redis.store.logs import RedisLogsStore
from programy.storage.stores.nosql.redis.store.duplicates import RedisDuplicatesStore
from programy.storage.stores.nosql.redis.store.errors import RedisErrorsStore
from programy.storage.stores.nosql.redis.store.errors_collection import RedisErrorsCollectionStore
from programy.storage.stores.nosql.redis.store.learnf import RedisLearnfStore


class RedisStorageEngine(StorageEngine):

    def __init__(self, configuration):
        StorageEngine.__init__(self, configuration)

    def initialise(self):
        self._prefix = self.configuration.prefix
        self._sessions_set_key = "{prefix}:sessions".format(prefix=self._prefix)
        self._expiretime = self.configuration.expiretime

        if self.configuration.password is not None:
            self._redis = redis.StrictRedis(
                host=self.configuration.host,
                port=self.configuration.port,
                password=self.configuration.password,
                db=self.configuration.db)
        else:
            self._redis = redis.StrictRedis(
                host=self.configuration.host,
                port=self.configuration.port,
                db=self.configuration.db)

        if self.configuration.drop_all_first is True:
            try:
                self.conversation_store().empty()
            except Exception as e:
                YLogger.exception(self, "Failed deleting conversation redis data - ", e)

    def binaries_store(self):
        return RedisBinariesStore(self)

    def braintree_store(self):
        return RedisBraintreeStore(self)

    def learnf_store(self):
        return RedisLearnfStore(self)

    def errors_store(self):
        return RedisErrorsStore(self)

    def duplicates_store(self):
        return RedisDuplicatesStore(self)

    def errors_collection_store(self):
        return RedisErrorsCollectionStore(self)

    def conversation_store(self):
        return RedisConversationStore(self)

    def logs_store(self):
        return RedisLogsStore(self)
