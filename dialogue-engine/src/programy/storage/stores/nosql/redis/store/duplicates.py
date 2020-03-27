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
import json
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.duplicates import DuplicatesStore


class RedisDuplicatesStore(RedisStore, DuplicatesStore):

    DUPLICATES = 'duplicates'

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def collection_name(self):
        return RedisDuplicatesStore.DUPLICATES

    def create_key(self, type):
        return "{prefix}:{type}:duplicates".format(prefix=self._storage_engine._prefix, type=type)

    def make_mesage(self, filename, start, end, raw, column, description):
        category_dic = {"start": start, "end": end}
        node_dic = {"raw": raw, "column": column}
        message_dic = {"file": filename, "category": category_dic, "node": node_dic, "description": description}
        return message_dic

    def save_duplicates(self, duplicates):
        YLogger.debug(self, "Saving duplicates to Redis")
        storeData = {"duplicates": []}

        for duplicate in duplicates:
            storeData["duplicates"].append(self.make_mesage(filename=duplicate[0], start=duplicate[1], end=duplicate[2],
                                           raw=duplicate[3], column=duplicate[4], description=duplicate[5]))

        json_text = json.dumps(storeData, ensure_ascii=False)
        try:
            h_key = self.create_key("duplicates")
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Adding duplicates [%s] - [%s]", s_key, h_key)

            self.store(h_key, s_key, s_key, json_text, ex=self._storage_engine._expiretime)

        except Exception as e:
            YLogger.exception(self, "Failed to save duplicates to Redis [%s]", e, s_key)

    def load_duplicates(self):
        try:
            h_key = self.create_key("duplicates")

            YLogger.debug(self, "Fetching duplicates [%s]", h_key)
            duplicates = self.load(h_key)
            json_data = json.loads(str(duplicates, encoding='utf-8'))
            return json_data

        except Exception as e:
            YLogger.exception(self, "Failed to load duplicates from Redis", e)

        return None
