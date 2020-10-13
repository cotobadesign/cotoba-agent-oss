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

from programy.processors.processing import PreProcessorCollection
from programy.processors.processing import PostProcessorCollection
from programy.config.brain.brain import BrainConfiguration
from programy.mappings.denormal import DenormalCollection
from programy.mappings.gender import GenderCollection
from programy.mappings.maps import MapCollection
from programy.mappings.nlu import NluCollection
from programy.mappings.botnames import BotNamesCollection
from programy.mappings.resttemplates import RestTemplatesCollection
from programy.mappings.normal import NormalCollection
from programy.mappings.person import PersonCollection
from programy.mappings.person import Person2Collection
from programy.mappings.properties import PropertiesCollection
from programy.mappings.properties import RegexTemplatesCollection
from programy.mappings.properties import DefaultVariablesCollection
from programy.mappings.sets import SetCollection
from programy.dynamic.dynamics import DynamicsCollection
from programy.rdf.collection import RDFCollection
from programy.parser.aiml_parser import AIMLParser
from programy.services.service import ServiceFactory
from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.dialog.sentence import Sentence
from programy.parser.pattern.factory import PatternNodeFactory
from programy.parser.template.factory import TemplateNodeFactory
from programy.binaries import BinariesManager
from programy.braintree import BraintreeManager
from programy.security.manager import SecurityManager
from programy.oob.handler import OOBHandler
from programy.nlu.nlu import NluRequest
from programy.parser.exceptions import LimitOverException
from programy.dialog.convo_vars import ConversationVariables
from programy.storage.factory import StorageFactory

import json


