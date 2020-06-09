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
from abc import ABCMeta, abstractmethod

from programy.utils.language.japanese import JapaneseLanguage


class BaseCollection(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def split_line(self, line):
        """
        Never Implemented
        """


class SingleStringCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._strings = []

    def empty(self):
        self._strings.clear()

    @property
    def strings(self):
        return self._strings

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                self._strings.append(line)
                count += 1
        return count


class DoubleStringCharSplitCollection(BaseCollection):

    def __init__(self):
        BaseCollection.__init__(self)
        self._pairs = []

    def empty(self):
        self._pairs.clear()

    def remove(self, name=None):
        self._pairs.clear()

    @property
    def pairs(self):
        return self._pairs

    def add_value(self, key, value):
        key = key.strip()
        value = value.strip()
        self._pairs.append([key, value])

    def set_value(self, key, value):
        key = key.strip()
        value = value.strip()
        for pair in self._pairs:
            if pair[0] == key:
                pair[1] = value

    def has_keyVal(self, key):
        for pair in self._pairs:
            if pair[0] == key:
                return True
        return False

    def value(self, key):
        for pair in self._pairs:
            if pair[0] == key:
                return pair[1]
        return None

    def get_split_char(self):
        return ','

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        for line in lines:
            line = line.strip()
            kvp = line.split(self.get_split_char())
            if len(kvp) > 1:
                key = kvp[0]
                value = self.get_split_char().join(kvp[1:])
                count += 1
                self.add_value(key, value)
        return count


class DoubleStringPatternSplitCollection(BaseCollection):
    RE_OF_SPLIT_PATTERN = re.compile('\"(.*?)\"[ \t]*,[ \t]*\"(.*?)\"')

    def __init__(self):
        BaseCollection.__init__(self)
        self._pairs = {}
        self._pairs_jp = {}

    def empty(self):
        self._pairs.clear()
        self._pairs_jp.clear()

    def has_keyVal_en(self, key):
        for pair in self._pairs.items():
            if pair[0] == key:
                return True

    def has_keyVal_jp(self, key):
        for pair in self._pairs_jp.items():
            if pair[0] == key:
                return True
        return False

    def has_keyVal(self, key):
        if self.has_keyVal_en(key) is True:
            return True
        return self.has_keyVal_jp(key)

    def value_en(self, key):
        if self.has_keyVal_en(key):
            return self._pairs[key]
        else:
            return None

    def value_jp(self, key):
        if self.has_keyVal_jp(key):
            return self._pairs_jp[key]
        else:
            return None

    def value(self, key):
        value = self.value_en(key)
        if value is not None:
            return value
        return self.value_jp(key)

    def add_to_lookup(self, index, pattern):
        if index in self._pairs:
            YLogger.error(self, "%s = %s already exists in collection", index, pattern)
        self._pairs[index] = pattern

    def replace_by_pattern(self, replacable):
        alreadys = []
        for key, pair in self._pairs.items():
            try:
                pattern = pair[0]
                if pattern.findall(replacable):
                    found = False
                    for already in alreadys:
                        stripped = key.strip()
                        if stripped in already:
                            found = True
                    if found is not True:

                        to_replace = pair[1]
                        to_replace = self.match_case(replacable, to_replace)

                        if pair[1].endswith("."):
                            replacable = pattern.sub(to_replace, replacable)
                        else:
                            replacable = pattern.sub(to_replace+" ", replacable)
                        alreadys.append(pair[1])

            except Exception as excep:
                YLogger.exception(self, "Invalid regular expression [%s]", excep, str(pair[0]))

        return re.sub(' +', ' ', replacable.strip())

    def match_case(self, replacable, to_replace):
        count = 0
        length = len(replacable)

        for i in range(length):
            if replacable[i].isupper():
                count += 1

        if count == length:
            return to_replace.upper()

        if float(count) > float(length)/3.0:
            return to_replace.upper()

        return to_replace.lower()

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        for line in lines:
            line = line.strip()
            split = self.split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)
            if split is not None:
                key, value = self.process_key_value(split[0], split[1])
                self.add_to_lookup(key, value)
                count += 1
        return count

    @staticmethod
    def split_line_by_pattern(line, pattern):
        line = line.strip()
        if line is not None and line:
            match = pattern.search(line)
            if match is not None:
                lhs = match.group(1)
                rhs = match.group(2)
                return [lhs, rhs]
            YLogger.error(None, "Pattern is bad [%s]", line)
        return None

    @staticmethod
    def normalise_pattern(pattern):
        pattern = pattern.replace("(", r"\(")
        pattern = pattern.replace(")", r"\)")
        pattern = pattern.replace("[", r"\[")
        pattern = pattern.replace("]", r"\]")
        pattern = pattern.replace("{", r"\{")
        pattern = pattern.replace("}", r"\}")
        pattern = pattern.replace("|", r"\|")
        pattern = pattern.replace("^", r"\^")
        pattern = pattern.replace("$", r"\$")
        pattern = pattern.replace("+", r"\+")
        pattern = pattern.replace(".", r"\.")
        pattern = pattern.replace("*", r"\*")
        return pattern

    @staticmethod
    def process_key_value(key, value, id=None):
        pattern_text = DoubleStringPatternSplitCollection.normalise_pattern(key)
        start = pattern_text.lstrip()
        middle = pattern_text
        end = pattern_text.rstrip()
        pattern = "(^%s|%s|%s$)" % (start, middle, end)
        replacement = value.upper()
        return key, [re.compile(pattern, re.IGNORECASE), replacement]


