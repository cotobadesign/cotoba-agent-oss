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
from programy.utils.logging.ylogger import YLogger
from abc import ABCMeta, abstractmethod

from programy.clients.client import BotClient
from programy.clients.restful.config import RestConfiguration
from programy.storage.factory import StorageFactory


class RestBotClient(BotClient):
    __metaclass__ = ABCMeta

    def __init__(self, id, argument_parser=None):
        BotClient.__init__(self, id, argument_parser)
        self.api_keys = []
        self._status_code = 200
        self._error_msg = ''

    def get_client_configuration(self):
        return RestConfiguration(self.id)

    def load_api_keys(self):
        if self.configuration.client_configuration.use_api_keys is True:
            if self.configuration.client_configuration.api_key_file is not None:
                try:
                    with open(self.configuration.client_configuration.api_key_file, "r", encoding="utf-8") as api_key_file:
                        for api_key in api_key_file:
                            self.api_keys.append(api_key.strip())

                except Exception as excep:
                    YLogger.exception(self, "Failed to open license key file [%s]", excep, self.configuration.client_configuration.api_key_file)

    def initialise(self):
        self.load_api_keys()

    @abstractmethod
    def get_request_body(self, rest_request):
        return None

    @abstractmethod
    def get_api_key(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_question(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_userid(self, rest_request):
        raise NotImplementedError()

    @abstractmethod
    def get_locale(self, rest_request):
        return ""

    @abstractmethod
    def get_time(self, rest_request):
        return ""

    @abstractmethod
    def get_topic(self, rest_request):
        return ""

    @abstractmethod
    def get_metadata(self, rest_request):
        return ""

    @abstractmethod
    def get_deleteVariable(self, rest_request):
        return False

    @abstractmethod
    def get_config_option(self, rest_request, option):
        return None

    @abstractmethod
    def get_variables(self, rest_request):
        return None

    @abstractmethod
    def get_reset_param(self, rest_request):
        return None

    @abstractmethod
    def create_response(self, response, status):
        raise NotImplementedError()

    def is_apikey_valid(self, apikey):
        return bool(apikey in self.api_keys)

    def verify_api_key_usage(self, request):
        if self.configuration.client_configuration.use_api_keys is True:

            apikey = self.get_api_key(request)

            if apikey is None:
                YLogger.error(self, "Unauthorised access - api required but missing")
                return {'error': 'Unauthorized access'}, 401

            if self.is_apikey_valid(apikey) is False:
                YLogger.error(self, "'Unauthorised access - invalid api key")
                return {'error': 'Unauthorized access'}, 401

        return None, None

    def format_success_response(self, userid, question, answer, userInfo):
        if userInfo is None:
            return {"utterance": question, "response": answer, "userId": userid}
        else:
            response_dic = {"utterance": question, "response": answer, "topic": userInfo.get("topic")}
            response_userid = userInfo.get("__USER_USERID__")
            if response_userid is None or response_userid == '':
                response_dic["userId"] = ""
            else:
                response_dic["userId"] = response_userid
            metadata = userInfo.get("__SYSTEM_METADATA__")
            if metadata is not None and metadata != '':
                response_dic["metadata"] = metadata
            return response_dic

    def format_error_response(self, userid, question, error, userInfo):
        client_context = self.create_client_context(userid)
        if userInfo is None:
            return {"utterance": question, "response": client_context.bot.get_default_response(client_context), "userId": userid, "error": error}
        else:
            response_dic = {"utterance": question, "response": client_context.bot.get_default_response(client_context),
                            "topic": userInfo.get("topic"), "error": error}
            response_userid = userInfo.get("__USER_USERID__")
            if response_userid is None or response_userid == '':
                response_dic["userId"] = ""
            else:
                response_dic["userId"] = response_userid
            metadata = userInfo.get("__SYSTEM_METADATA__")
            if metadata is not None and metadata != '':
                response_dic["metadata"] = metadata
            return response_dic

    def ask_question(self, userid, question, userInfo, deleteVariable, loglevel, nlu_latency=True):
        response = ""
        utterance = ""
        try:
            client_context = self.create_client_context(userid)
            client_context.userInfo = userInfo
            client_context.deleteVariable = deleteVariable
            client_context.log_level = loglevel
            client_context.nlu_latency = nlu_latency
            client_context.server_mode = getattr(self, '_server_mode', False)

            response = client_context.bot.ask_question(client_context, question, responselogger=self)
            utterance = client_context.bot.utterance
        except Exception as e:
            YLogger.exception(self, "ask_question Exception:", e)
        return response, utterance

    def get_config_loglevel(self, rest_request):
        level = self.get_config_option(rest_request, 'logLevel')
        if level is not None:
            if type(level) is not str:
                self._status_code = 400
                error_msg = "<loglevel> is not text : [%s] " % level
                raise Exception('ServerError: %s, status_code=%s', error_msg, self._status_code)
            elif level not in ['none', 'error', 'warning', 'info', 'debug']:
                self._status_code = 400
                error_msg = "<loglevel> is invalid : [%s] " % level
                raise Exception('ServerError: %s, status_code=%s', error_msg, self._status_code)
        return level

    def get_config_nlu_latency(self, rest_request):
        latency = self.get_config_option(rest_request, 'nlu_latency')
        if latency is not None:
            if type(latency) is bool:
                return latency
            elif type(latency) is str:
                latency = latency.upper()
                if latency == "FALSE":
                    return False
        return True

    def process_request(self, request):
        question = "Unknown"
        userid = "Unknown"
        userInfo = None
        self._status_code = 200
        self._error_msg = ''
        try:
            response, status = self.verify_api_key_usage(request)
            if response is not None:
                return response, status

            question = self.get_question(request)
            userid = self.get_userid(request)
            if question == "None" or userid == "None":
                return {'error': 'No Mandatory parameter'}, 400
            userInfo = UserInfo(self, request)
            deleteVariable = self.get_deleteVariable(request)
            loglevel = self.get_config_loglevel(request)
            nlu_latency = self.get_config_nlu_latency(request)

            answer, utterance = self.ask_question(userid, question, userInfo, deleteVariable, loglevel, nlu_latency)
            if utterance is not None:
                question = utterance

            return self.format_success_response(userid, question, answer, userInfo), 200

        except Exception as excep:
            if self._status_code == 200:
                return self.format_error_response(userid, question, str(excep), userInfo), 500
            else:
                return {'error': self._error_msg}, self._status_code

    def process_debug_request(self, request):
        userid = 'None'
        variables = 'None'
        reset_data = 'None'
        debugInfo = {}
        self._status_code = 200
        self._error_msg = ''

        try:
            bodydata = self.get_request_body(request)
            if len(bodydata) > 0:
                userid = self.get_userid(request)
                variables = self.get_variables(request)
                reset_data = self.get_reset_param(request)
        except Exception:
            pass

        client_context = self.create_client_context(userid)
        client_context.server_mode = getattr(self, '_server_mode', False)

        if reset_data != 'None':
            if userid == 'None':
                return {'error': 'Failed need userId for reset'}, 400

            if reset_data == 'conversation':
                result = client_context.bot.conversations.reset_conversation_data(client_context)
                if result is False:
                    return {'reset': 'Failed'}, 200
                return {'reset': 'Succeeded'}, 200
            elif reset_data == 'learn':
                result = client_context.bot.conversations.reset_learn_categories(client_context)
                if result is False:
                    return {'reset': 'Failed'}, 200
                return {'reset': 'Succeeded'}, 200
            elif reset_data == 'all':
                result = client_context.bot.conversations.reset_learn_categories(client_context)
                if result is False:
                    return {'reset': 'Failed'}, 200
                result = client_context.bot.conversations.reset_conversation_data(client_context)
                if result is False:
                    return {'reset': 'Failed'}, 200
                return {'reset': 'Succeeded'}, 200
            else:
                return {'error': 'Failed invalid reset target'}, 400

        if userid != 'None' and variables != 'None':
            try:
                variableDict = json.loads(variables)
                if len(variableDict) > 0:
                    client_context.bot.conversations.set_conversation_valiables(client_context, variableDict)
            except Exception:
                return {'error': 'Invalid variables list format'}, 400

        try:
            errors = self.get_errors(client_context)
            if errors is not None:
                debugInfo.update(errors)
        except Exception:
            return {'error': 'Load errors failed'}, 500

        try:
            duplicates = self.get_duplicates(client_context)
            if duplicates is not None:
                debugInfo.update(duplicates)
        except Exception:
            return {'error': 'Load duplicates failed'}, 500

        try:
            errors_collection = self.get_errors_collection(client_context)
            if errors_collection is not None:
                debugInfo.update(errors_collection)
        except Exception:
            pass

        if userid == 'None':
            return debugInfo, 200

        try:
            conversations, current_data = self.get_conversations(client_context)
            if conversations is not None and len(conversations) > 0:
                for key, val in conversations["conversations"]["properties"].items():
                    try:
                        jsondata = json.loads(val)
                        conversations["conversations"]["properties"][key] = jsondata
                    except Exception:
                        pass

                for key, val in conversations["conversations"]["data_properties"].items():
                    try:
                        jsondata = json.loads(val)
                        conversations["conversations"]["data_properties"][key] = jsondata
                    except Exception:
                        pass

                for i, question in enumerate(conversations["conversations"]["questions"]):
                    try:
                        for key, val in question["data_properties"].items():
                            try:
                                jsondata = json.loads(val)
                                conversations["conversations"]["questions"][i]["data_properties"][key] = jsondata
                            except Exception:
                                pass
                        for key, val in question["name_properties"].items():
                            try:
                                jsondata = json.loads(val)
                                conversations["conversations"]["questions"][i]["name_properties"][key] = jsondata
                            except Exception:
                                pass
                        for key, val in question["var_properties"].items():
                            try:
                                jsondata = json.loads(val)
                                conversations["conversations"]["questions"][i]["var_properties"][key] = jsondata
                            except Exception:
                                pass
                    except Exception:
                        pass

                debugInfo.update(conversations)

            if current_data is not None and len(current_data) > 0:
                current_info = {'current_conversation': current_data}
                debugInfo.update(current_info)

        except Exception:
            return {'error': 'Load conversations failed'}, 500

        try:
            logs = self.get_logs(client_context)
            if logs is not None:
                debugInfo.update(logs)
        except Exception:
            return {'error': 'Load logdatas failed'}, 500

        return debugInfo, 200

    def get_errors(self, client_context):
        errors = None
        if client_context.brain.configuration.debugfiles.save_errors is True:
            if self.storage_factory.entity_storage_engine_available(StorageFactory.ERRORS) is True:
                errors_engine = self.storage_factory.entity_storage_engine(StorageFactory.ERRORS)
                if errors_engine:
                    errors_store = errors_engine.errors_store()
                    errors = errors_store.load_errors()

        return errors

    def get_duplicates(self, client_context):
        duplicates = None
        if client_context.brain.configuration.debugfiles.save_duplicates is True:
            if self.storage_factory.entity_storage_engine_available(StorageFactory.DUPLICATES) is True:
                duplicates_engine = self.storage_factory.entity_storage_engine(StorageFactory.DUPLICATES)
                if duplicates_engine:
                    duplicates_store = duplicates_engine.duplicates_store()
                    duplicates = duplicates_store.load_duplicates()

        return duplicates

    def get_errors_collection(self, client_context):
        errors_collection = None
        if client_context.brain.configuration.debugfiles.save_errors_collection is True:
            if self.storage_factory.entity_storage_engine_available(StorageFactory.ERRORS_COLLECTION) is True:
                errors_collection_engine = self.storage_factory.entity_storage_engine(StorageFactory.ERRORS_COLLECTION)
                if errors_collection_engine:
                    errors_collection_store = errors_collection_engine.errors_collection_store()
                    errors_collection = errors_collection_store.load_errors_collection()

        return errors_collection

    def get_conversations(self, client_context):
        conversations = None
        current_info = None
        if self.storage_factory.entity_storage_engine_available(StorageFactory.CONVERSATIONS) is True:
            converstion_engine = self.storage_factory.entity_storage_engine(StorageFactory.CONVERSATIONS)
            if converstion_engine:
                conversation_store = converstion_engine.conversation_store()
                conversations, current_info = conversation_store.debug_conversation_data(client_context)

        return conversations, current_info

    def get_logs(self, client_context):
        logs = None
        if self.storage_factory.entity_storage_engine_available(StorageFactory.LOGS) is True:
            logs_engine = self.storage_factory.entity_storage_engine(StorageFactory.LOGS)
            if logs_engine:
                logs_store = logs_engine.logs_store()
                logs = logs_store.load_logs(client_context)

        return logs


class UserInfo(RestBotClient):

    def __init__(self, restClient, request):

        if restClient is None or request is None:
            self._userInfo = {
                "topic": "*",
                "__USER_LOCALE__": "None",
                "__USER_TIME__": "None",
                "__USER_METADATA__": "None",
                "__USER_USERID__": "None",
                "__USER_UTTERANCE__": "None",
                "__SYSTEM_NLUDATA__": "",
                "__SYSTEM_METADATA__": ""
            }
            return

        self._userInfo = {
            "topic": restClient.get_topic(request),
            "__USER_LOCALE__": restClient.get_locale(request),
            "__USER_TIME__": restClient.get_time(request),
            "__USER_METADATA__": restClient.get_metadata(request),
            "__USER_USERID__": restClient.get_userid(request),
            "__USER_UTTERANCE__": restClient.get_question(request),
            "__SYSTEM_NLUDATA__": "",
            "__SYSTEM_METADATA__": ""
        }

    def getUserInfo(self):
        return self._userInfo

    def set(self, key, value):
        response = False
        try:
            self._userInfo[key] = value
            response = True
        except Exception as e:
            YLogger.exception(self, "UserInfo.set %s:%s", key, e)

        return response

    def get(self, key):
        response = ""
        try:
            response = self._userInfo[key]
        except Exception as e:
            YLogger.exception(self, "UserInfo.get %s:%s", key, e)

        return response

    def userInfoPreProcessor(self, context, srai):

        conversation = context.bot.get_conversation(context)

        try:
            userInfoDict = context.userInfo.getUserInfo()

            for key in userInfoDict.keys():
                if key == 'topic':
                    if srai is False and userInfoDict[key] != "None":
                        conversation.set_property(key, userInfoDict[key])
                elif key == "__SYSTEM_METADATA__":
                    try:
                        if userInfoDict[key] != '':
                            if type(userInfoDict[key]) is dict:
                                conversation.current_question().set_property(key, json.dumps(userInfoDict[key], ensure_ascii=False))
                            else:
                                conversation.current_question().set_property(key, userInfoDict[key])
                        else:
                            conversation.current_question().set_property(key, '')
                    except Exception as e:
                        YLogger.exception(self, "UserInfoPreProcessor __SYSTEM_METADATA__ is not JSON: ", e)
                        conversation.current_question().set_property(key, "")
                else:
                    conversation.current_question().set_property(key, userInfoDict[key])

        except Exception as e:
            YLogger.exception(self, "UserInfoPreProcessor Reason: ", e)

        return

    def userInfoPostProcessor(self, context):

        conversation = context.bot.get_conversation(context)

        try:
            userInfoDict = context.userInfo.getUserInfo()

            for key in userInfoDict.keys():
                if key == 'topic':
                    userInfoDict[key] = conversation.property(key)
                elif key == '__SYSTEM_METADATA__':
                    metadata = conversation.current_question().property(key)
                    if metadata is None:
                        metadata = ''
                    try:
                        userInfoDict[key] = json.loads(metadata)
                        if type(userInfoDict[key]) is str:
                            userInfoDict[key] = metadata
                    except Exception:
                        userInfoDict[key] = metadata
                else:
                    value = conversation.current_question().property(key)
                    if value is None:
                        value = ''
                    userInfoDict[key] = value
        except Exception as e:
            YLogger.exception(self, "UserInfoPostProcessor Reason: ", e)

        return
