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

import re

from programy.utils.logging.ylogger import YLogger
from programy.utils.classes.loader import ClassLoader


class Tokenizer(object):

    def __init__(self, split_chars=' ', punctuation_chars=None,
                 before_concatenation_rule=None, after_concatenation_rule=None):
        self.split_chars = split_chars
        self.punctuation_chars = punctuation_chars

        try:
            self.before_concatenation_rule = re.compile(before_concatenation_rule)
        except Exception:
            self.before_concatenation_rule = None

        try:
            self.after_concatenation_rule = re.compile(after_concatenation_rule)
        except Exception:
            self.after_concatenation_rule = None

        self._is_template = False
        self._is_punctuation = True
        self._is_convert = True

    @property
    def is_template(self):
        return self._is_template

    @is_template.setter
    def is_template(self, is_template):
        self._is_template = is_template

    @property
    def is_punctuation(self):
        return self._is_punctuation

    @is_punctuation.setter
    def is_punctuation(self, is_punctuation):
        self._is_punctuation = is_punctuation

    @property
    def is_convert(self):
        return self._is_convert

    @is_convert.setter
    def is_convert(self, is_convert):
        self._is_convert = is_convert

    def set_configuration_punctuation_chars(self, punctuations):
        self.punctuation_chars = punctuations

    def set_configuration_before_concatenation_rule(self, before_rule):
        try:
            self.before_concatenation_rule = re.compile(before_rule)
        except Exception:
            pass

    def set_configuration_after_concatenation_rule(self, after_rule):
        try:
            self.after_concatenation_rule = re.compile(after_rule)
        except Exception:
            pass

    def texts_to_words(self, texts):
        if not texts:
            return []
        return [word.strip() for word in texts.split(self.split_chars) if word]

    def words_to_texts(self, words):
        if not words:
            return ''
        to_join = [word.strip() for word in words if word]
        return self.split_chars.join(to_join)

    def words_from_current_pos(self, words, current_pos):
        if not words:
            return ''
        return self.split_chars.join(words[current_pos:])

    def compare(self, value1, value2):
        return value1 == value2

    @staticmethod
    def load_tokenizer(configuration):
        if configuration is not None and configuration.tokenizer.classname is not None:
            YLogger.debug(None, "Loading tokenizer from class [%s]", configuration.tokenizer.classname)
            tokenizer_class = ClassLoader.instantiate_class(configuration.tokenizer.classname)
            return tokenizer_class(configuration.tokenizer.split_chars, configuration.tokenizer.punctuation_chars,
                                   configuration.tokenizer.before_concatenation_rule,
                                   configuration.tokenizer.after_concatenation_rule)
        else:
            tokenizer_class = ClassLoader.instantiate_class('programy.dialog.tokenizer.tokenizer_jp.TokenizerJP')
            return tokenizer_class(configuration.tokenizer.split_chars, configuration.tokenizer.punctuation_chars,
                                   configuration.tokenizer.before_concatenation_rule,
                                   configuration.tokenizer.after_concatenation_rule)
