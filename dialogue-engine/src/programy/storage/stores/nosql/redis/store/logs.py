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
from programy.storage.entities.logs import LogsStore


class RedisLogsStore(RedisStore, LogsStore):

    LOGS = 'logs'
    CLIENITD = 'clientid'
    USERID = 'userid'

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def collection_name(self):
        return RedisLogsStore.LOGS

    def create_key(self, clientid, userid):
        return "{prefix}:{clientid}:{userid}:logs".format(prefix=self._storage_engine._prefix, clientid=clientid, userid=userid)

    def store_logs(self, client_context, conversation):
        YLogger.debug(client_context, "Storing logs to Redis [%s] [%s]", client_context.client.id, client_context.userid)
        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Adding logs [%s] - [%s]", s_key, h_key)
            logs_json = {}
            logs_json['logs'] = conversation.logs

            json_text = json.dumps(logs_json, ensure_ascii=False, indent=4)

            self.store(h_key, s_key, client_context.client.id, json_text, ex=self._storage_engine._expiretime)

        except Exception as e:
            YLogger.exception(self, "Failed to save logs to Redis for clientid [%s][%s]", e, client_context.client.id, client_context.userid)

    def load_logs(self, client_context):
        YLogger.debug(client_context, "load logs from Redis [%s] [%s]", client_context.client.id, client_context.userid)
        logs = None

        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            # Check if clientid in sessions set
            if not self.is_member(s_key, client_context.client.id):
                YLogger.debug(self, "Clientid [%s], not in sessions [%s]", client_context.client.id, s_key)
                return logs

            YLogger.debug(self, "Fetching logs [%s]", h_key)
            redis_data = self.load(h_key)
            logs = json.loads(str(redis_data, encoding='utf-8'))
        except Exception:
            logs = None
            YLogger.debug(self, "Failed to Load logs from Redis for [%s][%s]", client_context.client.id, client_context.userid)

        return logs
