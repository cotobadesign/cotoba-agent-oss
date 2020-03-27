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
from programy.storage.entities.braintree import BraintreeStore

import datetime


class RedisBraintreeStore(RedisStore, BraintreeStore):

    def __init__(self, storage_engine):
        RedisStore.__init__(self, storage_engine)
        self._braintree = ''

    def create_key(self, type, format):
        if format == RedisStore.TEXT_FORMAT:
            return "{prefix}:{type}:textbraintree".format(prefix=self._storage_engine._prefix, type=type)
        elif format == RedisStore.XML_FORMAT:
            return "{prefix}:{type}:xmlbraintree".format(prefix=self._storage_engine._prefix, type=type)
        return "{prefix}:{type}:braintree".format(prefix=self._storage_engine._prefix, type=type)

    def output_braintree(self, handle, data):
        self._braintree += data

    def save_braintree(self, client_context, pattern_graph):
        self._braintree = ''

        # Default XML-Format
        format = RedisStore.XML_FORMAT
        encoding = 'UTF-8'

        try:
            h_key = self.create_key("binaries", format)
            s_key = self._storage_engine._sessions_set_key

            YLogger.info(self, "Saving brainTree to redis [%s]", h_key)
            start = datetime.datetime.now()

            if format == RedisStore.TEXT_FORMAT:
                pattern_graph.dump(output_func=self.output_braintree, eol="\n")

            elif format == RedisStore.XML_FORMAT:
                self._braintree = '<?xml version="1.0" encoding="%s"?>\n' % encoding
                self._braintree += '<aiml>\n'
                self._braintree += pattern_graph.root.to_xml(client_context)
                self._braintree += '</aiml>\n'

            else:
                YLogger.error(client_context, "Unknown brainTree content type [%s]", format)
                return

            self.store(h_key, s_key, s_key, self._braintree, ex=self._storage_engine._expiretime)

            stop = datetime.datetime.now()
            diff = stop - start
            YLogger.info(self, "BrainTree save took a total of %.2f sec", diff.total_seconds())

        except Exception as e:
            YLogger.exception(self, "Failed to save brainTree to Redis [%s]", e, s_key)
