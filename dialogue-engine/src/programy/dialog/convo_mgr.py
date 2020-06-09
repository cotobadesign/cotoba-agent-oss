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
from programy.dialog.conversation import Conversation
from programy.storage.factory import StorageFactory
from programy.config.bot.conversations import BotConversationsConfiguration


class ConversationManager(object):

    def __init__(self, conversation_configuration):
        assert (conversation_configuration is not None)
        assert (isinstance(conversation_configuration, BotConversationsConfiguration))

        self._configuration = conversation_configuration
        self._conversation_storage = None
        self._conversations = {}
        self._learnf_storage = None
        self._logs_storage = None
        self._internal_datas = {}

    @property
    def configuration(self):
        return self._configuration

    @property
    def storage(self):
        return self._conversation_storage

    @property
    def conversations(self):
        return self._conversations

    def empty(self):
        self._conversations.clear()

    def initialise(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.CONVERSATIONS) is True:
            converstion_engine = storage_factory.entity_storage_engine(StorageFactory.CONVERSATIONS)
            if converstion_engine:
                self._conversation_storage = converstion_engine.conversation_store()

        if storage_factory.entity_storage_engine_available(StorageFactory.LEARNF) is True:
            storage_engine = storage_factory.entity_storage_engine(StorageFactory.LEARNF)
            self._learnf_storage = storage_engine.learnf_store()

        if storage_factory.entity_storage_engine_available(StorageFactory.LOGS) is True:
            storage_engine = storage_factory.entity_storage_engine(StorageFactory.LOGS)
            self._logs_storage = storage_engine.logs_store()

    def save_conversation(self, client_context):
        if self._conversation_storage is not None:
            if client_context.userid in self._conversations:
                conversation = self._conversations[client_context.userid]
                if len(conversation.questions) > 0:
                    self._conversation_storage.store_conversation(client_context, conversation)
                    if client_context.server_mode is True and self._logs_storage is not None:
                        self._logs_storage.store_logs(client_context, conversation)

    def has_conversation(self, client_context):
        return bool(client_context.userid in self._conversations)

    def get_conversation(self, client_context):

        assert (client_context is not None)
        assert (client_context.userid is not None)

        if client_context.userid in self._conversations:
            YLogger.debug(client_context, "Retrieving conversation for client %s", client_context.userid)
            conversation = self._conversations[client_context.userid]

            # Load existing conversation from cache
            if self.configuration.multi_client:
                if self._conversation_storage is not None:
                    self._conversation_storage.load_conversation(client_context, conversation)

        else:
            YLogger.debug(client_context, "Creating new conversation for client %s", client_context.userid)

            conversation = Conversation(client_context)

            conversation.num_categories = client_context.brain.aiml_parser.num_categories

            conversation.load_initial_variables(client_context.brain.default_variables)

            self._conversations[client_context.userid] = conversation

            if self._conversation_storage is not None:
                self._conversation_storage.load_conversation(client_context, conversation)

            if client_context.server_mode is False:
                self.load_learnf_with_userid(client_context)

            if self.configuration.restore_last_topic is True:
                pass

        return conversation

    def remove_conversation(self, client_context):
        if client_context.userid in self._conversations:
            del self._conversations[client_context.userid]

    def load_learnf_with_userid(self, client_context):
        if self._learnf_storage is not None:
            if client_context.userid in self._conversations:
                client_context.brain.aiml_parser.user_categories = 0
                self._learnf_storage.load_learnf(client_context)
                conversation = self._conversations[client_context.userid]
                conversation.user_categories = client_context.brain.aiml_parser.user_categories

    def remove_learnf_with_userid(self, client_context):
        root = client_context.brain.aiml_parser.pattern_parser.root
        root.remove_children_with_userid(client_context.userid)

    def set_conversation_valiables(self, client_context, variables):
        if client_context.userid in self._conversations:
            conversation = self._conversations[client_context.userid]
        else:
            conversation = Conversation(client_context)
            conversation.num_categories = client_context.brain.aiml_parser.num_categories
            conversation.load_initial_variables(client_context.brain.default_variables)
            self._conversations[client_context.userid] = conversation

        if self._conversation_storage is not None:
            self._conversation_storage.load_conversation(client_context, conversation)

        for variable in variables:
            try:
                var_type = variable['type']
                var_key = variable['key']
                var_value = variable['value']
            except Exception:
                raise

            if var_type == 'name':
                YLogger.debug(client_context, "set userid[%s] variable name[%s] = [%s]", client_context.userid, var_key, var_value)
                conversation.set_property(var_key, var_value)
            elif var_type == 'data':
                YLogger.debug(client_context, "set userid[%s] variable data[%s] = [%s]", client_context.userid, var_key, var_value)
                conversation.set_data_property(var_key, var_value)
            else:
                raise Exception('variable type not supported.')

        if self._conversation_storage is not None:
            self._conversation_storage.modify_conversation_data(client_context, conversation)

        if client_context.server_mode is True:
            self.remove_conversation(client_context)

    def reset_conversation_data(self, client_context):
        try:
            self.remove_conversation(client_context)
            self.remove_internal_data(client_context)
            self._conversation_storage.delete_conversation(client_context)
        except Exception:
            return False
        return True

    def reset_learn_categories(self, client_context):
        try:
            self.remove_learnf_with_userid(client_context)
            self._learnf_storage.delete_learnf(client_context)
        except Exception:
            return False
        return True

    def set_internal_data(self, client_context):
        conversation = self._conversations[client_context.userid]
        internal_data = conversation.internal_data
        self._internal_datas[client_context.userid] = internal_data

    def remove_internal_data(self, client_context):
        if client_context.userid in self._internal_datas:
            del self._internal_datas[client_context.userid]
        if client_context.userid in self._conversations:
            conversation = self._conversations[client_context.userid]
            conversation.clear_internal_data()
