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
import os
import shutil

from programy.utils.logging.ylogger import YLogger

from programy.storage.stores.file.store.filestore import FileStore

from programy.storage.entities.rdf import RDFStore
from programy.storage.entities.rdf import RDFUpdatesStore

from datetime import datetime


class FileRDFStore(FileStore, RDFStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _load_file_contents(self, rdf_collection, filename):
        YLogger.debug(self, "Loading rdf [%s]", filename)
        try:
            line_no = 0
            with open(filename, 'r', encoding='utf8') as my_file:
                for line in my_file:
                    line_no += 1
                    line = line.strip()
                    if line:
                        if line[0] == '#':
                            continue
                        splits = line.split(":")
                        if len(splits) > 2:
                            subj = splits[0].strip()
                            pred = splits[1].strip()
                            obj = (":".join(splits[2:])).strip()

                            rdf_name = self.get_just_filename_from_filepath(filename)

                            rdf_collection.add_entity(subj, pred, obj, rdf_name, filename, line_no=line_no)
                        else:
                            error_info = "illegal format [%s]" % line
                            rdf_collection.set_error_info(filename, line_no, error_info)

        except Exception as excep:
            YLogger.exception(self, "Failed to load rdf [%s]", excep, filename)

    def get_storage(self):
        return self.storage_engine.configuration.rdf_storage

    def reload(self, collection, rdf_name):
        filename = collection.storename(rdf_name)
        collection.empty()
        self._load_file_contents(collection, filename)


class FileRDFUpdatesStore(FileStore, RDFUpdatesStore):

    COMMAND_ADD = 'add'
    COMMAND_DELETE = 'del'
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S:%f"

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _updates_filename(self, storage_dir):
        return "%s%srdf_updates.txt" % (storage_dir, os.sep)

    def _save_filename(self, storage_dir):
        return "%s%srdf_data.txt" % (storage_dir, os.sep)

    def get_storage(self):
        return self.storage_engine.configuration.rdf_updates_storage

    def _get_storage_path(self):
        if len(self.storage_engine.configuration.rdf_updates_storage.dirs) > 1:
            YLogger.warning(self, "RDF-Modified Storage has multiple folders specified, using first only")
        return self.storage_engine.configuration.rdf_updates_storage.dirs[0]

    def empty(self):
        updates_path = self._get_storage_path()
        if os.path.exists(updates_path) is True:
            shutil.rmtree(updates_path)

    def empty_updates(self):
        updates_filepath = self._updates_filename(self._get_storage_path())
        if os.path.exists(updates_filepath):
            os.remove(updates_filepath)

    def _write_entry(self, command, subject, predicate, objct):
        self._ensure_dir_exists(self._get_storage_path())
        filepath = self._updates_filename(self._get_storage_path())

        date = datetime.now().strftime(self.DATE_FORMAT)
        cmdline = "%s\t%s\t%s:%s:%s\n" % (date, command, subject, predicate, objct)
        try:
            updates_file = open(filepath, 'a')
            updates_file.write(cmdline)
            updates_file.close()
        except Exception as e:
            YLogger.exception(None, "Failed to write RDF-update[add] [%s]", e, filepath)
        return

    def add_entry(self, subject, predicate, objct):
        command = self.COMMAND_ADD
        self._write_entry(command, subject, predicate, objct)

    def delete_entry(self, subject, predicate, objct):
        command = self.COMMAND_DELETE
        if predicate is None:
            predicate = ' '
        if objct is None:
            objct = ' '
        self._write_entry(command, subject, predicate, objct)

    def apply_rdf_updates(self, rdf_collection, lastdate: datetime):
        filepath = self._updates_filename(self._get_storage_path())
        if os.path.exists(filepath) is False:
            return

        if lastdate is None:
            is_apply = True
        else:
            is_apply = False
            filetime = os.path.getmtime(filepath)
            filedate = datetime.fromtimestamp(filetime)
            if filedate < lastdate:
                return

        try:
            lineNo = 0
            with open(filepath, "r", encoding="utf-8") as updates_file:
                for line in updates_file:
                    lineNo += 1
                    line = line.strip()
                    if line:
                        commands = line.split('\t')
                        if len(commands) < 3:
                            YLogger.error(None, "RDF-Updates line[%d] illegal [%s]", lineNo, line)
                            continue

                        update = commands[0].strip()
                        if is_apply is False:
                            checkdate = datetime.strptime(update, self.DATE_FORMAT)
                            if checkdate < lastdate:
                                continue
                            is_apply = True

                        method = commands[1].strip()
                        rdf_param = commands[2].strip()
                        splits = rdf_param.split(':')
                        if len(splits) < 3:
                            YLogger.error(None, "RDF-Updates line[%d] illegal [%s]", lineNo, line)
                            continue

                        subject = splits[0].strip()
                        predicate = splits[1].strip()
                        objct = splits[2].strip()
                        if predicate == '':
                            predicate = None
                        if objct == '':
                            objct = None
                        if method == self.COMMAND_ADD:
                            YLogger.debug(None, "Apply RDF-Updates line[%d] add[%s:%s:%s]", lineNo, subject, predicate, objct)
                            rdf_collection.add_entity(subject, predicate, objct, None)
                        elif method == self.COMMAND_DELETE:
                            YLogger.debug(None, "Apply RDF-RDF-Updates line[%d] delete[%s:%s:%s]", lineNo, subject, predicate, objct)
                            rdf_collection.delete_entity(subject, predicate, objct)
                        else:
                            YLogger.error(None, "Apply RDF-Updates line[%d] unknown [%s]", lineNo, method)

        except Exception as e:
            YLogger.exception(None, "Failed to load RDF-Updates [%s]", e, filepath)

        return

    def save_rdf_data(self, collection):
        if collection is None:
            return

        self._ensure_dir_exists(self._get_storage_path())
        filepath = self._save_filename(self._get_storage_path())
        try:
            savedata_file = open(filepath, 'a')
            entities = collection.entities
            for subject, preddic in entities.items():
                predicates = preddic._predicates
                for predicate, objdic in predicates.items():
                    for objct in objdic:
                        dataform = '"%s": "%s": "%s"\n' % (subject, predicate, objct)
                        savedata_file.write(dataform)
            savedata_file.close()
        except Exception as e:
            YLogger.exception(None, "Failed to write RDF-update[add] [%s]", e, filepath)
