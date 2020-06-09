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
import json
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.errors_collection import ErrorsCollectionStore


class RedisErrorsCollectionStore(RedisStore, ErrorsCollectionStore):

    ERRORS_COLLECTION = 'errors_collection'

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def collection_name(self):
        return RedisErrorsCollectionStore.ERRORS_COLLECTION

    def create_key(self, type):
        return "{prefix}:{type}:errors_collection".format(prefix=self._storage_engine._prefix, type=type)

    def save_errors_collection(self, errors):
        YLogger.debug(self, "Saving errors_collection to Redis")
        storeData = {"errors_collection": errors}

        json_text = json.dumps(storeData, ensure_ascii=False)
        try:
            h_key = self.create_key("errors_collection")
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Adding errors_collection [%s] - [%s]", s_key, h_key)

            self.store(h_key, s_key, s_key, json_text, ex=self._storage_engine._expiretime)

        except Exception as e:
            YLogger.exception(self, "Failed to errors_collection to Redis [%s]", e, s_key)

    def load_errors_collection(self):
        try:
            h_key = self.create_key("errors_collection")

            YLogger.debug(self, "Fetching errors_collection [%s]", h_key)
            errors_collection = self.load(h_key)
            json_data = json.loads(str(errors_collection, encoding='utf-8'))
            return json_data

        except Exception as e:
            YLogger.exception(self, "Failed to load errors_collection from Redis", e)

        return None
