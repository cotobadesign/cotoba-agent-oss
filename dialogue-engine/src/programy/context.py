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
import datetime
import uuid

from programy.utils.logging.ylogger import YLogger
from programy.parser.exceptions import LimitOverException


class ClientContext(object):

    def __init__(self, client, userid):
        self._client = client
        self._userid = userid
        self._bot = None
        self._brain = None
        self._question_start_time = None
        self._question_depth = 0
        self._id = uuid.uuid1()
        self._deleteVariable = False
        self._server_mode = False
        self._log_level = None
        self._match_nlu = False
        self._match_type = None
        self._nlu_latency = True

    def ylogger_type(self):
        return "context"

    @property
    def id(self):
        return self._id

    @property
    def client(self):
        return self._client

    @property
    def userid(self):
        return self._userid

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, id):
        self._bot = id

    @property
    def brain(self):
        return self._brain

    @property
    def question_start_time(self):
        return self._question_start_time

    @brain.setter
    def brain(self, id):
        self._brain = id

    @property
    def deleteVariable(self):
        return self._deleteVariable

    @deleteVariable.setter
    def deleteVariable(self, deleteVariable):
        self._deleteVariable = deleteVariable

    @property
    def server_mode(self):
        return self._server_mode

    @server_mode.setter
    def server_mode(self, server_mode):
        self._server_mode = server_mode

    @property
    def log_level(self):
        return self._log_level

    @log_level.setter
    def log_level(self, log_level):
        self._log_level = log_level

    @property
    def match_nlu(self):
        return self._match_nlu

    @match_nlu.setter
    def match_nlu(self, match_nlu):
        self._match_nlu = match_nlu

    @property
    def match_type(self):
        return self._match_type

    @match_type.setter
    def match_type(self, match_type):
        self._match_type = match_type

    @property
    def nlu_latency(self):
        return self._nlu_latency

    @nlu_latency.setter
    def nlu_latency(self, nlu_latency):
        self._nlu_latency = nlu_latency

    def get_loglevel(self):
        return self._log_level

    def check_max_recursion(self):
        if self.bot.configuration.max_question_recursion != -1:
            if self._question_depth > self.bot.configuration.max_question_recursion:
                raise LimitOverException("Maximum recursion limit [%d] exceeded" % self.bot.configuration.max_question_recursion)

    def total_search_time(self):
        delta = datetime.datetime.now() - self._question_start_time
        return abs(delta.total_seconds())

    def check_max_timeout(self):
        if self.bot.configuration.max_question_timeout != -1:
            if self.total_search_time() >= self.bot.configuration.max_question_timeout:
                raise LimitOverException("Maximum question time limit [%d]secs exceeded" % self.bot.configuration.max_question_timeout)

    def mark_question_start(self, question, srai=False):
        if srai is False:
            if self._question_depth == 0:
                self._question_start_time = datetime.datetime.now()
            YLogger.debug(self, "############################################################################(srai:False)##")
        else:
            YLogger.debug(self, "----------------------------------------------------------------------------(srai:True)---")
        YLogger.debug(self, "Question (%s): %s", self._client.id, question)

        self._question_depth += 1

    def reset_question(self):
        self._question_depth = 0

    def __str__(self):
        return "[%s] [%s] [%s] [%s] [%d]" % (
            self._client.id,
            self._userid,
            self._bot.id if self._bot else "",
            self._brain.id if self._brain else "",
            self._question_depth
        )

    def to_json(self):
        return {
            "clientid": self._client.id,
            "userid": self._userid,
            "botid": self._bot.id if self._bot else None,
            "brainid": self._brain.id if self._brain else None,
            "depth": self._question_depth
        }

    def dump(self, output_func=print, verbose=False):
        """
        Helper Function for output tree structure
        :param output_func: Function used to display output, typically print or logging function
        :param verbose: Level of detail to display
        :return: None
        """
        self.brain.aiml_parser.pattern_parser.dump(output_func=output_func, verbose=False)
