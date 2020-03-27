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
import MeCab
import mojimoji
import re

from programy.dialog.tokenizer.tokenizer import Tokenizer
from programy.utils.language.japanese import JapaneseLanguage

tagger = MeCab.Tagger('-Owakati')


class TokenizerJP(Tokenizer):

    TOKENIZER_CHILD_IN = '\uF010'
    TOKENIZER_CHILD_OUT = '\uF011'

    def __init__(self, split_chars=' ', punctuation_chars=None, before_concatenation_rule=None, after_concatenation_rule=None):
        Tokenizer.__init__(self, split_chars=split_chars, punctuation_chars=punctuation_chars,
                           before_concatenation_rule=before_concatenation_rule,
                           after_concatenation_rule=after_concatenation_rule)

    def _texts_to_words_en(self, texts):
        if not texts:
            return []

        if self._is_template is True:
            words = [word.strip() for word in texts.split(self.split_chars) if word]
            return [" ".join(words)]

        if self.punctuation_chars is None or self._is_punctuation is False:
            new_texts = texts
        else:
            new_texts = ""
            for ch in texts:
                is_append = True
                for punch_ch in self.punctuation_chars:
                    if ch == punch_ch:
                        is_append = False
                        break
                if is_append is True:
                    new_texts += ch

        return [word.strip() for word in new_texts.split(self.split_chars) if word]

    def _texts_to_words_jp(self, texts):
        if not texts:
            return []

        words_text = tagger.parse(texts.strip()).strip()
        words = [word.strip() for word in words_text.split(self.split_chars) if word]

        if self.punctuation_chars is None or self._is_punctuation is False:
            return words
        else:
            new_words = []
            for word in words:
                is_append = True
                for ch in self.punctuation_chars:
                    if word == ch:
                        is_append = False
                        break
                if is_append is True:
                    new_words.append(word)
            return new_words

    def _template_texts_to_words_jp(self, texts):
        if not texts:
            return []
        return [word.strip() for word in texts.split('\n')]

    def _words_to_texts(self, words):
        if not words or len(words) == 0:
            return ''

        texts = ''
        last_word = ''
        is_child_tag = None
        is_tag_text = False
        for word in words:
            if is_tag_text is True:
                if is_child_tag == self.TOKENIZER_CHILD_IN:
                    if last_word != '' and last_word[-1] != '"':
                        if self._check_concatenation_rule(last_word, word) is True:
                            texts += ' '
                    texts += self.TOKENIZER_CHILD_IN
                    is_child_tag = None

                texts += word
                if word == self.TOKENIZER_CHILD_OUT:
                    is_tag_text = False
                    is_child_tag = self.TOKENIZER_CHILD_OUT
                else:
                    last_word = word
                continue

            if word == self.TOKENIZER_CHILD_IN:
                is_tag_text = True
                is_child_tag = self.TOKENIZER_CHILD_IN
                continue

            if word == '　' or word == ' ' or word == '':
                texts += ' '
                last_word = ' '
            else:
                if is_child_tag == self.TOKENIZER_CHILD_OUT and word[0] == '"':
                    texts += word
                else:
                    if self._check_concatenation_rule(last_word, word) is True:
                        texts += ' '
                    texts += word

            last_word = word
            is_child_tag = None

        return texts

    def _check_concatenation_rule(self, last_word, now_word):
        if self.before_concatenation_rule is None or last_word is None:
            return False
        before_match = self.before_concatenation_rule.fullmatch(last_word)
        if before_match is None:
            return False

        if self.after_concatenation_rule is None:
            return False
        after_match = self.after_concatenation_rule.fullmatch(now_word)
        if after_match is None:
            return False

        return True

    def texts_to_words(self, texts):
        if not texts:
            return []

        if self._is_convert is True:
            han_texts = mojimoji.zen_to_han(texts, kana=False)
            zen_texts = mojimoji.han_to_zen(han_texts, digit=False, ascii=False)
        else:
            han_texts = texts
            zen_texts = texts

        if JapaneseLanguage.is_CJKword(zen_texts) is True:
            if self._is_template is False:
                words = []
                target_text = ''
                words_CJK = JapaneseLanguage.is_CJKchar(zen_texts[0])
                for ch in zen_texts:
                    char_CJK = JapaneseLanguage.is_CJKchar(ch)
                    if words_CJK != char_CJK:
                        if words_CJK is True:
                            tmp_words = self._texts_to_words_jp(target_text)
                        else:
                            tmp_words = self._texts_to_words_en(target_text)
                        for word in tmp_words:
                            words.append(word)
                        words_CJK = char_CJK
                        target_text = ''
                    target_text += ch
                if len(target_text) > 0:
                        if words_CJK is True:
                            tmp_words = self._texts_to_words_jp(target_text)
                        else:
                            tmp_words = self._texts_to_words_en(target_text)
                        for word in tmp_words:
                            words.append(word)
            else:
                words = self._template_texts_to_words_jp(texts)
        else:
            if self._is_template is False:
                words = self._texts_to_words_en(han_texts)
            else:
                words = self._texts_to_words_en(texts)
        return words

    def words_to_texts(self, words):
        if not words:
            return ''

        if self.TOKENIZER_CHILD_IN in words:
            # タグ展開文字列の単単語化
            new_words = []
            child_words = []
            is_child = False
            for word in words:
                if word == self.TOKENIZER_CHILD_IN:  # タグ展開文字列の開始コード
                    new_words.append(word)
                    is_child = True

                elif word == self.TOKENIZER_CHILD_OUT:  # タグ展開文字列の終了コード
                    texts = ''
                    if len(child_words) > 0:
                        texts = self.words_to_texts(child_words)
                        new_words.append(texts)
                    new_words.append(word)
                    child_words = []
                    is_child = False

                else:
                    if is_child is False:
                        new_words.append(word)
                    else:
                        if word == '　' or word == ' ' or word == '':
                            new_words.append(word)
                        else:
                            word = word.replace('\\"', '"')
                            child_words.append(word)
            words = new_words

        # 日本語 文字列結合
        texts = self._words_to_texts(words)
        return re.sub(' +', ' ', texts.strip())

    def words_from_current_pos(self, words, current_pos):
        if words:
            return self.words_to_texts(words[current_pos:])
        raise Exception("Num word array violation !")

    def compare(self, value1, value2):
        return value1 == value2
