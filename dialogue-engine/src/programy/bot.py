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

from programy.brain import Brain
from programy.dialog.question import Question
from programy.dialog.sentence import Sentence
from programy.dialog.convo_mgr import ConversationManager
from programy.utils.classes.loader import ClassLoader
from programy.spelling.base import SpellingChecker
from programy.dialog.splitter.splitter import SentenceSplitter
from programy.dialog.joiner.joiner import SentenceJoiner
from programy.translate.base import BaseTranslator
from programy.sentiment.base import BaseSentimentAnalyser
from programy.triggers.system import SystemTriggers
from programy.parser.exceptions import LimitOverException


class BrainSelector(object):

    def __init__(self, configuration):
        self._configuration = configuration

    def select_brain(self, brains):
        pass


class DefaultBrainSelector(BrainSelector):

    def __init__(self, configuration):
        BrainSelector.__init__(self, configuration)

    def select_brain(self, brains):
        if brains:
            return next(iter(brains.values()))
        return None


class BrainFactory(object):

    def __init__(self, bot):
        self._brains = {}
        self.loads_brains(bot)
        self._brain_selector = None
        self.load_brain_selector(bot.configuration)

    def brainids(self):
        return self._brains.keys()

    def brain(self, id):
        if id in self._brains:
            return self._brains[id]
        else:
            return None

    def loads_brains(self, bot):
        for config in bot.configuration.configurations:
            brain = Brain(bot, config)
            self._brains[brain.id] = brain

    def load_brain_selector(self, configuration):
        if configuration.brain_selector is None:
            self._brain_selector = DefaultBrainSelector(configuration)
        else:
            try:
                self._brain_selector = ClassLoader.instantiate_class(configuration.brain_selector)(configuration)
            except Exception:
                self._brain_selector = DefaultBrainSelector(configuration)

    def select_brain(self):
        return self._brain_selector.select_brain(self._brains)


