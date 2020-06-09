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

from programy.mappings.base import DoubleStringCharSplitCollection
from programy.storage.factory import StorageFactory


class BasePropertiesCollection(DoubleStringCharSplitCollection):

    def __init__(self, errors_dict=None):
        DoubleStringCharSplitCollection.__init__(self)
        self._errors_dict = errors_dict

    def get_split_char(self):
        return ":"

    def has_property(self, key):
        return self.has_keyVal(key)

    def property(self, key):
        return self.value(key)

    def set_error_info(self, filename, line, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'line': line, 'description': description}
            self._errors_dict.append(error_info)

    def add_property(self, key, value, filename=None, line=0):
        if key == '':
            error_info = "key is empty"
            self.set_error_info(filename, line, error_info)
            return

        if self.has_property(key) is False:
            self.pairs.append([key, value])
        else:
            error_info = "duplicate key='%s' (value='%s' is invalid)" % (key, value)
            self.set_error_info(filename, line, error_info)

    def set_property(self, key, value):
        if self.has_property(key):
            self.set_value(key, value)
        else:
            self.pairs.append([key, value])

    def get_storage_name(self):
        raise NotImplementedError()

    def get_store(self, engine):
        raise NotImplementedError()

    def load(self, storage_factory):
        name = self.get_storage_name()
        if storage_factory.entity_storage_engine_available(name) is True:
            engine = storage_factory.entity_storage_engine(name)
            if engine:
                try:
                    store = self.get_store(engine)
                    store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load %s from storage", e, name)

    def reload_file(self, storage_factory):
        self.load(storage_factory)


class PropertiesCollection(BasePropertiesCollection):

    def __init__(self, errors_dict=None):
        if errors_dict is None:
            self._errors = None
        else:
            errors_dict['properties'] = []
            self._errors = errors_dict['properties']
        BasePropertiesCollection.__init__(self, self._errors)

    def get_storage_name(self):
        return StorageFactory.PROPERTIES

    def get_store(self, engine):
        return engine.property_store()


class DefaultVariablesCollection(BasePropertiesCollection):

    def __init__(self, errors_dict=None):
        if errors_dict is None:
            self._errors = None
        else:
            errors_dict['defaults'] = []
            self._errors = errors_dict['defaults']
        BasePropertiesCollection.__init__(self, self._errors)

    def get_storage_name(self):
        return StorageFactory.DEFAULTS

    def get_store(self, engine):
        return engine.defaults_store()

    def has_variable(self, key):
        return self.has_property(key)

    def variable(self, key):
        return self.property(key)

    def add_variable(self, key, value):
        self.add_property(key, value)


class RegexTemplatesCollection(BasePropertiesCollection):

    def __init__(self, errors_dict=None):
        if errors_dict is None:
            self._errors = None
        else:
            errors_dict['regex_templates'] = []
            self._errors = errors_dict['regex_templates']
        BasePropertiesCollection.__init__(self, self._errors)

    def get_storage_name(self):
        return StorageFactory.REGEX_TEMPLATES

    def get_store(self, engine):
        return engine.regex_store()

    def has_regex(self, key):
        return self.has_property(key)

    def regex(self, key):
        return self.property(key)

    def add_regex(self, key, value):
        self.add_property(key, value)
