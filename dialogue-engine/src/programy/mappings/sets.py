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
Copyright(c) 2016-2019 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files(the "Software"), to deal in the Software without restriction, including without limitation
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

from programy.storage.factory import StorageFactory


class SetCollection(object):

    def __init__(self, errors_dict=None):
        self._sets = {}
        self._stores = {}
        self._is_cjk = {}
        self._values = {}

        if errors_dict is None:
            self._errors_dict = None
        else:
            errors_dict['sets'] = []
            self._errors_dict = errors_dict['sets']

    @property
    def sets(self):
        return self._sets

    @property
    def stores(self):
        return self._stores

    def storename(self, mapname):
        if mapname in self._stores:
            return self._stores[mapname]
        return None

    def empty(self):
        self._sets.clear()
        self._stores.clear()
        self._is_cjk.clear()
        self._values.clear()

    def remove(self, set_name):
        self._sets.pop(set_name, None)
        self._stores.pop(set_name, None)
        self._is_cjk.pop(set_name, None)
        self._values.pop(set_name, None)

    def set_error_info(self, filename, line, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'line': line, 'description': description}
            self._errors_dict.append(error_info)

    def add_set(self, set_name, the_set, set_store, is_cjk, values):

        # Set names always stored in upper case to handle ambiquity
        set_name = set_name.upper()

        if set_name in self._sets:
            error_info = "duplicate set_name='%s' (set_list is invalid)" % set_name
            self.set_error_info(set_store, 0, error_info)
            return

        YLogger.debug(self, "Adding set [%s][%s] to set group", set_name, set_store)
        self._sets[set_name] = the_set
        self._stores[set_name] = set_store
        self._is_cjk[set_name] = is_cjk
        self._values[set_name] = values

    def contains(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        return bool(set_name in self._sets)

    def set_list(self, name):
        # Set names always stored in upper case to handle ambiquity
        set_name = name.upper()
        if set_name in self._sets:
            return self._sets[set_name]
        return None

    def store_name(self, set_name):
        if set_name in self._stores:
            return self._stores[set_name]
        return None

    def is_cjk(self, set_name):
        if set_name in self._is_cjk:
            return self._is_cjk[set_name]
        return None

    def values(self, set_name):
        if set_name in self._values:
            return self._values[set_name]
        return None

    def count_words_in_sets(self):
        count = 0
        for _, aset in self._sets.items():
            for _, variant in aset.items():
                for value in variant:
                    if type(value) is list:
                        count += len(value)
                    else:
                        count += 1

        return count

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.SETS) is True:
            sets_store_engine = storage_factory.entity_storage_engine(StorageFactory.SETS)
            if sets_store_engine:
                try:
                    sets_store = sets_store_engine.sets_store()
                    sets_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load set from storage", e)

        return len(self._sets)

    def reload(self, storage_factory, set_name):
        if storage_factory.entity_storage_engine_available(StorageFactory.SETS) is True:
            set_engine = storage_factory.entity_storage_engine(StorageFactory.SETS)
            if set_engine:
                try:
                    sets_store = set_engine.sets_store()
                    sets_store.reload(self, set_name)
                except Exception as e:
                    YLogger.exception(self, "Failed to load set from storage", e)