class Bot(object):

    def __init__(self, config, client):

        assert (config is not None)
        assert (client is not None)

        self._configuration = config
        self._client = client

        self._brain_factory = BrainFactory(self)

        self._question_depth = 0
        self._question_start_time = None

        self._spell_checker = None
        self.initiate_spellchecker()

        self._sentence_splitter = None
        self.initiate_sentence_splitter()

        self._sentence_joiner = None
        self.initiate_sentence_joiner()

        self._from_translator = None
        self._to_translator = None
        self.initiate_translator()

        self._sentiment_analyser = None
        self._sentiment_scores = None
        self.initiate_sentiment_analyser()

        self._conversation_mgr = ConversationManager(config.conversations)
        self._conversation_mgr.initialise(self._client.storage_factory)

        self._utterance = None

        self._is_error = False
        self._srai_count = 0

    def ylogger_type(self):
        return "bot"

    @property
    def id(self):
        return self._configuration.section_name

    @property
    def client(self):
        return self._client

    @property
    def configuration(self):
        return self._configuration

    @property
    def brain_factory(self):
        return self._brain_factory

    @property
    def spell_checker(self):
        return self._spell_checker

    def initiate_spellchecker(self):
        if self.configuration.spelling is not None:
            self._spell_checker = SpellingChecker.initiate_spellchecker(self.configuration.spelling, self.client.storage_factory)

    @property
    def sentence_splitter(self):
        return self._sentence_splitter

    def initiate_sentence_splitter(self):
        if self.configuration.splitter is not None:
            self._sentence_splitter = SentenceSplitter.initiate_sentence_splitter(self.configuration.splitter)
            if self._sentence_splitter is not None:
                if self.brain.properties.has_property("splitter_split_chars") is True:
                    self._sentence_splitter.set_configuration_split_chars(self.brain.properties.property("splitter_split_chars"))
                if self.brain.properties.has_property("punctuation_chars") is True:
                    self._sentence_splitter.set_configuration_punctuation_chars(self.brain.properties.property("punctuation_chars"))

    @property
    def sentence_joiner(self):
        return self._sentence_joiner

    def initiate_sentence_joiner(self):
        if self.configuration.joiner is not None:
            self._sentence_joiner = SentenceJoiner.initiate_sentence_joiner(self.configuration.joiner)
            if self._sentence_joiner is not None:
                if self.brain.properties.has_property("joiner_join_chars") is True:
                    self._sentence_joiner.set_configuration_join_chars(self.brain.properties.property("joiner_join_chars"))
                if self.brain.properties.has_property("joiner_terminator") is True:
                    self._sentence_joiner.set_configuration_terminator(self.brain.properties.property("joiner_terminator"))

    @property
    def from_translator(self):
        return self._from_translator

    @property
    def to_translator(self):
        return self._to_translator

    def initiate_translator(self):
        if self.configuration.from_translator is not None:
            self._from_translator = BaseTranslator.initiate_translator(self.configuration.from_translator)

        if self.configuration.to_translator is not None:
            self._to_translator = BaseTranslator.initiate_translator(self.configuration.to_translator)

    @property
    def sentiment_analyser(self):
        return self._sentiment_analyser

    @property
    def sentiment_scores(self):
        return self._sentiment_scores

    def initiate_sentiment_analyser(self):
        if self.configuration.sentiment_analyser is not None:
            self._sentiment_analyser, self._sentiment_scores = BaseSentimentAnalyser.initiate_sentiment_analyser(self.configuration.sentiment_analyser)

    @property
    def brain(self):
        return self._brain_factory.select_brain()

    @property
    def conversations(self):
        return self._conversation_mgr

    @property
    def default_response(self):
        return self.configuration.default_response

    @property
    def default_response_srai(self):
        return self.configuration.default_response_srai

    @property
    def exit_response(self):
        return self.configuration.exit_response

    @property
    def exit_response_srai(self):
        return self.configuration.exit_response_srai

    @property
    def exception_response(self):
        return self.configuration.exception_response

    @property
    def initial_question(self):
        return self.configuration.initial_question

    @property
    def initial_question_srai(self):
        return self.configuration.initial_question_srai

    @property
    def override_properties(self):
        return self.configuration.override_properties

    @property
    def utterance(self):
        return self._utterance

    def get_version_string(self, client_context):

        assert (client_context is not None)

        if client_context.brain.properties.has_property("version"):
            # The old version of returning the version string, did not distinquish
            # between App and Grammar version
            return "%s, v%s, initiated %s " % (
                client_context.brain.properties.property("name"),
                client_context.brain.properties.property("version"),
                client_context.brain.properties.property("birthdate"))
        else:
            # This version now does
            return "%s, App: v%s Grammar v%s, initiated %s " % (
                client_context.brain.properties.property("name"),
                client_context.brain.properties.property("app_version"),
                client_context.brain.properties.property("grammar_version"),
                client_context.brain.properties.property("birthdate"))

    def has_conversation(self, client_context):

        assert (self._conversation_mgr is not None)

        return self._conversation_mgr.has_conversation(client_context)

    def conversation(self, client_context):
        return self.get_conversation(client_context)

    def get_conversation(self, client_context):

        assert (self._conversation_mgr is not None)

        return self._conversation_mgr.get_conversation(client_context)

    def save_conversation(self, client_context):

        assert (self._conversation_mgr is not None)

        self._conversation_mgr.save_conversation(client_context)

    def check_spelling_before(self, client_context, each_sentence):
        if self.spell_checker is not None:
            self.spell_checker.check_spelling_before(client_context, each_sentence)

    def check_spelling_and_retry(self, client_context, each_sentence):
        if self.spell_checker is not None:
            return self.spell_checker.check_spelling_and_retry(client_context, each_sentence)
        return None

    def get_default_response(self, client_context):

        assert (client_context is not None)

        if self.default_response_srai is not None and self.default_response_srai != '':
            sentence = Sentence(client_context.brain.tokenizer, self.default_response_srai)
            default_response = client_context.brain.ask_question(client_context, sentence, default_srai=True)
            if default_response is None:
                default_response = client_context.brain.properties.property("default-response")
                if default_response is None:
                    default_response = self.default_response
            return default_response
        else:
            default_response = client_context.brain.properties.property("default-response")
            if default_response is None:
                default_response = self.default_response
            return default_response

    def get_exception_response(self, client_context):

        assert (client_context is not None)

        exception_response = client_context.brain.properties.property("exception-response")
        if exception_response is None:
            exception_response = self.exception_response
        return exception_response

    def get_initial_question(self, client_context):

        assert (client_context is not None)

        if self.initial_question_srai is not None:
            conversation = client_context.bot.get_conversation(client_context)
            question = self.get_question(client_context, self.initial_question_srai, True)
            conversation.record_dialog(question)
            sentence = Sentence(client_context.brain.tokenizer, self.initial_question_srai)
            try:
                initial_question = client_context.brain.ask_question(client_context, sentence)
            except Exception:
                initial_question = None
            conversation.pop_dialog()
            if initial_question is None or not initial_question:
                initial_question = self.initial_question
            return initial_question
        else:
            return self.initial_question

    def get_exit_response(self, client_context):

        assert (client_context is not None)

        if self.exit_response_srai is not None:
            sentence = Sentence(client_context.brain.tokenizer, self.exit_response_srai)
            exit_response = client_context.brain.ask_question(client_context, sentence)
            if exit_response is None or not exit_response:
                exit_response = self.exit_response

            return exit_response

        else:
            return self.exit_response

    def pre_process_text(self, client_context, text, srai):

        assert (client_context is not None)
        assert (client_context.brain is not None)

        if srai is False:
            pre_processed = client_context.brain.pre_process_question(client_context, text)
            YLogger.debug(client_context, "Pre Processed (%s): %s", client_context.userid, pre_processed)

        else:
            pre_processed = text

        if pre_processed is None or pre_processed == "":

            assert (self.configuration is not None)

            pre_processed = self.configuration.empty_string

        return pre_processed

    def get_question(self, client_context, pre_processed, srai):
        if srai is False:
            return Question.create_from_text(client_context, pre_processed, srai=srai)
        else:
            return Question.create_from_text(client_context, pre_processed, split=False, srai=srai)

    def combine_answers(self, answers, srai):

        assert (answers is not None)
        assert (self._sentence_joiner is not None)

        return self._sentence_joiner.combine_answers(answers, srai)

    def post_process_response(self, client_context, response, srai):
        if srai is False:

            assert (client_context is not None)

            answer = client_context.brain.post_process_response(client_context, response).strip()
            if not answer:
                answer = self.get_default_response(client_context)

        else:
            answer = response

        return answer

    def log_answer(self, client_context, text, answer, responselogger, srai):
        YLogger.debug(client_context, "Processed Response (%s) [srai:%s] : %s", client_context.userid, srai, answer)

        if responselogger is not None:
            responselogger.log_response(text, answer)

    def ask_question(self, client_context, text, srai=False, responselogger=None):

        assert (client_context is not None)

        if srai is False:
            client_context.bot = self
            client_context.brain = client_context.bot.brain
            self._is_error = False
        else:
            if self._is_error is True:
                return ''

        assert (client_context.bot is not None)
        assert (client_context.brain is not None)

        client_context.mark_question_start(text, srai)

        pre_processed = self.pre_process_text(client_context, text, srai)

        question = self.get_question(client_context, pre_processed, srai)

        conversation = self.get_conversation(client_context)
        if len(conversation.questions) == 0:
            if self.client.trigger_manager is not None:
                self.client.trigger_manager.trigger(SystemTriggers.CONVERSATION_START, client_context)

        assert (conversation is not None)

        if srai is False:
            conversation.exception = None
            if client_context.server_mode is True:
                self.conversations.load_learnf_with_userid(client_context)
                client_context.brain.rdf.apply_updates()
            if client_context.deleteVariable is True:
                conversation.clear_data_property()
            self.conversations.remove_internal_data(client_context)

        conversation.record_dialog(question)

        try:
            answers = self.process_sentences(client_context, question, srai, responselogger)
        except LimitOverException as excep:
            if self._is_error is False:
                self._is_error = True
                conversation.exception = str(excep)
                YLogger.exception(client_context, "Limit-Over Exception", excep)
                base = conversation.internal_base
                conversation.add_internal_data(base, 'exception', conversation.exception)
            if srai is True:
                conversation.pop_dialog()
                raise
        except Exception as excep:
            if self._is_error is False:
                self._is_error = True
                conversation.exception = str(excep)
                YLogger.exception(client_context, "Exception", excep)
                base = conversation.internal_base
                conversation.add_internal_data(base, 'exception', conversation.exception)
            if srai is True:
                conversation.pop_dialog()
                raise

        if self._is_error is True:
            question.exception = conversation.exception
            answer = self.get_exception_response(client_context)
            sentence = question.current_sentence()
            sentence.response = answer
            answers = [answer]

        client_context.reset_question()

        if srai is True:
            conversation.pop_dialog()

        conversation.save_sentiment()

        if srai is False:
            self.conversations.set_internal_data(client_context)
            self.save_conversation(client_context)
            if client_context.server_mode is True:
                self.conversations.remove_conversation(client_context)
                self.conversations.remove_learnf_with_userid(client_context)

        if self.client.trigger_manager is not None and srai is False:
            self.client.trigger_manager.trigger(SystemTriggers.QUESTION_ASKED, client_context)

        return self.combine_answers(answers, srai)

    def process_sentences(self, client_context, question, srai, responselogger):
        self._utterances = None
        utterances = []
        answers = []
        sentence_no = 0
        for sentence in question.sentences:
            YLogger.debug(client_context, "Sentence-Words %s", sentence.words)
            question.set_current_sentence_no(sentence_no)
            utterance = client_context.brain.tokenizer.words_to_texts(sentence.words)
            if utterance == '':
                answer = ''
            else:
                answer = self.process_sentence(client_context, sentence, srai, responselogger)
            utterances.append(utterance)
            answers.append(answer)
            if self._is_error is True:
                break
            sentence_no += 1

        self._utterance = self.combine_answers(utterances, False)
        return answers

    def process_sentence(self, client_context, sentence, srai, responselogger):

        assert (client_context is not None)
        assert (client_context.brain is not None)

        try:
            client_context.check_max_recursion()
            client_context.check_max_timeout()
        except LimitOverException:
            raise

        if srai is False:
            self.check_spelling_before(client_context, sentence)
            self._srai_count = 0
        else:
            self._srai_count += 1
            if self._srai_count > client_context.bot.configuration.max_search_srai:
                raise LimitOverException("Max search srai [%d] exceeded: [%s]" %
                                         (client_context.bot.configuration.max_search_srai, client_context.brain.tokenizer.words_to_texts(sentence.words)))

        response = client_context.brain.ask_question(client_context, sentence, srai)

        if response is None and srai is False:
            response = self.check_spelling_and_retry(client_context, sentence)

        if response is not None:
            return self.handle_response(client_context, sentence, response, srai, responselogger)
        else:
            return self.handle_none_response(client_context, sentence, responselogger)

    def handle_response(self, client_context, sentence, response, srai, responselogger):

        assert (sentence is not None)

        YLogger.debug(client_context, "Raw Response (%s): %s", client_context.userid, response)
        sentence.response = response

        sentence.calculate_sentinment_score(client_context)

        answer = self.post_process_response(client_context, response, srai)
        self.log_answer(client_context, sentence.text(), answer, responselogger, srai)

        return answer

    def handle_none_response(self, client_context, sentence, responselogger):

        assert (sentence is not None)

        sentence.response = self.get_default_response(client_context)

        sentence.calculate_sentinment_score(client_context)

        if responselogger is not None:
            responselogger.log_unknown_response(sentence)

        return sentence.response
