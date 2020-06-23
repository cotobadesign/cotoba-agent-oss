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


class PatternBotNode(PatternNode):

    def __init__(self, attribs, text, userid='*', element=None, brain=None):
        PatternNode.__init__(self, userid)
        if 'name' in attribs:
            self._property = attribs['name']
        elif 'property' in attribs:
            self._property = attribs['property']
        elif text:
            self._property = text
        else:
            raise ParserException("No parameter specified as attribute or text", xml_element=element, nodename='bot(pattern)')

        if self._property == '':
            raise ParserException("No parameter specified as attribute or text", xml_element=element, nodename='bot(pattern)')

        if brain is not None:
            if brain.properties.has_property(self._property) is False:
                raise ParserException("Bot_property[%s] not found" % self._property, xml_element=element, nodename='bot(pattern)')

    def is_bot(self):
        return True

    @property
    def property(self):
        return self._property

    def to_xml(self, client_context, include_user=False):
        string = ""
        if include_user is True:
            string += '<bot userid="%s" property="%s">\n' % (self.userid, self.property)
        else:
            string += '<bot property="%s">\n' % self.property
        string += super(PatternBotNode, self).to_xml(client_context)
        string += "</bot>"
        return string

    def to_string(self, verbose=True):
        if verbose is True:
            return "BOT [%s] [%s] property=[%s]" % (self.userid, self._child_count(verbose), self.property)
        return "BOT property=[%s]" % (self.property)

    def equivalent(self, other):
        if other.is_bot():
            if self.userid == other.userid:
                if self.property == other.property:
                    return True
        return False

    def equals(self, client_context, words, word_no):
        if client_context.match_nlu is True:
            return EqualsMatch(False, word_no)

        word = words.word(word_no)

        if self.userid != '*':
            if self.userid != client_context.userid:
                return EqualsMatch(False, word_no)

        if client_context.brain.properties.has_property(self.property):
            value = client_context.brain.properties.property(self.property)
            value_len = len(value)
            word_len = len(word)
            texts = word
            add_count = 0
            if value_len > word_len:
                texts_len = word_len
                check_index = 0
                for word in words.words:
                    if check_index <= word_no:
                        check_index += 1
                        continue
                    if word == '__TOPIC__':
                        break
                    texts_len += len(word)
                    texts += word
                    add_count += 1
                    if texts_len >= value_len:
                        break

            check_texts = JapaneseLanguage.zenhan_normalize(texts)
            value_texts = JapaneseLanguage.zenhan_normalize(value)
            if check_texts.upper() == value_texts.upper():
                word_no += add_count
                YLogger.debug(client_context, "Found words [%s] as bot property", value)
                return EqualsMatch(True, word_no, value)

        return EqualsMatch(False, word_no)
