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

from programy.parser.pattern.nodes.base import PatternNode
from programy.parser.pattern.matcher import EqualsMatch
from programy.parser.exceptions import ParserException
from programy.utils.language.japanese import JapaneseLanguage


class PatternISetNode(PatternNode):

    iset_count = 1

    def __init__(self, attribs, text, userid='*', element=None):
        PatternNode.__init__(self, userid)
        self._words = {}
        self._values = {}

        if 'words' in attribs:
            words = attribs['words']
        elif text:
            words = text
        else:
            raise ParserException("No words specified as attribute or text", xml_element=element, nodename='iset')

        check_words = JapaneseLanguage.zenhan_normalize(words)
        self._is_CJK = JapaneseLanguage.is_CJKword(check_words)
        if self._parse_words(words) is False:
            raise ParserException("empty element in words", xml_element=element, nodename='iset')

        self._iset_name = "iset_%d" % (PatternISetNode.iset_count)
        PatternISetNode.iset_count += 1

    def _parse_words(self, words):
        is_success = True
        splits = words.split(",")
        for word in splits:
            word = word.strip()
            if word == '':
                is_success = False
            else:
                self.add_set_values(word)
        return is_success

    def add_set_values(self, value):
        checkwords = JapaneseLanguage.zenhan_normalize(value)
        checkwords = checkwords.upper()
        if checkwords in self._values:
            return
        self._values[checkwords] = value

        if self._is_CJK is True:
            splits = checkwords
            key = splits[0].upper()
        else:
            splits = checkwords.split()
            key = splits[0].upper()

        if key not in self._words:
            self._words[key] = []
        self._words[key].append(splits)

    @property
    def words(self):
        return self._words

    @property
    def iset_name(self):
        return self._iset_name

    def is_iset(self):
        return True

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<iset userid="%s" words="' % self.userid
        else:
            string += '<iset words="'
        if self._is_CJK is False:
            string += ", ".join(self._words)
        else:
            join_char = ""
            for key in self.words:
                for value in self.words[key]:
                    string += '%s%s' % (join_char, value)
                    join_char = ", "
        string += '">'
        string += super(PatternISetNode, self).to_xml(client_context)
        string += "</iset>\n"
        return string

    def to_string(self, verbose=True):
        if self._is_CJK is False:
            words_str = ",".join(self._words)
        else:
            words_str = ""
            join_char = ""
            for key in self.words:
                for value in self.words[key]:
                    words_str += '%s%s' % (join_char, value)
                    join_char = ","
        if verbose is True:
            return "ISET [%s] [%s] words=[%s]" % (self.userid, self._child_count(verbose), words_str)
        return "ISET words=[%s]" % words_str

    def equivalent(self, other):
        if self.userid != other.userid:
            return False

        if len(self.words) != len(other.words):
            return False

        if self._is_CJK is False:
            for word in self.words:
                if word not in other.words:
                    return False
        else:
            for key in self.words:
                if key not in other.words:
                    return False
                if len(self.words[key]) != len(other.words[key]):
                    return False
                for value in self.words[key]:
                    if value not in other.words[key]:
                        return False

        return True

    def equals(self, client_context, words, word_no):
        if client_context.match_nlu is True:
            return EqualsMatch(False, word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        word = words.word(word_no)
        if word is not None:
            match = self.words_in_set(client_context, words, word_no)
            if match.matched is True:
                YLogger.debug(client_context, "Found word [%s] in iset", word)
                return match

        YLogger.debug(client_context, "No word [%s] found in iset", word)
        return EqualsMatch(False, word_no)

    def words_in_set(self, client_context, words, word_no):
        word = words.word(word_no)
        check_word = JapaneseLanguage.zenhan_normalize(word)
        word = check_word.upper()
        if self._is_CJK is True:
            keyword = word[0]
        else:
            keyword = word

        if keyword in self._words:
            phrases = self._words[keyword]
            phrases = sorted(phrases, key=len, reverse=True)
            for phrase in phrases:
                if self._is_CJK is True:
                    phrase_words = client_context.brain.tokenizer.texts_to_words(phrase)
                    phrase = "".join(phrase_words)
                    phrase_text = phrase
                else:
                    phrase_text = " ".join(phrase)
                phrase_word_no = 0
                words_word_no = word_no
                while phrase_word_no < len(phrase) and words_word_no < words.num_words():
                    word = words.word(words_word_no)
                    check_word = JapaneseLanguage.zenhan_normalize(word)
                    word = check_word.upper()
                    if self._is_CJK is True:
                        phrase_word = phrase[phrase_word_no:(phrase_word_no + len(word))]
                        if phrase_word == word:
                            if (phrase_word_no + len(word)) == len(phrase):
                                return EqualsMatch(True, words_word_no, self._values[phrase_text])
                        else:
                            break
                        phrase_word_no += len(word)
                    else:
                        phrase_word = phrase[phrase_word_no]
                        if phrase_word == word:
                            if phrase_word_no+1 == len(phrase):
                                return EqualsMatch(True, words_word_no, self._values[phrase_text])
                        else:
                            break
                        phrase_word_no += 1
                    words_word_no += 1

        return EqualsMatch(False, word_no)
