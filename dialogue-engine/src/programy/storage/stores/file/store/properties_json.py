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
from programy.utils.logging.ylogger import YLogger

import os
import json

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.properties_json import PropertyJsonStore


class FilePropertyJsonStore(FileStore, PropertyJsonStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading json property from [%s]", filename)
        try:
            with open(filename, 'r+', encoding="utf-8") as json_file:
                json_dict = json.load(json_file)
                key = self._get_filename_from_filepath(filename)
                collection.add_property(key, json.dumps(json_dict, ensure_ascii=False), filename, 0)
        except Exception as excep:
            YLogger.exception(self, "Failed to load json property file [%s]", excep, filename)
            error_info = "invalid json format"
            collection.set_error_info(filename, 0, error_info)

    def _get_filename_from_filepath(self, filepath):
        try:
            filename = os.path.splitext(os.path.basename(filepath))[0]
        except Exception:
            return ""
        return filename

    def get_storage(self):
        return self.storage_engine.configuration.properties_json_storage

    def load(self, collection):
        json_store = self.get_storage()
        self._load_json_property(collection, json_store.file)
