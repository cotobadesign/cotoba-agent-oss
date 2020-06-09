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
import json
import codecs
import iso8601

from programy.utils.logging.ylogger import YLogger
from programy.context import ClientContext
from programy.clients.restful.yadlan.config import YadlanRestConfiguration
from programy.clients.restful.client import RestBotClient


class YadlanRestBotClient(RestBotClient):

    def __init__(self, id, argument_parser=None):
        RestBotClient.__init__(self, id, argument_parser)
        self.initialise()

        bot_name = "defaultbot"
        try:
            bot = self._bot_factory.select_bot()
            brain = bot._brain_factory.select_brain()
            bot_name = brain.configuration.bot_name

            YLogger.set_prefix(bot_name)
        except Exception:
            pass

        self._server_mode = True  # if Not Server-Mode then change to comment line.
        YLogger.set_stdout(self.arguments.args.stdoutlog)
        YLogger.set_traceback(False)

    def get_client_configuration(self):
        return YadlanRestConfiguration("yadlan")

    def get_request_body(self, rest_request):
        raise NotImplementedError()

    def get_api_key(self, rest_request):
        if 'apikey' not in rest_request.args or rest_request.args['apikey'] is None:
            return None
        return rest_request.args['apikey']

    def server_abort(self, error_code, error_msg):
        self._status_code = error_code
        self._error_msg = error_msg
        raise Exception('ServerError: %s, status_code=%s', error_msg, error_code)

    def get_parameter(self, rest_request, key):
        bodydata = self.get_request_body(rest_request)
        if len(bodydata) == 0:
            errMsg = "Missing Request Data"
            YLogger.error(self, key + " " + errMsg)
            self.server_abort(400, errMsg)
        try:
            dialogRequest = codecs.decode(bodydata, "utf_8")
            dialogDict = json.loads(dialogRequest)
        except Exception as excep:
            errMsg = "Request is not JSON-format"
            YLogger.exception(self, key + " " + errMsg, excep)
            self.server_abort(400, errMsg)

        response = "None"
        try:
            if len(format(dialogDict[key])) != 0:
                response = dialogDict[key]
        except Exception:
            YLogger.debug(self, "user data " + key + " : is None")

        if response is None:
            response = "None"
        elif type(response) is not str:
            errMsg = "<%s> is not Text : [%s] " % (key, response)
            YLogger.error(self, errMsg)
            self.server_abort(400, errMsg)

        return response

    def get_question(self, rest_request):
        return self.get_parameter(rest_request, 'utterance')

    def get_userid(self, rest_request):
        return self.get_parameter(rest_request, 'userId')

    def get_locale(self, rest_request):
        locale = self.get_parameter(rest_request, 'locale')
        if locale == 'None':
            return locale

        if '-' not in locale:
            errMsg = "<locale> invalid format: [%s]" % locale
            YLogger.error(self, errMsg)
            self.server_abort(400, errMsg)
        else:
            locale_param = locale.split('-')
            if len(locale_param) != 2:
                errMsg = "<locale> invalid format: [%s]" % locale
                YLogger.error(self, errMsg)
                self.server_abort(400, errMsg)
            else:
                if len(locale_param[0]) != 2 and len(locale_param[0]) != 3:
                    errMsg = "<locale> invalid lunguage_code: [%s]" % locale
                    YLogger.error(self, errMsg)
                    self.server_abort(400, errMsg)
                if len(locale_param[1]) != 2 and len(locale_param[1]) != 3:
                    errMsg = "<locale> invalid country_code: [%s]" % locale
                    YLogger.error(self, errMsg)
                    self.server_abort(400, errMsg)
                if locale_param[0].islower() is False:
                    errMsg = "<locale> lunguage_code is not lower: [%s]" % locale
                    YLogger.error(self, errMsg)
                    self.server_abort(400, errMsg)
                if locale_param[1].isupper() is False:
                    errMsg = "<locale> country_code is not upper: [%s]" % locale
                    YLogger.error(self, errMsg)
                    self.server_abort(400, errMsg)

        return locale

    def get_time(self, rest_request):
        time_param = self.get_parameter(rest_request, 'time')
        if time_param != 'None':
            try:
                iso8601.parse_date(time_param)
            except Exception:
                errMsg = "<time> datetime parser error: [%s]" % time_param
                YLogger.error(self, errMsg)
                self.server_abort(400, errMsg)

        return time_param

    def get_topic(self, rest_request):
        return self.get_parameter(rest_request, 'topic')

    def get_deleteVariable(self, rest_request):
        bodydata = self.get_request_body(rest_request)
        key = 'deleteVariable'
        if len(bodydata) == 0:
            errMsg = "Missing Request Data"
            YLogger.error(self, key + " " + errMsg)
            self.server_abort(400, errMsg)
        try:
            dialogRequest = codecs.decode(bodydata, 'utf_8')
            dialogDict = json.loads(dialogRequest)
        except Exception as excep:
            errMsg = "Request is not JSON-format"
            YLogger.exception(self, key + " " + errMsg, excep)
            self.server_abort(400, errMsg)

        response = False
        try:
            if len(format(dialogDict[key])) != 0:
                response = dialogDict[key]
        except Exception:
            YLogger.debug(self, "user data " + key + " : is None")

        if response is None:
            response = False
        elif type(response) is not bool:
            errMsg = "<%s> is not bool : [%s] " % (key, response)
            YLogger.error(self, errMsg)
            self.server_abort(400, errMsg)

        return response

    def get_metadata(self, rest_request):
        bodydata = self.get_request_body(rest_request)
        if len(bodydata) == 0:
            errMsg = "Missing Request Data"
            YLogger.error(self, "metadata " + errMsg)
            self.server_abort(400, errMsg)
        try:
            dialogRequest = codecs.decode(bodydata, 'utf_8')
            dialogDict = json.loads(dialogRequest)
        except Exception as excep:
            errMsg = "Request is not JSON-format"
            YLogger.exception(self, "metadata " + errMsg, excep)
            self.server_abort(400, errMsg)

        try:
            metadata = dialogDict["metadata"]
        except Exception:
            YLogger.debug(self, "user data metadata : is None")
            return 'None'

        if metadata is None:
            response = 'null'
        elif type(metadata) is str:
            response = metadata
        else:
            response = json.dumps(metadata, ensure_ascii=False)

        return response

    def get_config_option(self, rest_request, optionKey):
        bodydata = self.get_request_body(rest_request)
        key = 'config'
        if len(bodydata) == 0:
            errMsg = "Missing Request Data"
            YLogger.error(self, key + " " + errMsg)
            self.server_abort(400, errMsg)
        try:
            dialogRequest = codecs.decode(bodydata, "utf_8")
            dialogDict = json.loads(dialogRequest)
        except Exception as excep:
            errMsg = "Request is not JSON-format"
            YLogger.exception(self, key + " " + errMsg, excep)
            self.server_abort(400, errMsg)

        response = None
        try:
            optionDict = dialogDict[key]
            if len(format(optionDict[optionKey])) != 0:
                response = optionDict[optionKey]
        except Exception:
            YLogger.debug(self, "config-option:" + key + " : is None")
        return response

    def get_variables(self, rest_request):
        bodydata = self.get_request_body(rest_request)
        key = 'variables'
        if len(bodydata) == 0:
            errMsg = "Missing Request Data"
            YLogger.error(self, key + " " + errMsg)
            self.server_abort(400, errMsg)

        try:
            dialogRequest = codecs.decode(bodydata, "utf_8")
            dialogDict = json.loads(dialogRequest)
        except Exception as excep:
            errMsg = "Request is not JSON-format"
            YLogger.exception(self, key + " " + errMsg, excep)
            self.server_abort(400, errMsg)

        try:
            response = json.dumps(dialogDict["variables"], ensure_ascii=False)
        except Exception:
            response = 'None'
            YLogger.debug(self, "variables is Not JSON format")

        return response

    def get_reset_param(self, rest_request):
        return self.get_parameter(rest_request, 'reset')

    def get_errors_param(self, rest_request):
        bodydata = self.get_request_body(rest_request)
        key = 'errors_collection'
        if len(bodydata) == 0:
            errMsg = "Missing Request Data"
            YLogger.error(self, key + " " + errMsg)
            self.server_abort(400, errMsg)
        try:
            dialogRequest = codecs.decode(bodydata, 'utf_8')
            dialogDict = json.loads(dialogRequest)
        except Exception as excep:
            errMsg = "Request is not JSON-format"
            YLogger.exception(self, key + " " + errMsg, excep)
            self.server_abort(400, errMsg)

        response = False
        try:
            if len(format(dialogDict[key])) != 0:
                response = dialogDict[key]
        except Exception:
            YLogger.debug(self, "user data " + key + " : is None")

        if response is None:
            response = False
        elif type(response) is not bool:
            response = False

        return response

    def create_response(self, request, response_data, status, latency):
        self.dump_request_response(request, response_data, latency)
        return response_data

    def checkBotVersion(self, version):
        bot = self._bot_factory.select_bot()
        if bot.configuration.version is not None:
            if bot.configuration.version == version:
                return True
        return False

    def dump_request_response(self, request, response, latency):
        bodydata = self.get_request_body(request)
        requestDict = {}
        if len(bodydata) != 0:
            try:
                requestDict = json.loads(codecs.decode(bodydata, "utf_8"), encoding="utf-8")
            except Exception:
                YLogger.debug(self, "request is Not JSON format")
                pass
        logdataDict = {"latency": latency, "request": requestDict, "response": response}
        if len(requestDict) > 0:
            try:
                userId = self.get_userid(request)
                client_context = self.create_client_context(userId)
                YLogger.info(client_context, json.dumps(logdataDict, ensure_ascii=False))
            except Exception:
                pass

    def save_data_before_exit(self):
        client_context = ClientContext(self, None)
        client_context.bot = self._bot_factory.select_bot()
        client_context.brain = client_context.bot._brain_factory.select_brain()
        #  client_context.brain.rdf.save_rdf_data()
