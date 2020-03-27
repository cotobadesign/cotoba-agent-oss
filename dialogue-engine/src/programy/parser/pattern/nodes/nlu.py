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
from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.exceptions import ParserException
from operator import gt, ge, eq, le, lt
import json


class PatternNluNode(PatternNode):

    def __init__(self, attribs, text, userid='*', element=None):
        PatternNode.__init__(self, userid)
        if 'intent' in attribs:
            self._intent = attribs['intent']
            if self._intent == '':
                raise ParserException("Empty intent attribute", xml_element=element, nodename='nlu')
        else:
            raise ParserException("Missing intent attribute", xml_element=element, nodename='nlu')

        self._maxLikelihood = True
        if 'maxLikelihood' in attribs:
            if attribs['maxLikelihood'].upper() == 'FALSE':
                self._maxLikelihood = False

        self._score = None
        self._scoreOperator = None
        if 'scoreGt' in attribs:
            self._score = float(attribs['scoreGt'])
            self._scoreOperator = gt
            self._maxLikelihood = False
        elif 'scoreGe' in attribs:
            self._score = float(attribs['scoreGe'])
            self._scoreOperator = ge
            self._maxLikelihood = False
        elif 'score' in attribs:
            self._score = float(attribs['score'])
            self._scoreOperator = eq
            self._maxLikelihood = False
        elif 'scoreLe' in attribs:
            self._score = float(attribs['scoreLe'])
            self._scoreOperator = le
            self._maxLikelihood = False
        elif 'scoreLt' in attribs:
            self._score = float(attribs['scoreLt'])
            self._scoreOperator = lt
            self._maxLikelihood = False

    @property
    def intent(self):
        return self._intent

    @property
    def score(self):
        return self._score

    @property
    def scoreOperator(self):
        return self._scoreOperator

    @property
    def maxLikelihood(self):
        return self._maxLikelihood

    def scoreName(self):
        if self._scoreOperator == gt:
            return 'scoreGt'
        elif self._scoreOperator == ge:
            return 'scoreGe'
        elif self._scoreOperator == eq:
            return 'score'
        elif self._scoreOperator == le:
            return 'scoreLe'
        elif self._scoreOperator == lt:
            return 'scoreLt'

        return None

    def is_nlu(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<nlu userid="%s" intent="%s"' % (self.userid, self._intent)
        else:
            string += '<nlu intent="%s"' % self._intent

        if self._scoreOperator:
            string += ' %s="%.2f"' % (self.scoreName(), self._score)
        else:
            if self._maxLikelihood is False:
                string += ' maxLikelihood="false"'

        string += '>\n'
        string += super(PatternNluNode, self).to_xml(client_context)
        string += "</nlu>"
        return string

    def to_string(self, verbose=True):
        text = "NLU "
        if verbose is True:
            text += "[%s] [%s] " % (self.userid, self._child_count(verbose))
        if self._score is not None:
            text += "intent=[%s] score=[%.2f %s]" % (self._intent, self._score, self.scoreName())
        else:
            if self._maxLikelihood is False:
                text += "intent=[%s] score=[None] maxLikelihood=[False]" % self._intent
            else:
                text += "intent=[%s] score=[None]" % self._intent
        return text

    def equivalent(self, other):
        if self.userid != other.userid:
            return False

        if self._intent == other.intent and self._maxLikelihood == other.maxLikelihood and self._score == other.score and self._scoreOperator == other.scoreOperator:
            return True

        return False

    def equals(self, client_context, words, word_no):
        if client_context.match_nlu is False:
            return EqualsMatch(False, word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        conversation = client_context.bot.get_conversation(client_context)
        try:
            quetion = conversation.current_question()
            if quetion is None:
                return EqualsMatch(False, word_no)

            json_dict = quetion.property("__SYSTEM_NLUDATA__")
            if json_dict is None or json_dict == '':
                return EqualsMatch(False, word_no)
            else:
                json_dict = json.loads(json_dict)
        except Exception as e:
            YLogger.exception(self, "PatternNluNode failed to load keys", e)
            return EqualsMatch(False, word_no)

        if self._intent == "*":
            return EqualsMatch(True, word_no, self._intent)

        try:
            intents = json_dict["intents"]
        except Exception as e:
            YLogger.exception(self, "PatternNluNode failed to load JSON", e)
            return EqualsMatch(False, word_no)

        score = None
        try:
            intentList = [intent.get("intent") for intent in intents]
            scoreList = [score.get("score") for score in intents]

            matchIntentIndex = intentList.index(self._intent)
            maxScore = max(scoreList)

            if scoreList[matchIntentIndex] == maxScore:
                score = scoreList[matchIntentIndex]
            elif self._maxLikelihood is not True:
                score = scoreList[matchIntentIndex]

            if score is not None:
                if self._score is None:
                    YLogger.debug(client_context, "PatternNluNode [%s] resolved", self._intent)
                    return EqualsMatch(True, word_no, self._intent)

                if self._scoreOperator(score, self._score):
                    YLogger.debug(client_context, "PatternNluNode [%s] resolved to [%f] %s [%f]", self._intent, score, self.scoreName(), self._score)
                    return EqualsMatch(True, word_no, "__INTENT__"+self._intent)
        except Exception:
            YLogger.debug(client_context, "PatternNluNode failed to get intent[%s]", self._intent)
            return EqualsMatch(False, word_no)

        return EqualsMatch(False, word_no)
