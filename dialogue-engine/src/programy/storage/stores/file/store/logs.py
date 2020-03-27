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
import shutil

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.logs import LogsStore
import json


class FileLogsStore(FileStore, LogsStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def empty(self):
        if os.path.exists(self._storage_engine.configuration.logs_storage.dirs[0]) is True:
            shutil.rmtree(self._storage_engine.configuration.logs_storage.dirs[0])

    def _logs_filename(self, storage_dir, clientid, userid, ext="log"):
        return "%s%s%s_%s.%s" % (storage_dir, os.sep, clientid, userid, ext)

    def store_logs(self, client_context, conversation):
        self._ensure_dir_exists(self._storage_engine.configuration.logs_storage.dirs[0])

        logs_filepath = self._logs_filename(self._storage_engine.configuration.logs_storage.dirs[0], client_context.client.id, client_context.userid)

        YLogger.debug(self, "Writing logs to [%s]", logs_filepath)

        logs_json = {}
        logs_json['logs'] = conversation.logs

        try:
            with open(logs_filepath, "w+", encoding="utf-8") as logs_file:
                json.dump(logs_json, logs_file, ensure_ascii=False, indent=4)

        except Exception as excep:
            YLogger.exception(self, "Failed to write logs file [%s]", excep, logs_filepath)

    def load_logs(self, client_context):
        logs_filepath = self._logs_filename(self._storage_engine.configuration.logs_storage.dirs[0], client_context.client.id, client_context.userid)
        logs = None
        if self._file_exists(logs_filepath):
            try:
                with open(logs_filepath, "r+", encoding="utf-8") as logs_file:
                    logs = json.load(logs_file)
            except Exception as excep:
                logs = None
                YLogger.exception(self, "Failed to read logs file [%s]", excep, logs_filepath)

        return logs
