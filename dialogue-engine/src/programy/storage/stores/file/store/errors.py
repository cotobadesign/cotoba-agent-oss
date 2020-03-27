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
import os
import os.path

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.errors import ErrorsStore


class FileErrorsStore(FileStore, ErrorsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self.storage_engine.configuration.errors_storage.file

    def empty(self):
        filename = self._get_storage_path()
        if os.path.exists(filename) is True:
            os.remove(filename)

    def save_errors(self, errors):
        filename = self._get_storage_path()
        file_dir = self._get_dir_from_path(filename)
        self._ensure_dir_exists(file_dir)
        try:
            YLogger.debug(self, "Saving errors to [%s]", filename)

            with open(filename, "w+", encoding="utf-8") as errors_file:
                errors_file.write("FileName\tCategory-Start\tCategory-End\tNode-Raw\tNode-Column\tNode-Name\tDescription\n")
                for error in errors:
                    errors_file.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (error[0], error[1], error[2], error[3], error[4], error[5], error[6]))
                errors_file.flush()

        except Exception as excep:
            YLogger.exception(self, "Failed to write errors file [%s]", excep, filename)

    def make_message(self, filename, start, end, raw, column, nodename, description):
        if start == 'None':
            category_dic = {"start": None, "end": None}
        else:
            try:
                start_int = int(start)
                end_int = int(end)
                category_dic = {"start": start_int, "end": end_int}
            except Exception:
                category_dic = {"start": start, "end": end}
        try:
            raw_int = int(raw)
            column_int = int(column)
            node_dic = {"raw": raw_int, "column": column_int}
        except Exception:
            node_dic = {"raw": raw, "column": column}
        if nodename == 'None':
            nodename = None
        message_dic = {"description": description, "file": filename, "category": category_dic, "node": node_dic, "node_name": nodename}
        return message_dic

    def load_errors(self):
        loadData = {"errors": []}
        filename = self._get_storage_path()
        is_header = True

        try:
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    if is_header is True:
                        is_header = False
                        continue
                    if line:
                        line = line.strip()
                        error_info = line.split('\t')
                        error_dic = self.make_message(filename=error_info[0],
                                                      start=error_info[1],
                                                      end=error_info[2],
                                                      raw=error_info[3],
                                                      column=error_info[4],
                                                      nodename=error_info[5],
                                                      description=error_info[6])
                        loadData["errors"].append(error_dic)

        except Exception as excep:
            loadData = None
            YLogger.exception(self, "Failed to load errors", excep)

        return loadData