class Brain(object):

    NLU_UTTERANCE = 'NLU_Matching'

    def __init__(self, bot, configuration: BrainConfiguration):

        assert (bot is not None)
        assert (configuration is not None)

        self._bot = bot
        self._configuration = configuration

        self._binaries = BinariesManager(configuration.binaries)
        self._braintree = BraintreeManager(configuration.braintree)
        self._tokenizer = Tokenizer.load_tokenizer(configuration)

        if configuration.debugfiles.save_errors_collection is True:
            errors_dict = {}
        else:
            errors_dict = None

        self._denormal_collection = DenormalCollection(errors_dict)
        self._normal_collection = NormalCollection(errors_dict)
        self._gender_collection = GenderCollection(errors_dict)
        self._person_collection = PersonCollection(errors_dict)
        self._person2_collection = Person2Collection(errors_dict)
        self._rdf_collection = RDFCollection(errors_dict)
        self._sets_collection = SetCollection(errors_dict)
        self._maps_collection = MapCollection(errors_dict)

        self._properties_collection = PropertiesCollection(errors_dict)
        self._default_variables_collection = DefaultVariablesCollection(errors_dict)
        self._botnames_collection = BotNamesCollection(errors_dict)
        self._rest_templates_collection = RestTemplatesCollection(errors_dict)

        self._preprocessors = PreProcessorCollection(errors_dict)
        self._postprocessors = PostProcessorCollection(errors_dict)

        self._pattern_factory = None
        self._template_factory = None

        self._security = SecurityManager(configuration.security)

        self._oobhandler = OOBHandler(configuration.oob)

        self._regex_templates = RegexTemplatesCollection(errors_dict)

        self._dynamics_collection = DynamicsCollection()

        self._aiml_parser = self.load_aiml_parser()

        self._nlu_collection = NluCollection(bot.client, configuration.nlu, errors_dict)
        self._nlu = NluRequest.load_nlu(configuration.nlu)
        self._nlu_utterance = None

        self.load(self.configuration)

        if configuration.debugfiles.save_errors_collection is True:
            storage_factory = self.bot.client.storage_factory
            if storage_factory.entity_storage_engine_available(StorageFactory.ERRORS_COLLECTION) is True:
                errors_collection_engine = storage_factory.entity_storage_engine(StorageFactory.ERRORS_COLLECTION)
                errors_collection_store = errors_collection_engine.errors_collection_store()
                errors_collection_store.save_errors_collection(errors_dict)

    def ylogger_type(self):
        return "brain"

    @property
    def id(self):
        return self._configuration.section_name

    @property
    def bot(self):
        return self._bot

    @property
    def configuration(self):
        return self._configuration

    @property
    def aiml_parser(self):
        return self._aiml_parser

    @property
    def denormals(self):
        return self._denormal_collection

    @property
    def normals(self):
        return self._normal_collection

    @property
    def genders(self):
        return self._gender_collection

    @property
    def persons(self):
        return self._person_collection

    @property
    def person2s(self):
        return self._person2_collection

    @property
    def rdf(self):
        return self._rdf_collection

    @property
    def sets(self):
        return self._sets_collection

    @property
    def maps(self):
        return self._maps_collection

    @property
    def properties(self):
        return self._properties_collection

    @property
    def default_variables(self):
        return self._default_variables_collection

    @property
    def botnames(self):
        return self._botnames_collection

    @property
    def rest_templates(self):
        return self._rest_templates_collection

    @property
    def preprocessors(self):
        return self._preprocessors

    @property
    def postprocessors(self):
        return self._postprocessors

    @property
    def pattern_factory(self):
        return self._pattern_factory

    @property
    def template_factory(self):
        return self._template_factory

    @property
    def regex_templates(self):
        return self._regex_templates

    @property
    def dynamics(self):
        return self._dynamics_collection

    @property
    def tokenizer(self):
        return self._tokenizer

    @property
    def nlu(self):
        return self._nlu

    @property
    def nlu_servers(self):
        return self._nlu_collection

    @property
    def security(self):
        return self._security

    def load_aiml_parser(self):
        self._load_pattern_nodes()
        self._load_template_nodes()
        return AIMLParser(self)

    def load_aiml(self):
        YLogger.debug(self, "Loading aiml source brain")
        self._aiml_parser.load_aiml()

    def reload_aimls(self):
        YLogger.debug(self, "Loading aiml source brain")
        self._aiml_parser.empty()
        self._aiml_parser.load_aiml()

    def load(self, configuration: BrainConfiguration):

        self._load_properties()
        if self.properties.has_property("punctuation_chars") is True:
            self.tokenizer.set_configuration_punctuation_chars(self.properties.property("punctuation_chars"))
        if self.properties.has_property("before_concatenation_rule") is True:
            self.tokenizer.set_configuration_before_concatenation_rule(self.properties.property("before_concatenation_rule"))
        if self.properties.has_property("after_concatenation_rule") is True:
            self.tokenizer.set_configuration_after_concatenation_rule(self.properties.property("after_concatenation_rule"))

        YLogger.debug(self, "Loading collections")
        self.load_collections()

        YLogger.debug(self, "Loading dynamics sets, maps and vars")
        self.load_dynamics()

        YLogger.debug(self, "Loading services")
        self.load_services(configuration)

        load_aiml = True

        if self.configuration.binaries.load_binary is True:
            load_aiml = self._binaries.load_binary(self.bot.client.storage_factory)
            if load_aiml is False:
                self._aiml_parser = self._binaries.get_aiml_parser()

        if load_aiml is True:
            self.load_aiml()
            self._binaries.set_aiml_parser(self._aiml_parser)
            if configuration.binaries.save_binary is True:
                self._binaries.save_binary(self.bot.client.storage_factory)

        YLogger.debug(self, "Loading security services")
        self.load_security_services()

        YLogger.debug(self, "Loading oob processors")
        self._oobhandler.load_oob_processors()

    def dump_brain_tree(self, client_context):
        self._braintree.dump_brain_tree(client_context)

    def _load_denormals(self):
        self._denormal_collection.empty()
        self._denormal_collection.load(self.bot.client.storage_factory)

    def _load_normals(self):
        self._normal_collection.empty()
        self._normal_collection.load(self.bot.client.storage_factory)

    def _load_genders(self):
        self._gender_collection.empty()
        self._gender_collection.load(self.bot.client.storage_factory)

    def _load_persons(self):
        self._person_collection.empty()
        self._person_collection.load(self.bot.client.storage_factory)

    def _load_person2s(self):
        self._person2_collection.empty()
        self._person2_collection.load(self.bot.client.storage_factory)

    def _load_nlu_servers(self):
        self._nlu_collection.empty()
        self._nlu_collection.load(self.bot.client.storage_factory)
        self._nlu_collection.make_match_nlu_list()

    def _load_botnames(self):
        self._botnames_collection.empty()
        self._botnames_collection.load(self.bot.client.storage_factory)

    def _load_rest_templates(self):
        self._rest_templates_collection.empty()
        self._rest_templates_collection.load(self.bot.client.storage_factory)

    def _load_properties(self):
        self._properties_collection.empty()
        self._properties_collection.load(self.bot.client.storage_factory)
        self._properties_collection.load_json(self.bot.client.storage_factory)

    def _load_default_variables(self):
        self._default_variables_collection.empty()
        self._default_variables_collection.load(self.bot.client.storage_factory)

        self._set_system_defined()

    def _set_system_defined(self):
        self.set_sentiment_scores(0.0, 0.5)

    def set_sentiment_scores(self, positivity, subjectivity):
        if self._default_variables_collection.has_variable("positivity") is False:
            self._default_variables_collection.set_value("positivity", str(positivity))

        if self._default_variables_collection.has_variable("subjectivity") is False:
            self._default_variables_collection.set_value("subjectivity", str(subjectivity))

    def _load_maps(self):
        self._maps_collection.empty()
        self._maps_collection.load(self.bot.client.storage_factory)

    def reload_map(self, mapname):
        if self._maps_collection.contains(mapname):
            self._maps_collection.reload(self.bot.client.storage_factory, mapname)

    def _load_sets(self):
        self._sets_collection.empty()
        self._sets_collection.load(self.bot.client.storage_factory)

    def reload_set(self, setname):
        if self._sets_collection.contains(setname):
            self._sets_collection.reload(self.bot.client.storage_factory, setname)

    def _load_rdfs(self):
        self._rdf_collection.empty()
        self._rdf_collection.load(self.bot.client.storage_factory)

    def reload_rdf(self, rdfname):
        if self._rdf_collection.contains(rdfname):
            self._rdf_collection.reload(self.bot.client.storage_factory, rdfname)

    def _load_regex_templates(self):
        self._regex_templates.load(self.bot.client.storage_factory)

    def _load_preprocessors(self):
        self._preprocessors.empty()
        self._preprocessors.load(self.bot.client.storage_factory)

    def _load_postprocessors(self):
        self._postprocessors.empty()
        self._postprocessors.load(self.bot.client.storage_factory)

    def _load_pattern_nodes(self):
        self._pattern_factory = PatternNodeFactory()
        self._pattern_factory.load(self.bot.client.storage_factory)

    def _load_template_nodes(self):
        self._template_factory = TemplateNodeFactory()
        self._template_factory.load(self.bot.client.storage_factory)

    def load_collections(self):
        self._load_denormals()
        self._load_normals()
        self._load_genders()
        self._load_persons()
        self._load_person2s()
        self._load_default_variables()
        self._load_nlu_servers()
        self._load_botnames()
        self._load_rest_templates()
        self._load_rdfs()
        self._load_sets()
        self._load_maps()
        self._load_regex_templates()
        self._load_preprocessors()
        self._load_postprocessors()

    def load_services(self, configuration):
        ServiceFactory.preload_services(configuration.services)

    def load_security_services(self):
        self._security.load_security_services(self.bot.client)

    def load_dynamics(self):
        if self.configuration.dynamics is not None:
            self._dynamics_collection.load_from_configuration(self.configuration.dynamics)
        else:
            YLogger.debug(self, "No dynamics configuration defined...")

    def pre_process_question(self, client_context, question):
        return self.preprocessors.process(client_context, question)

    def post_process_response(self, client_context, response: str):
        return self.postprocessors.process(client_context, response)

    def failed_authentication(self, client_context):
        return self._security.failed_authentication(client_context)

    def authenticate_user(self, client_context):
        return self._security.authenticate_user(client_context)

    def resolve_matched_template(self, client_context, match_context):

        assert (client_context is not None)
        assert (match_context is not None)

        template_node = match_context.template_node()

        YLogger.debug(client_context, "AIML Parser evaluating template [%s]", template_node.to_string())

        response = template_node.template.resolve(client_context)

        if self._oobhandler.oob_in_response(response) is True:
            if client_context.brain.template_factory.exists('oob') is True:
                response = self._oobhandler.handle(client_context, response)
            else:
                YLogger.debug(client_context, "OOB function is disable [%s]", response)

        return response

    def ask_question(self, client_context, sentence, srai=False, default_srai=False):

        assert (client_context is not None)
        assert (client_context.bot is not None)
        assert (self._aiml_parser is not None)

        client_context.brain = self

        authenticated = self.authenticate_user(client_context)
        if authenticated is not None:
            return authenticated

        conversation = client_context.bot.get_conversation(client_context)
        answer = None

        if conversation is not None:
            if srai is False and default_srai is False:
                self._nlu_utterance = None
            try:
                client_context.userInfo.userInfoPreProcessor(client_context, srai)
            except Exception:
                pass

            topic_pattern = conversation.get_topic_pattern(client_context)

            that_pattern = conversation.get_that_pattern(client_context, srai)

            original_base = None
            if default_srai is True and conversation.internal_base is not None:
                original_base = conversation.internal_base
                base = original_base
                if 'srai_histories' not in base:
                    base['srai_histories'] = []
                    default_srai_root = base['srai_histories']
                    default_srai_root.append({})
                    conversation.internal_base = default_srai_root[-1]
                conversation.add_internal_data(conversation.internal_base, 'default_srai', True)
            elif srai is False:
                conversation.internal_data.append({})
                conversation.internal_base = conversation.internal_data[-1]
            base = conversation.internal_base
            texts = self.tokenizer.words_to_texts(sentence.words)
            conversation.add_internal_data(base, 'question', texts)
            conversation.add_internal_data(base, 'topic', topic_pattern)
            conversation.add_internal_data(base, 'that', that_pattern)

            current_variables = ConversationVariables(conversation)

            match_context = self._aiml_parser.match_sentence(client_context,
                                                             sentence,
                                                             topic_pattern=topic_pattern,
                                                             that_pattern=that_pattern)

            if match_context is not None:
                if len(match_context.matched_nodes) == 3 and match_context.matched_nodes[0].matched_node.is_wildcard() is True:
                    if self._aiml_parser.pattern_parser.use_nlu is False:
                        YLogger.debug(client_context, "Matched Catgeory (*): file[%s] line[%s-%s]",
                                      match_context._template_node._filename, match_context._template_node._start_line, match_context._template_node._end_line)
                        conversation.add_internal_matched(base, match_context._template_node)
                        answer = self.resolve_matched_template(client_context, match_context)
                else:
                    YLogger.debug(client_context, "Matched Catgeory : file[%s] line[%s-%s]",
                                  match_context._template_node._filename, match_context._template_node._start_line, match_context._template_node._end_line)
                    try:
                        conversation.add_internal_matched(base, match_context._template_node)
                        answer = self.resolve_matched_template(client_context, match_context)
                    except Exception:
                        self.set_match_context_info(conversation, match_context)
                        before, after = current_variables.different_variables(conversation)
                        conversation.add_internal_data(base, 'before_variables', before)
                        conversation.add_internal_data(base, 'after_variables', after)
                        raise

            if answer is None and self._aiml_parser.pattern_parser.use_nlu is True:
                assert (self._nlu is not None)
                try:
                    utterance = client_context.brain.tokenizer.words_to_texts(sentence.words)
                    if default_srai is False or self.bot.configuration.default_response_srai != utterance:
                        nluResult = conversation.current_question().property("__SYSTEM_NLUDATA__")
                        if nluResult is None or nluResult == "" or self._nlu_utterance != utterance:
                            self._nlu_utterance = utterance

                            match_context = self.multi_nlu_match(client_context, conversation, topic_pattern, that_pattern)
                        else:
                            client_context.match_nlu = True
                            sentence = Sentence(client_context.brain.tokenizer, self.NLU_UTTERANCE)
                            match_context = self._aiml_parser.match_sentence(client_context,
                                                                             sentence,
                                                                             topic_pattern=topic_pattern,
                                                                             that_pattern=that_pattern)
                            client_context.match_nlu = False
                        if match_context is not None:
                            YLogger.debug(client_context, "Matched Catgeory (NLU): file[%s] line[%s-%s]",
                                          match_context._template_node._filename, match_context._template_node._start_line, match_context._template_node._end_line)
                            conversation.add_internal_matched(base, match_context._template_node)
                            answer = self.resolve_matched_template(client_context, match_context)
                except NotImplementedError:
                    if match_context is not None:
                        YLogger.debug(client_context, "Matched Catgeory (*): file[%s] line[%s-%s]",
                                      match_context._template_node._filename, match_context._template_node._start_line, match_context._template_node._end_line)
                        conversation.add_internal_matched(base, match_context._template_node)
                        answer = self.resolve_matched_template(client_context, match_context)
                except Exception:
                    self.set_match_context_info(conversation, match_context)
                    before, after = current_variables.different_variables(conversation)
                    conversation.add_internal_data(base, 'before_variables', before)
                    conversation.add_internal_data(base, 'after_variables', after)
                    raise

            self.set_match_context_info(conversation, match_context)

            before, after = current_variables.different_variables(conversation)
            conversation.add_internal_data(base, 'before_variables', before)
            conversation.add_internal_data(base, 'after_variables', after)
            conversation.add_internal_data(base, 'processing_result', answer)

            if original_base is not None:
                conversation.internal_base = original_base
                base = conversation.internal_base
            conversation.add_internal_data(base, 'response', answer)

        try:
            client_context.userInfo.userInfoPostProcessor(client_context)
        except Exception:
            pass

        return answer

    def set_match_context_info(self, conversation, match_context):
        if match_context is not None:
            json_matchedNode = {'file_name': match_context._template_node._filename,
                                'start_line': match_context._template_node._start_line,
                                'end_line': match_context._template_node._end_line
                                }
            question = conversation.current_question()
            if question is not None:
                question.sentences[question._current_sentence_no].matched_node = json_matchedNode

    def multi_nlu_match(self, client_context, conversation, topic_pattern, that_pattern):
        nlu_list = self._nlu_collection.match_nlus
        timeout = self._nlu_collection.timeout
        match_context = None

        conversation.current_question().set_property("__MATCH_NLU_LATENCY__", '')
        latency_list = []
        nluResult = None
        for server_name in nlu_list:
            try:
                server = self._nlu_collection.server_info(server_name)
                nluResult = self._nlu.nluCall(client_context, server.url, server.apikey, self._nlu_utterance, timeout)
            except NotImplementedError:
                raise

            try:
                latency = self._nlu.get_latency()
                if latency is None or latency == '':
                    latency = '0.0'
                latency_list.append({server_name: float(latency)})
                YLogger.debug(client_context, "Matcher NLU-Call [%s] latency[%s]", server_name, latency)
            except NotImplementedError:
                pass

            conversation.current_question().set_property("__SYSTEM_NLUDATA__", nluResult)
            if nluResult is not None:
                client_context.match_nlu = True
                sentence = Sentence(client_context.brain.tokenizer, self.NLU_UTTERANCE)
                match_context = self._aiml_parser.match_sentence(client_context,
                                                                 sentence,
                                                                 topic_pattern=topic_pattern,
                                                                 that_pattern=that_pattern)
                client_context.match_nlu = False

                if match_context is not None:
                    if len(match_context.matched_nodes) != 3 or \
                       match_context.matched_nodes[0].matched_node.is_wildcard() is False:
                        break

        if nluResult is None:
            client_context.match_nlu = True
            sentence = Sentence(client_context.brain.tokenizer, self.NLU_UTTERANCE)
            match_context = self._aiml_parser.match_sentence(client_context,
                                                             sentence,
                                                             topic_pattern=topic_pattern,
                                                             that_pattern=that_pattern)
            client_context.match_nlu = False

        if len(latency_list) > 0 and client_context.nlu_latency is True:
            latency_dict = {"latency": latency_list}
            conversation.current_question().set_property("__MATCH_NLU_LATENCY__", json.dumps(latency_dict, ensure_ascii=False))

        if match_context is None:
            conversation.current_question().set_property("__SYSTEM_NLUDATA__", None)
        try:
            client_context.userInfo.userInfoPostProcessor(client_context)
        except Exception:
            pass

        return match_context
