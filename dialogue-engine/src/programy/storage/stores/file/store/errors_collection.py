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
import os.path
import json

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.errors_collection import ErrorsCollectionStore


class FileErrorsCollectionStore(FileStore, ErrorsCollectionStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.errors_collection_storage.file

    def empty(self):
        filename = self._get_storage_path()
        if os.path.exists(filename) is True:
            os.remove(filename)

    def save_errors_collection(self, errors):
        filename = self._get_storage_path()
        file_dir = self._get_dir_from_path(filename)
        self._ensure_dir_exists(file_dir)

        YLogger.debug(self, "Saving errors_collection to [%s]", filename)
        try:
            storeData = {"errors_collection": errors}
            json_text = json.dumps(storeData, ensure_ascii=False, indent=4)
            with open(filename, "w+", encoding="utf-8") as errors_file:
                errors_file.write(json_text)

        except Exception as excep:
            YLogger.exception(self, "Failed to write errors_collection file [%s]", excep, filename)

    def load_errors_collection(self):
        filename = self._get_storage_path()

        try:
            with open(filename, "r+", encoding="utf-8") as error_file:
                json_text = error_file.read()
                loadData = json.loads(json_text)

        except Exception as excep:
            loadData = None
            YLogger.exception(self, "Failed to errors_collection", excep)

        return loadData
