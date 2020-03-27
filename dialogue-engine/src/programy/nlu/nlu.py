
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
from programy.utils.classes.loader import ClassLoader
from programy.config.brain.nlu import BrainNluConfiguration


class NluRequest(object):

    def __init__(self, nlu_configration):
        assert (nlu_configration is not None)
        assert (isinstance(nlu_configration, BrainNluConfiguration))

        self._configuration = nlu_configration

    def nluCall(self, client_context, url, apikey, utterance):
        raise NotImplementedError()

    @staticmethod
    def load_nlu(nlu_config):
        if nlu_config.classname is not None:
            try:
                YLogger.debug(None, "Loading nluRequest from class [%s]", nlu_config.classname)
                nlu_class = ClassLoader.instantiate_class(nlu_config.classname)
                nlu = nlu_class(nlu_config)
                return nlu
            except Exception as excep:
                YLogger.exception(None, "Failed to initiate nlu", excep)
        else:
            YLogger.warning(None, "No configuration setting for nlu!")

        return None
