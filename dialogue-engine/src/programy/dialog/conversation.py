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
import re

from programy.dialog.question import Question
from programy.parser.exceptions import LimitOverException


class Conversation(object):

    def __init__(self, client_context):
        self._client_context = client_context
        self._questions = []
        self._max_histories = client_context.bot.configuration.conversations.max_histories
        self._properties = {'topic': client_context.bot.configuration.conversations.initial_topic}
        self._data_properties = {}
        self._num_categories = 0
        self._user_categories = 0
        self._logs = []
        self._exception = None
        self._max_properties = client_context.bot.configuration.max_properties
        self._internal_data = []
        self._internal_base = None

    @property
    def questions(self):
        return self._questions

    @property
    def max_histories(self):
        return self._max_histories

    @property
    def properties(self):
        return self._properties

    @property
    def data_properties(self):
        return self._data_properties

    @property
    def num_categories(self):
        return self._num_categories

    @num_categories.setter
    def num_categories(self, categories):
        self._num_categories = categories

    @property
    def user_categories(self):
        return self._user_categories

    @user_categories.setter
    def user_categories(self, categories):
        self._user_categories = categories

    @property
    def logs(self):
        return self._logs

    @property
    def exception(self):
        return self._exception

    @exception.setter
    def exception(self, exception: str):
        self._exception = exception

    @property
    def internal_data(self):
        return self._internal_data

    @property
    def internal_base(self):
        return self._internal_base

    @internal_base.setter
    def internal_base(self, base):
        self._internal_base = base

    def has_current_question(self):
        return bool(self._questions)

    def current_question(self):
        if len(self._questions) > 0:
            return self._questions[-1]
        return None

    def previous_nth_question(self, num: int):
        if len(self._questions) < (num + 1):
            raise Exception("Num question array violation !")
        previous = -1 - num
        return self._questions[previous]

    def set_property(self, name: str, value: str):
        if name == 'topic':
            if value == '':
                value = '*'
        if value == '':
            try:
                del self._properties[name]
            except Exception:
                pass
        else:
            if name not in self._properties:
                self._check_properties_count()
            self._properties[name] = value
        return value

    def set_data_property(self, data: str, value: str):
        if value == '':
            try:
                del self._data_properties[data]
            except Exception:
                pass
        else:
            if data not in self._data_properties:
                self._check_properties_count()
            self._data_properties[data] = value

    def _check_properties_count(self):
        used_count = len(self._properties) + len(self._data_properties)

        except_properties = ['positivity', 'subjectivity']
        for key in self._properties.keys():
            if key in except_properties:
                used_count -= 1

        if used_count >= self._max_properties:
            raise LimitOverException("Max properties count [%d] exceeded" % self._max_properties)

    def clear_data_property(self):
        self._data_properties.clear()

    def property(self, name: str):
        if self._properties is not None:
            if name in self._properties:
                return self._properties[name]
        return None

    def data_property(self, data: str):
        if self._properties is not None:
            if data in self._data_properties:
                return self._data_properties[data]
        return None

    def record_dialog(self, question: Question):
        if len(self._questions) == self._max_histories:
            YLogger.debug(self, "Conversation history at max [%d], removing oldest", self._max_histories)
            self._questions.remove(self._questions[0])
        self._questions.append(question)

    def pop_dialog(self):
        if self._questions:
            self._questions.pop()

    def load_initial_variables(self, variables_collection):
        for pair in variables_collection.pairs:
            YLogger.debug(self, "Setting variable [%s] = [%s]", pair[0], pair[1])
            self._properties[pair[0]] = pair[1]

    def get_topic_pattern(self, client_context):
        topic_pattern = self.property("topic")

        if topic_pattern is None:
            YLogger.debug(client_context, "No Topic pattern default to [*]")
            topic_pattern = "*"
        else:
            YLogger.debug(client_context, "Topic pattern = [%s]", topic_pattern)

        return topic_pattern

    def parse_last_sentences_from_response(self, client_context, response):

        # If the response contains punctuation such as "Hello. There" then THAT is none
        response = re.sub(r'<\s*br\s*/>\s*', ".", response)
        response = re.sub(r'<br></br>*', ".", response)
        sentences = response.split(".")
        sentences = [x for x in sentences if x]
        last_sentence = sentences[-1]

        that_pattern = client_context.bot.sentence_splitter.remove_punctuation(last_sentence)
        that_pattern = that_pattern.strip()

        if that_pattern == "":
            that_pattern = '*'

        return that_pattern

    def get_that_pattern(self, client_context, srai=False):
        try:
            that_question = None
            if srai is False:
                that_question = self.previous_nth_question(1)
            else:
                if len(self._questions) > 2:
                    for question in reversed(self._questions[:-2]):
                        if question._srai is False and question.has_response():
                            that_question = question
                            break

            if that_question is not None:
                that_sentence = that_question.current_sentence()
            else:
                that_sentence = None

            # If the last response was valid, i.e not none and not empty string, then use
            # that as the that_pattern, otherwise we default to '*' as pattern
            if that_sentence.response is not None and that_sentence.response != '':
                that_pattern = self.parse_last_sentences_from_response(client_context, that_sentence.response)
                YLogger.debug(client_context, "That pattern = [%s]", that_pattern)
            else:
                YLogger.debug(client_context, "That pattern, no response, default to [*]")
                that_pattern = "*"

        except Exception:
            YLogger.debug(client_context, "No That pattern default to [*]")
            that_pattern = "*"

        return that_pattern

    def to_json(self):
        json_data = {
            'client_context': self._client_context.to_json(),
            'questions': [],
            'max_histories': self._max_histories,
            'properties': self._properties,
            'data_properties': self._data_properties,
            'exception': self._exception,
            'categories': self._num_categories,
            'user_categories': self._user_categories
        }

        for question in self.questions:
            json_question = {'sentences': [],
                             'srai': question._srai,
                             'var_properties': question._properties,
                             'name_properties': question._name_properties,
                             'data_properties': question._data_properties,
                             'exception': question._exception
                             }
            json_data['questions'].append(json_question)

            for sentence in question.sentences:
                json_sentence = {"question": sentence.text(),
                                 "response": sentence.response,
                                 "positivity": sentence.positivity,
                                 "subjectivity": sentence.subjectivity,
                                 'matched_node': sentence.matched_node
                                 }
                json_question['sentences'].append(json_sentence)

        return json_data

    def from_json(self, client_context, json_data):
        if json_data is not None:
            json_questions = json_data['questions']
            self._properties = json_data['properties']
            self._data_properties = json_data['data_properties']
            self._exception = json_data['exception']
            self._num_categories = json_data['categories']
            self._user_categories = json_data['user_categories']
            for json_question in json_questions:
                json_sentences = json_question['sentences']
                for json_sentence in json_sentences:
                    question = Question.create_from_text(self._client_context, json_sentence['question'])
                    question.sentence(0).response = json_sentence['response']
                    question.sentence(0).matched_node = json_sentence['matched_node']
                    question._properties = json_question['var_properties']
                    question._name_properties = json_question['name_properties']
                    question._data_properties = json_question['data_properties']
                    question._exception = json_question['exception']
                    self._questions.append(question)
            self.recalculate_sentiment_score(client_context)

    def append_log(self, log):
        self._logs.append(log)

    def recalculate_sentiment_score(self, client_context):
        for question in self._questions:
            question.recalculate_sentinment_score(client_context)

    def calculate_sentiment_score(self):

        positivity = 0.00
        subjectivity = 0.00

        count = 0
        for question in self._questions:
            q_positivity, q_subjectivity = question.calculate_sentinment_score()

            positivity += q_positivity
            subjectivity += q_subjectivity

            count += 1

        if count > 0:
            positivity /= count
            subjectivity /= count
        else:
            subjectivity = 0.5

        return positivity, subjectivity

    def save_sentiment(self):
        positivity, subjectivity = self.calculate_sentiment_score()
        self._properties['positivity'] = str(positivity)
        self._properties['subjectivity'] = str(subjectivity)

    def clear_internal_data(self):
        self._internal_data.clear()
        self._internal_base = None

    def add_internal_data(self, base, tag, data):
        if base is not None: 
            base[tag] = data

    def add_internal_variables(self, base, tag):
        if base is None: 
            return

        name_dict = {}
        for key, val in self.properties.items():
            name_dict[key] = val

        data_dict = {}
        for key, val in self.data_properties.items():
            data_dict[key] = val

        var_dict = {}
        question = self.current_question()
        if question is not None:
            for key, val in question._properties.items():
                var_dict[key] = val

        variables_dict = {}
        variables_dict["name_properties"] = name_dict
        variables_dict["data_properties"] = data_dict
        variables_dict["var_properties"] = var_dict

        base[tag] = variables_dict

    def add_internal_matched(self, base, match_template):
        if base is None: 
            return

        match_dict = {}
        match_dict['file_name'] = match_template._filename
        match_dict['start_line'] = match_template._start_line
        match_dict['end_line'] = match_template._end_line

        base['matched_node'] = match_dict