class PersonalPronounCollection(DoubleStringPatternSplitCollection):

    def __init__(self, errors_dict=None):
        DoubleStringPatternSplitCollection.__init__(self)
        self._match = {}
        self._match_jp = {}
        self._errors_dict = errors_dict

    def empty(self):
        super(PersonalPronounCollection, self).empty()
        self._match.clear()
        self._match_jp.clear()

    def set_error_info(self, filename, line, description):
        if self._errors_dict is not None:
            error_info = {'file': filename, 'line': line, 'description': description}
            self._errors_dict.append(error_info)

    def add_to_lookup(self, org_key, org_value, filename=None, line=0):
        key = org_key.strip()
        if key == '':
            error_info = "key is empty"
            self.set_error_info(filename, line, error_info)
            return

        target_key = JapaneseLanguage.zenhan_normalize(key)
        target_key = re.sub(' +', ' ', target_key.upper())
        value = org_value.strip()

        if JapaneseLanguage.is_CJKword(target_key) is True:
            if target_key in self._pairs_jp:
                YLogger.error(self, "%s = %s already exists in jp_collection", key, value)
                error_info = "duplicate key='%s' (value='%s' is invalid)" % (key, value)
                self.set_error_info(filename, line, error_info)
                return
            else:
                matchs = self._match_jp
                splits = target_key
                check_key = target_key[0]
                self._pairs_jp[target_key] = value
        else:
            if target_key in self._pairs:
                YLogger.error(self, "%s = %s already exists in en_collection", key, value)
                error_info = "duplicate key='%s' (value='%s' is invalid)" % (key, value)
                self.set_error_info(filename, line, error_info)
                return
            else:
                matchs = self._match
                splits = target_key.split()
                check_key = splits[0]
                self._pairs[target_key] = value

        if check_key not in matchs:
            matchs[check_key] = []
        matchs[check_key].append(splits)

    def replace_by_words(self, tokenizer, replacable):
        resolved = ''

        if tokenizer is None:
            words = replacable.split()
        else:
            tokenizer.is_punctuation = False
            words = tokenizer.texts_to_words(replacable)
            tokenizer.is_punctuation = True
        if len(words) == 0:
            return resolved

        last_CJK = True
        match_count = 0
        word_no = 0
        for word in words:
            if match_count > 0:
                match_count -= 1
                word_no += 1
                continue

            target_word = JapaneseLanguage.zenhan_normalize(word)
            target_word = target_word.upper()
            is_CJK = JapaneseLanguage.is_CJKword(target_word)
            if is_CJK is True:
                pairs = self._pairs_jp
                matchs = self._match_jp
            else:
                pairs = self._pairs
                matchs = self._match

            if is_CJK is True:
                keyword = target_word[0]
            else:
                keyword = target_word
            if keyword in matchs:
                phrases = matchs[keyword]
                match_count, key = self.match(is_CJK, words, word_no, phrases)
            if match_count > 0:
                if is_CJK is False or last_CJK != is_CJK:
                    resolved += ' '
                resolved += pairs[key]
                match_count -= 1
            else:
                if is_CJK is False or last_CJK != is_CJK:
                    resolved += ' '
                resolved += word
            last_CJK = is_CJK
            word_no += 1

        return resolved.strip()

    def match(self, is_CJK, words, word_no, phrases):
        match_count = 0
        phrases = sorted(phrases, key=len, reverse=True)

        for phrase in phrases:
            key = ''
            phrase_word_no = 0
            words_word_no = word_no
            while phrase_word_no < len(phrase) and words_word_no < len(words):
                word = words[words_word_no]
                target_word = JapaneseLanguage.zenhan_normalize(word)
                target_word = target_word.upper()

                if is_CJK is True:
                    phrase_word = phrase[phrase_word_no:(phrase_word_no + len(word))]
                    if phrase_word == target_word:
                        key += target_word
                        match_count += 1
                        if (phrase_word_no + len(word)) == len(phrase):
                            return match_count, key
                    else:
                        match_count = 0
                        break
                    phrase_word_no += len(word)
                else:
                    phrase_word = phrase[phrase_word_no]
                    if phrase_word == target_word:
                        if key != '':
                            key += ' '
                        key += target_word
                        match_count += 1
                        if (phrase_word_no + 1) == len(phrase):
                            return match_count, key
                    else:
                        match_count = 0
                        break
                    phrase_word_no += 1
                words_word_no += 1

        return 0, ''

    def load_from_text(self, text):
        lines = text.split("\n")
        count = 0
        line_no = 0
        for line in lines:
            line_no += 1
            line = line.strip()
            split = self.split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)
            if split is not None:
                self.add_to_lookup(split[0], split[1], 'text', line_no)
                count += 1
        return count
