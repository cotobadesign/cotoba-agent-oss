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
import xml.etree.ElementTree as ET

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.learnf import LearnfStore


class FileLearnfStore(FileStore, LearnfStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    @staticmethod
    def create_learnf_path(client_context, learnf_dir):
        return "%s%s%s_%s.aiml" % (learnf_dir, os.sep, client_context.client.id, client_context.userid)

    @staticmethod
    def create_learnf_file_if_missing(learnf_path):

        if os.path.isfile(learnf_path) is False:
            try:
                YLogger.debug(None, "Creating new learnf file [%s]", learnf_path)

                with open(learnf_path, "w+", encoding="utf-8") as file:
                    file.write('<?xml version="1.0" encoding="UTF-8"?>\n')
                    file.write('<aiml>\n')
                    file.write('</aiml>\n')
                    file.close()

            except Exception as excep:
                YLogger.exception(None, "Error Writing learnf to %s", excep, learnf_path)

    @staticmethod
    def write_node_to_learnf_file(client_context, node, learnf_path, is_replace):

        YLogger.debug(client_context, "Writing learnf to %s", learnf_path)

        try:
            tree = ET.parse(learnf_path)
        except Exception:
            # Assume invalid aiml file, so remove it and start again with a fresh copy
            if os.path.exists(learnf_path) is True:
                os.remove(learnf_path)
            FileLearnfStore.create_learnf_file_if_missing(learnf_path)
            tree = ET.parse(learnf_path)

        root = tree.getroot()

        if is_replace is True:
            FileLearnfStore.remove_existed_node(root, node)

        root.append(node)
        tree.write(learnf_path, method="xml", encoding='UTF-8')

    @staticmethod
    def remove_existed_node(root, node):

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

    def _get_storage_path(self):
        if len(self.storage_engine.configuration.learnf_storage.dirs) > 1:
            YLogger.warning(self, "Learnf Storage has multiple folders specified, using first only")

        return self.storage_engine.configuration.learnf_storage.dirs[0]

    def create_category_xml_node(self, client_context, category):
        # Add our new element
        child = ET.Element("category")
        child.append(category.pattern)
        child.append(category.topic)
        child.append(category.that)
        xml_category = category.template.xml_tree(client_context)
        child.append(xml_category)
        return child

    def save_learnf(self, client_context, category, is_replace):
        try:
            xml_node = self.create_category_xml_node(client_context, category)

            learnf_path = self._get_storage_path()
            self._ensure_dir_exists(learnf_path)

            learnf_fullpath = self.create_learnf_path(client_context, learnf_path)

            self.create_learnf_file_if_missing(learnf_fullpath)

            self.write_node_to_learnf_file(client_context, xml_node, learnf_fullpath, is_replace)

        except Exception as exc:
            YLogger.exception(client_context, "Failed to save learnf", exc)

    def load_learnf(self, client_context):
        try:
            learnf_path = self._get_storage_path()
            if os.path.exists(learnf_path) is True:
                learnf_fullpath = self.create_learnf_path(client_context, learnf_path)

                if self._file_exists(learnf_fullpath):
                    YLogger.debug(self, "Load learnfile from [%s]", learnf_fullpath)
                    client_context.brain.aiml_parser.parse_from_file(learnf_fullpath, userid=client_context.userid)
                    return True

            return False

        except Exception as exc:
            YLogger.exception(client_context, "Failed to load learnfile", exc)

    def delete_learnf(self, client_context):
        try:
            learnf_path = self._get_storage_path()
            if os.path.exists(learnf_path) is True:
                learnf_fullpath = self.create_learnf_path(client_context, learnf_path)
                if os.path.exists(learnf_fullpath) is True:
                    os.remove(learnf_fullpath)
        except Exception as exc:
            YLogger.exception(client_context, "Failed to delete learnfile", exc)
