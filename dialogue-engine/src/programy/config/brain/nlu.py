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
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

from programy.config.base import BaseConfigurationData
from programy.utils.substitutions.substitues import Substitutions


class BrainNluConfiguration(BaseConfigurationData):

    DEFAULT_CLASSNAME = "programy.nlu.nlu.NluRequest"
    DEFAULT_URL = "http://localhost:3000/run"
    DEFAULT_APIKEY = ""
    DEFAULT_USE_FILE = False

    def __init__(self):
        BaseConfigurationData.__init__(self, name="nlu")
        self._classname = BrainNluConfiguration.DEFAULT_CLASSNAME
        self._url = BrainNluConfiguration.DEFAULT_URL
        self._apikey = BrainNluConfiguration.DEFAULT_APIKEY
        self._use_file = BrainNluConfiguration.DEFAULT_USE_FILE

    @property
    def classname(self):
        return self._classname

    @property
    def url(self):
        return self._url

    @property
    def apikey(self):
        return self._apikey

    @property
    def use_file(self):
        return self._use_file

    def check_for_license_keys(self, license_keys):
        BaseConfigurationData.check_for_license_keys(self, license_keys)

    def load_config_section(self, configuration_file, configuration, bot_root, subs: Substitutions = None):
        nlu = configuration_file.get_section(self._section_name, configuration)
        if nlu is not None:
            self._classname = configuration_file.get_option(nlu, "classname", missing_value=BrainNluConfiguration.DEFAULT_CLASSNAME, subs=subs)
            self._url = configuration_file.get_option(nlu, "url", missing_value=BrainNluConfiguration.DEFAULT_URL, subs=subs)
            self._apikey = configuration_file.get_option(nlu, "apikey", missing_value=BrainNluConfiguration.DEFAULT_APIKEY, subs=subs)
            self._use_file = configuration_file.get_bool_option(nlu, "use_file", missing_value=BrainNluConfiguration.DEFAULT_USE_FILE, subs=subs)
            if self._apikey == 'None':
                self._apikey = ''
        else:
            YLogger.debug(self, "'nlu' section missing from bot config, using defaults")

    def to_yaml(self, data, defaults=True):
        if defaults is True:
            data['classname'] = BrainNluConfiguration.DEFAULT_CLASSNAME
            data['url'] = BrainNluConfiguration.DEFAULT_URL
            data['apikey'] = BrainNluConfiguration.DEFAULT_APIKEY
            data['use_file'] = BrainNluConfiguration.DEFAULT_USE_FILE
        else:
            data['classname'] = self._classname
            data['url'] = self._url
            data['apikey'] = self._apikey
            data['use_file'] = self._use_file
