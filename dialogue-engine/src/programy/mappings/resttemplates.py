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
import json
import ast
import copy

from programy.utils.logging.ylogger import YLogger

from programy.storage.factory import StorageFactory
from programy.utils.language.japanese import JapaneseLanguage


class RestParameters(object):

    AVAILABLE_METHOD = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

    def __init__(self, host=None):
        self._host = None
        self._method = 'GET'
        self._query = {}
        self._header = {}
        self._body = None

        if host is not None:
            host = host.strip()
            if host != '':
                self._host = host

    @property
    def host(self):
        return self._host

    @property
    def method(self):
        return self._method

    @property
    def query(self):
        return self._query

    @property
    def header(self):
        return self._header

    @property
    def body(self):
        return self._body

    def change_host(self, host):
        if host is not None:
            host = host.strip()
            if host == '':
                return False
            self._host = host
        return True

    def set_method(self, method):
        if method is not None:
            method = method.strip()
            if method == '':
                self._method = 'GET'
            else:
                method = method.upper()
                if method in self.AVAILABLE_METHOD:
                    self._method = method
                else:
                    return False
        return True

    def set_query(self, query):
        if query is not None:
            try:
                query_dict = ast.literal_eval("{" + query + "}")
                for key in query_dict.keys():
                    if key == '':
                        return False
                self._query = query_dict
            except Exception:
                return False
        return True

    def set_header(self, header):
        if header is not None:
            try:
                header_dict = ast.literal_eval("{" + header + "}")
                new_dict = {}
                for key, value in header_dict.items():
                    if key == '':
                        return False
                    if value is None:
                        continue
                    if type(value) is not str:
                        return False
                    new_dict[key] = value

                self._header = new_dict
            except Exception:
                return False
        return True

    def set_body(self, body):
        self._body = body

    def join_query(self, query):
        if len(self._query) == 0:
            return self.set_query(query)

        new_query, success = self._cocatenate_dict(self._query, query)
        if success is True:
            self._query = new_query
        return success

    def join_header(self, header):
        if len(self._header) == 0:
            return self.set_header(header)

        if header is not None:
            try:
                header_dict = ast.literal_eval("{" + header + "}")
                for key, value in header_dict.items():
                    if value is not None:
                        if type(value) is not str:
                            return False
            except Exception:
                return False

        new_header, success = self._cocatenate_dict(self._header, header)
        if success is True:
            self._header = new_header
        return success

    def join_body(self, body):
        if self._body is None:
            self.set_body(body)
            return

        if body is None:
            return
        if body == '':
            self._body = None
            return

        try:
            org_body = json.loads(self._body)
        except Exception:
            org_body = self._body

        try:
            join_body = json.loads(body)
        except Exception:
            join_body = body

        if type(org_body) is dict and type(join_body) is dict:
            for key, value in join_body.items():
                if value is None:
                    if key in org_body.keys():
                        del org_body[key]
                        continue
                org_body[key] = value
            if len(org_body) == 0:
                self._body = None
            else:
                self._body = json.dumps(org_body, ensure_ascii=False)
        else:
            if type(join_body) is dict:
                self._body = json.dumps(join_body, ensure_ascii=False)
            else:
                self._body = join_body

    def _cocatenate_dict(self, self_dict, option):
        if option is None:
            return self_dict, True

        try:
            option_dict = ast.literal_eval("{" + option + "}")
            if len(option_dict) == 0:
                return {}, True

            for key in option_dict.keys():
                if key == '':
                    return None, False
        except Exception:
            return None, False

        new_dict = copy.copy(self_dict)
        for key, value in option_dict.items():
            if key in self_dict:
                if value is None:
                    del new_dict[key]
                else:
                    new_dict[key] = value
            else:
                if value is not None:
                    new_dict[key] = value
        return new_dict, True


class RestTemplatesCollection(object):

    def __init__(self, errors_dict=None):
        self._templates = {}

        if errors_dict is None:
            self._errors_dict = None
        else:
            errors_dict['rest_templates'] = []
            self._errors_dict = errors_dict['rest_templates']

    @property
    def templates(self):
        return self._templates

    def empty(self):
        self._templates.clear()

    def rest_template(self, name):
        template_name = JapaneseLanguage.zenhan_normalize(name)
        template_name = template_name.upper()
        if template_name in self._templates:
            return self._templates[template_name]
        return None

    def set_error_info(self, filename, idx, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'index': idx, 'description': description}
            self._errors_dict.append(error_info)

    def make_rest_params(self, host):
        params = RestParameters(host)
        return params

    def add_rest_template(self, name, params, filename, idx):
        template_name = JapaneseLanguage.zenhan_normalize(name)
        template_name = template_name.upper()
        if template_name not in self._templates:
            self._templates[template_name] = params
        else:
            error_info = "duplicate template_name='%s' (host='%s' is invalid)" % (name, params.host)
            self.set_error_info(filename, idx, error_info)
            return

    def remove(self, name):
        template_name = JapaneseLanguage.zenhan_normalize(name)
        template_name = template_name.upper()
        self._templates.pop(template_name, None)

    def contains(self, name):
        template_name = JapaneseLanguage.zenhan_normalize(name)
        template_name = template_name.upper()
        return bool(template_name in self._templates)

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.REST_TEMPLATES) is True:
            templates_store_engine = storage_factory.entity_storage_engine(StorageFactory.REST_TEMPLATES)
            if templates_store_engine:
                try:
                    templates_store = templates_store_engine.rest_templates_store()
                    templates_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load REST-Template from storage", e)

        return len(self._templates)

    def reload(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.REST_TEMPLATES) is True:
            templates_engine = storage_factory.entity_storage_engine(StorageFactory.REST_TEMPLATES)
            if templates_engine:
                try:
                    templates_store = templates_engine.rest_templates_store()
                    templates_store.reload(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load REST-Template from storage", e)
