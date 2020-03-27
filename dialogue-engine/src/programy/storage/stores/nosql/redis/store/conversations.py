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
import copy
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.conversation import ConversationStore


class RedisConversationStore(RedisStore, ConversationStore):

    CONVERSATIONS = 'conversations'
    CONVERSATION = 'conversation'
    CLIENITD = 'clientid'
    USERID = 'userid'
    CHUNK_SIZE = 5000

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def collection_name(self):
        return RedisConversationStore.CONVERSATIONS

    def empty(self):
        return

    def create_key(self, clientid, userid):
        return "{prefix}:{clientid}:{userid}:conversation".format(prefix=self._storage_engine._prefix, clientid=clientid, userid=userid)

    def store_conversation(self, client_context, conversation):
        YLogger.debug(client_context, "Storing conversation to Redis [%s] [%s]", client_context.client.id, client_context.userid)
        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Adding conversation [%s] - [%s]", s_key, h_key)
            conversation.questions[len(conversation.questions)-1]._name_properties = copy.copy(conversation.properties)
            conversation.questions[len(conversation.questions)-1]._data_properties = copy.copy(conversation.data_properties)

            convo_json = conversation.to_json()
            json_text = json.dumps(convo_json, ensure_ascii=False, indent=4)

            self.store(h_key, s_key, client_context.client.id, json_text, ex=self._storage_engine._expiretime)

        except Exception as e:
            YLogger.exception(self, "Failed to save conversation to Redis for clientid [%s][%s]", e, client_context.client.id, client_context.userid)

    def load_conversation(self, client_context, conversation):
        YLogger.debug(client_context, "Loading conversation from Redis [%s] [%s]", client_context.client.id, client_context.userid)

        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            # Check if clientid in sessions set
            if not self.is_member(s_key, client_context.client.id):
                YLogger.debug(self, "Clientid [%s], not in sessions [%s]", client_context.client.id, s_key)
                return {}

            YLogger.debug(self, "Fetching conversation [%s]", h_key)
            conversations = self.load(h_key)

            json_data = json.loads(str(conversations, encoding='utf-8'))
            conversation.from_json(client_context, json_data)
            return True

        except Exception:
            YLogger.debug(self, "Failed to load conversation from Redis for [%s] [%s]", client_context.client.id, client_context.userid)

        return False

    def delete_conversation(self, client_context):
        YLogger.debug(client_context, "Delete conversation from Redis [%s] [%s]", client_context.client.id, client_context.userid)
        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)

            YLogger.debug(self, "Delete conversation from Redis [%s]", h_key)

            cursor = '0'
            while cursor != 0:
                cursor, keys = self._storage_engine._redis.scan(cursor=cursor, match=h_key, count=RedisConversationStore.CHUNK_SIZE)
                if keys:
                    self._storage_engine._redis.delete(*keys)

        except Exception as e:
            YLogger.exception(self, "Failed to delete conversation from Redis for clientid [%s]", e, client_context.client.id)

    def debug_conversation_data(self, client_context):
        YLogger.debug(client_context, "Debug conversation from Redis [%s] [%s]", client_context.client.id, client_context.userid)
        conversations = {}
        conversation = None

        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            # Check if clientid in sessions set
            if not self.is_member(s_key, client_context.client.id):
                YLogger.debug(self, "Clientid [%s], not in sessions [%s]", client_context.client.id, s_key)
                return conversations

            YLogger.debug(self, "Fetching conversation [%s]", h_key)
            redis_data = self.load(h_key)
            conversation = json.loads(str(redis_data, encoding='utf-8'))
        except Exception:
            conversation = None
            YLogger.debug(self, "Failed to Debug conversation from Redis for [%s][%s]", client_context.client.id, client_context.userid)

        if conversation is not None:
            conversations['conversations'] = conversation

        return conversations

    def modify_conversation_data(self, client_context, conversation):
        YLogger.debug(client_context, "Modify conversation to Redis [%s] [%s]", client_context.client.id, client_context.userid)
        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            YLogger.debug(self, "Adding conversation [%s] - [%s]", s_key, h_key)
            convo_json = conversation.to_json()
            json_text = json.dumps(convo_json, ensure_ascii=False, indent=4)

            self.store(h_key, s_key, client_context.client.id, json_text)

        except Exception as e:
            YLogger.exception(self, "Failed to modify conversation to Redis for clientid [%s][%s]", e, client_context.client.id, client_context.userid)
