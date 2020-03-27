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

import xml.etree.ElementTree as ET
from programy.utils.logging.ylogger import YLogger
from programy.storage.stores.nosql.redis.store.redisstore import RedisStore
from programy.storage.entities.learnf import LearnfStore


class RedisLearnfStore(RedisStore, LearnfStore):

    LEARNF = 'learnf'
    CHUNK_SIZE = 5000

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)

    def collection_name(self):
        return RedisLearnfStore.LEARNF

    def create_key(self, clientid, userid):
        return "{prefix}:{clientid}:{userid}:learnf".format(prefix=self._storage_engine._prefix, clientid=clientid, userid=userid)

    def create_learnf_if_missing(self):
        return ET.fromstring('<?xml version="1.0" encoding="UTF-8"?><aiml></aiml>')

    def create_category_xml_node(self, client_context, category):
        # Add our new element
        child = ET.Element("category")
        child.append(category.pattern)
        child.append(category.topic)
        child.append(category.that)
        xml_category = category.template.xml_tree(client_context)
        child.append(xml_category)
        return child

    def _remove_existed_node(self, root, node):

        new_pattern = node.find('pattern')
        if new_pattern is None:
            return
        new_pattern_str = ET.tostring(new_pattern)

        new_topic = node.find('topic')
        if new_topic is None:
            new_topic_str = None
        else:
            new_topic_str = ET.tostring(new_topic)
        new_that = node.find('that')
        if new_that is None:
            new_that_str = None
        else:
            new_that_str = ET.tostring(new_that)

        for category in root:
            current_pattern = category.find('pattern')
            if current_pattern is not None:
                current_pattern_str = ET.tostring(current_pattern)
                if current_pattern_str == new_pattern_str:
                    current_topic = category.find('topic')
                    if current_topic is None:
                        current_topic_str = None
                    else:
                        current_topic_str = ET.tostring(current_topic)
                    current_that = category.find('that')
                    if current_that is None:
                        current_that_str = None
                    else:
                        current_that_str = ET.tostring(current_that)
                    if current_topic_str == new_topic_str and current_that_str == new_that_str:
                        root.remove(category)

    def save_learnf(self, client_context, category, is_replace):

        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            learnf = self._load_learnf(client_context)
            if learnf:
                root_node = ET.fromstring(learnf)
            else:
                root_node = self.create_learnf_if_missing()

            learnf_node = self.create_category_xml_node(client_context, category)

            if is_replace is True:
                self._remove_existed_node(root_node, learnf_node)

            root_node.append(learnf_node)
            node = ET.tostring(root_node, encoding='utf-8')
            self.store(h_key, s_key, client_context.client.id, node, ex=self._storage_engine._expiretime)

        except Exception as e:
            YLogger.exception(self, "Failed to save learnf to Redis for clientid [%s]", e, client_context.client.id)

    def _load_learnf(self, client_context):
        YLogger.debug(client_context, "Loading learnf from Redis [%s] [%s]", client_context.client.id, client_context.userid)

        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)
            s_key = self._storage_engine._sessions_set_key

            # Check if clientid in sessions set
            if not self.is_member(s_key, client_context.client.id):
                YLogger.debug(self, "Clientid [%s], not in sessions [%s]", client_context.client.id, s_key)
                return None

            YLogger.debug(self, "Fetching learnf [%s]", h_key)
            return self.load(h_key)

        except Exception:
            YLogger.debug(self, "Failed to load learnf from Redis for clientid [%s]", client_context.client.id, client_context.userid)
            return None

    def load_learnf(self, client_context):
        learnf = self._load_learnf(client_context)
        if learnf:
            client_context.brain.aiml_parser.parse_from_text(str(learnf, encoding='utf-8'), client_context.userid)
            return True

        return False

    def delete_learnf(self, client_context):

        YLogger.debug(client_context, "Delete learnf from Redis [%s] [%s]", client_context.client.id, client_context.userid)
        try:
            h_key = self.create_key(client_context.client.id, client_context.userid)

            YLogger.debug(self, "Delete learnf from Redis [%s]", h_key)

            cursor = '0'
            while cursor != 0:
                cursor, keys = self._storage_engine._redis.scan(cursor=cursor, match=h_key, count=RedisLearnfStore.CHUNK_SIZE)
                if keys:
                    self._storage_engine._redis.delete(*keys)

        except Exception as e:
            YLogger.exception(self, "Failed to delete learnf from Redis for clientid [%s]", e, client_context.client.id)
