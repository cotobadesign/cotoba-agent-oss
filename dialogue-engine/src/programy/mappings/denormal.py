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

from programy.mappings.base import DoubleStringPatternSplitCollection
from programy.storage.factory import StorageFactory
from programy.utils.language.japanese import JapaneseLanguage


class DenormalCollection(DoubleStringPatternSplitCollection):

    def __init__(self):
        DoubleStringPatternSplitCollection.__init__(self)
        self._match = {}
        self._match_jp = {}

    def denormalise(self, normal):
        if self.has_keyVal(normal):
            return self.value(normal)
        return None

    def denormalise_string(self, tokenizer, string):
        return self.replace_by_words(tokenizer, string)

    def load(self, storage_factory):
        if storage_factory.entity_storage_engine_available(StorageFactory.DENORMAL) is True:
            lookups_engine = storage_factory.entity_storage_engine(StorageFactory.DENORMAL)
            if lookups_engine:
                try:
                    lookups_store = lookups_engine.denormal_store()
                    lookups_store.load_all(self)
                except Exception as e:
                    YLogger.exception(self, "Failed to load lookups from storage", e)

    def reload(self, storage_factory):
        self.load(storage_factory)

    def empty(self):
        super(DenormalCollection, self).empty()
        self._match.clear()
        self._match_jp.clear()

    def add_to_lookup(self, org_key, org_value):
        key = org_key.strip()
        value = org_value

        if JapaneseLanguage.is_CJKword(org_key) is True:
            if key in self._pairs_jp:
                YLogger.error(self, "%s = %s already exists in jp_collection", key, value)
                return
            else:
                matchs = self._match_jp
                splits = key
                check_key = key[0]
                self._pairs_jp[key] = value
        else:
            if key in self._pairs:
                YLogger.error(self, "%s = %s already exists in en_collection", key, value)
                return
            else:
                matchs = self._match
                splits = key.split()
                check_key = splits[0]
                self._pairs[key] = value

        if check_key not in matchs:
            matchs[check_key] = []
        matchs[check_key].append(splits)

    def replace_by_words(self, tokenizer, replacable):
        resolved = ''

        if tokenizer is None:
            words = replacable.split()
        else:
            tokenizer.is_convert = False
            tokenizer.is_punctuation = False
            words = tokenizer.texts_to_words(replacable)
            tokenizer.is_convert = True
            tokenizer.is_punctuation = True
        if len(words) == 0:
            return resolved

        match_count = 0
        word_no = 0
        is_match = False
        last_CJK = True
        for word in words:
            if match_count > 0:
                match_count -= 1
                word_no += 1
                continue

            word_CJK = JapaneseLanguage.is_CJKword(word)
            if word_CJK is True:
                pairs = self._pairs_jp
                matchs = self._match_jp
                keyword = word[0]
            else:
                pairs = self._pairs
                matchs = self._match
                keyword = word

            if keyword in matchs:
                phrases = matchs[keyword]
                match_count, key = self.match(word_CJK, words, word_no, phrases)
            if match_count > 0:
                resolved += pairs[key]
                match_count -= 1
                is_match = True
                word_CJK = JapaneseLanguage.is_CJKword(pairs[key])
            else:
                if is_match is False:
                    if word_CJK is False or (last_CJK is False and word_CJK is True):
                        resolved += ' '
                is_match = False
                resolved += word
            word_no += 1
            last_CJK = word_CJK

        return resolved.strip()

    def match(self, is_CJK, words, word_no, phrases):
        match_count = 0
        phrases = sorted(phrases, key=len, reverse=True)

        for phrase in phrases:
            key = ''
            phrase_word_no = 0
            words_word_no = word_no
            while phrase_word_no < len(phrase) and words_word_no < len(words):
                if is_CJK is True:
                    word = words[words_word_no]
                    phrase_word = phrase[phrase_word_no:(phrase_word_no + len(word))]
                    if phrase_word == word:
                        key += word
                        match_count += 1
                        if (phrase_word_no + len(word)) == len(phrase):
                            return match_count, key
                    else:
                        match_count = 0
                        break
                    phrase_word_no += len(word)
                else:
                    phrase_word = phrase[phrase_word_no]
                    word = words[words_word_no]
                    if phrase_word == word:
                        if key != '':
                            key += ' '
                        key += word
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
        for line in lines:
            line = line.strip()
            split = self.split_line_by_pattern(line, DoubleStringPatternSplitCollection.RE_OF_SPLIT_PATTERN)
            if split is not None:
                self.add_to_lookup(split[0], split[1])
                count += 1
        return count
