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
import yaml

from programy.utils.logging.ylogger import YLogger

from programy.storage.stores.file.store.filestore import FileStore
from programy.storage.entities.resttemplates import RestTemplatesStore


class FileRestTemplatesStore(FileStore, RestTemplatesStore):

    def __init__(self, storage_engine):
        FileStore.__init__(self, storage_engine)

    def _get_storage_path(self):
        return self._storage_engine.configuration.rest_templates_storage.file

    def _load_file_contents(self, collection, filename):
        YLogger.debug(self, "Loading NLU_Servers [%s]", filename)
        template_index = 0
        try:
            with open(filename, 'r+', encoding="utf-8") as yml_file:
                yaml_data = yaml.load(yml_file, Loader=yaml.SafeLoader)
                if yaml_data is not None:
                    rest_section = self._get_section(yaml_data, 'rest')
                    if rest_section is not None:
                        templates = self._get_keys(rest_section)
                        for name in templates:
                            template = self._get_section(rest_section, name)
                            params, error_info = self._make_rest_params(collection, template)
                            if error_info is None:
                                collection.add_rest_template(name, params, filename, template_index)
                            else:
                                collection.set_error_info(filename, template_index, error_info)
                            template_index += 1
                    else:
                        error_info = "rest section not found"
                        collection.set_error_info(filename, None, error_info)

        except Exception as excep:
            YLogger.exception(self, "Failed to load REST-Template [%s]", excep, filename)
            error_info = "illegal yaml format"
            collection.set_error_info(filename, 0, error_info)

    def _make_rest_params(self, collection, template_yaml):
        error_info = None
        host = self._get_yaml_option(template_yaml, 'host')
        params = collection.make_rest_params(host)
        if params.host is None:
            error_info = "invalid host parameter [%s]" % host
            return None, error_info
        method = self._get_yaml_option(template_yaml, 'method')
        if params.set_method(method) is False:
            error_info = "invalid method parameter [%s]" % method
            return None, error_info
        query = self._get_yaml_option(template_yaml, 'query')
        if params.set_query(query) is False:
            error_info = "invalid query parameter [%s]" % query
            return None, error_info
        header = self._get_yaml_option(template_yaml, 'header')
        if params.set_header(header) is False:
            error_info = "invalid header parameter [%s]" % header
            return None, error_info
        body = self._get_yaml_option(template_yaml, 'body')
        params.set_body(body)
        return params, error_info

    def _get_section(self, yaml_data, section_name):
        if section_name in yaml_data:
            return yaml_data[section_name]
        return None

    def _get_keys(self, section):
        return section.keys()

    def _get_yaml_option(self, section, option_name):
        if option_name in section:
            return section[option_name]
        return None

    def get_storage(self):
        return self.storage_engine.configuration.rest_templates_storage

    def load(self, collection):
        templates_path = self._get_storage_path()
        self._load_file_contents(collection, templates_path)

    def reload_all(self, collection):
        templates_path = self._get_storage_path()
        self._load_file_contents(collection, templates_path)
