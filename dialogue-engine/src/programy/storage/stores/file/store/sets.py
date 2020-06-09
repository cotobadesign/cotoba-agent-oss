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
from programy.utils.language.japanese import JapaneseLanguage

from programy.storage.entities.sets import SetsStore

import re


class FileSetsStore(FileStore, SetsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, set_collection, filename):
        YLogger.debug(self, "Loading set [%s]", filename)
        try:
            the_set = {}
            set_list = []
            check_list = []
            is_cjk = False
            values = {}
            line_no = 0
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    line_no += 1
                    line = line.strip()
                    if line:
                        if line[0] == '#':
                            continue
                        chk_words = JapaneseLanguage.zenhan_normalize(line)
                        chk_words = chk_words.upper()
                        cjk = self.check_cjk(is_cjk, chk_words)
                        if cjk is True:
                            chk_words = re.sub(' ', '', chk_words)
                            if is_cjk is False:
                                is_cjk = True
                        else:
                            chk_words = re.sub(' +', ' ', chk_words)
                        if chk_words in check_list:
                            error_info = "duplicate value='%s'" % line
                            set_collection.set_error_info(filename, line_no, error_info)
                        else:
                            set_list.append(line)
                            check_list.append(chk_words)
            the_set, values = self.make_set_table(is_cjk, set_list)

        except Exception as excep:
            YLogger.exception(self, "Failed to load set [%s]", excep, filename)

        set_name = self.get_just_filename_from_filepath(filename)
        set_collection.add_set(set_name, the_set, filename, is_cjk, values)

    def get_storage(self):
        return self.storage_engine.configuration.sets_storage

    def load(self, collection):
        col_store = self.get_storage()
        collection.empty()
        self._load_file_contents(collection, col_store.file)

    def reload(self, collection, set_name):
        filename = collection.storename(set_name)
        collection.empty()
        self._load_file_contents(collection, filename)
