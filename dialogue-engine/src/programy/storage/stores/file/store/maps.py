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

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.maps import MapsStore

from programy.utils.language.japanese import JapaneseLanguage

import re


class FileMapsStore(FileStore, MapsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, map_collection, filename):
        YLogger.debug(self, "Loading map [%s]", filename)

        the_map = {}
        try:
            line_no = 0
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    line_no += 1
                    line = line.strip()
                    if line == '' or line[0] == '#':
                        continue
                    splits = line.split(":")
                    if len(splits) > 1:
                        targer_word = splits[0].strip()
                        if targer_word == '':
                            error_info = "key is empty"
                            map_collection.set_error_info(filename, line_no, error_info)
                            continue
                        targer_word = JapaneseLanguage.zenhan_normalize(targer_word)
                        key = re.sub(' +', ' ', targer_word.upper())
                        value = ":".join(splits[1:]).strip()
                        if key not in the_map:
                            the_map[key] = value.strip()
                        else:
                            error_info = "duplicate key='%s' (value='%s' is invalid)" % (key, value)
                            map_collection.set_error_info(filename, line_no, error_info)
                    else:
                        error_info = "invalid parameters [%s]" % line
                        map_collection.set_error_info(filename, line_no, error_info)

        except Exception as excep:
            YLogger.exception(self, "Failed to load map [%s]", excep, filename)

        if len(the_map) > 0:
            name = self.get_just_filename_from_filepath(filename)
            map_name = JapaneseLanguage.zenhan_normalize(name)
            map_collection.add_map(map_name, the_map, filename)

        return self.storage_engine.configuration.maps_storage

    def get_storage(self):
        return self.storage_engine.configuration.maps_storage

    def load(self, collection):
        col_store = self.get_storage()
        collection.empty()
        self._load_file_contents(collection, col_store.file)

    def reload(self, collection, map_name):
        filename = collection.storename(map_name)
        collection.empty()
        self._load_file_contents(collection, filename)
