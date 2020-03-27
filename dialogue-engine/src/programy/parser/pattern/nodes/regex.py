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

from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.exceptions import ParserException


class PatternRegexNode(PatternNode):

    def __init__(self, attribs, text, userid='*', element=None):
        # @TODO This does not handle upper and lower case
        PatternNode.__init__(self, userid)
        self._pattern_text = None
        self._pattern_template = None
        self._pattern = None
        self._is_form = False
        self._is_NotOption = False
        if 'pattern' in attribs:
            self._pattern_text = attribs['pattern']
        elif 'template' in attribs:
            self._pattern_template = attribs['template']
            if self._pattern_template == '':
                raise ParserException("Specified Parameter is empty", xml_element=element, nodename='regex')
        elif 'form' in attribs:
            form_text = attribs['form']
            if form_text.count('(?!') > 0:
                self._is_NotOption = True
            self._is_form = True
            self._pattern_text = form_text
        elif text:
            self._pattern_text = text
        else:
            raise ParserException("No Parameter specified as attribute or text", xml_element=element, nodename='regex')

        if self._pattern_text is not None:
            if self._pattern_text == '':
                raise ParserException("Specified Parameter is empty", xml_element=element, nodename='regex')
            try:
                self._pattern = re.compile(self._pattern_text, re.IGNORECASE)
            except Exception:
                raise ParserException("invalid regex expression (unable re.compile)", xml_element=element, nodename='regex')

    @property
    def pattern(self):
        return self._pattern

    @property
    def pattern_text(self):
        return self._pattern_text

    @property
    def pattern_template(self):
        return self._pattern_template

    def is_regex(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if self._pattern_template is not None:
            if include_user is True:
                string += '<regex userid="%s" template="%s">' % (self.userid, self._pattern_template)
            else:
                string += '<regex template="%s">' % self._pattern_template
        elif self._is_form is True:
            if include_user is True:
                string += '<regex userid="%s" form="%s">' % (self.userid, self._pattern_text)
            else:
                string += '<regex form="%s">' % self._pattern_text
        else:
            if include_user is True:
                string += '<regex userid="%s" pattern="%s">' % (self.userid, self._pattern_text)
            else:
                string += '<regex pattern="%s">' % self._pattern_text
        string += super(PatternRegexNode, self).to_xml(client_context)
        string += "</regex>\n"
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            if self._pattern_template is not None:
                return "REGEX [%s] [%s] template=[%s]" % (self.userid, self._child_count(verbose), self._pattern_template)
            elif self._is_form is True:
                return "REGEX [%s] [%s] form=[%s]" % (self.userid, self._child_count(verbose), self._pattern_text)
            return "REGEX [%s] [%s] pattern=[%s]" % (self.userid, self._child_count(verbose), self._pattern_text)

        if self._pattern_template is not None:
            return "REGEX template=[%s]" % self._pattern_template
        elif self._is_form is True:
            return "REGEX form=[%s]" % self._pattern_text
        return "REGEX pattern=[%s]" % self._pattern_text

    def equivalent(self, other):
        if other.is_regex():
            if self.userid == other.userid:
                if self._pattern_template is not None:
                    if other.pattern_template is not None:
                        return bool(self._pattern_template == other.pattern_template)
                else:
                    if other.pattern is not None:
                        return bool(self.pattern == other.pattern)
        return False

    def equals(self, client_context, words, word_no):
        if client_context.match_nlu is True:
            return EqualsMatch(False, word_no)

        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        if self._pattern_template is not None:
            template = client_context.brain.regex_templates.regex(self._pattern_template)
            if template is not None:
                result = template.match(word)
                if result is not None:
                    YLogger.debug(client_context, "Match word [%s] regex", word)
                    return EqualsMatch(True, word_no, word)
                else:
                    YLogger.debug(client_context, "No word [%s] matched regex", word)
                    return EqualsMatch(False, word_no)
            else:
                return EqualsMatch(False, word_no)
        else:
            if self._is_form is False:
                result = self.pattern.match(word)
                if result is not None:
                    YLogger.debug(client_context, "Match word [%s] regex", word)
                    return EqualsMatch(True, word_no, word)
                else:
                    YLogger.debug(client_context, "No word [%s] matched regex", word)
                    return EqualsMatch(False, word_no)
            else:
                check_words = []
                check_index = 0
                for word in words.words:
                    if word_no > check_index:
                        check_index += 1
                        continue
                    if word == '__TOPIC__':
                        break
                    check_words.append(word)
                if len(check_words) > 0:
                    words_text = client_context.brain.tokenizer.words_to_texts(check_words)
                    result = self.pattern.match(words_text)
                    if result is not None:
                        if self._is_NotOption is False:
                            matchlen = result.end()
                        else:
                            matchlen = result.endpos
                        checklen = 0
                        matchwords = []
                        check_no = word_no
                        for word in check_words:
                            checklen += len(word)
                            if checklen >= matchlen:
                                overlen = checklen - matchlen
                                if overlen == 0:
                                    matchwords.append(word)
                                else:
                                    words.divide_word(check_no, (len(word) - overlen))
                                    matchwords.append(words.words[check_no])
                                break
                            matchwords.append(word)
                            check_no += 1
                            if words_text[checklen] == ' ':
                                checklen += 1
                        words_text = client_context.brain.tokenizer.words_to_texts(matchwords)
                        YLogger.debug(client_context, "Match words [%s] regex", words_text)
                        return EqualsMatch(True, check_no, words_text)

                YLogger.debug(client_context, "No words [%s] matched regex", word)
                return EqualsMatch(False, word_no)
