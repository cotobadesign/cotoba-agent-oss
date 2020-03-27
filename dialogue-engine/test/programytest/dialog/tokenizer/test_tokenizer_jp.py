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
import unittest

from programy.dialog.tokenizer.tokenizer_jp import TokenizerJP


class TokenizerJPTests(unittest.TestCase):

    def test_tokenizer_normal_texts(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello"], tokenizer.texts_to_words("Hello"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words("Hello World"))
        self.assertEqual(["Hello", "World"], tokenizer.texts_to_words(" Hello   World "))
        self.assertEqual(["こんにちは"], tokenizer.texts_to_words("こんにちは"))
        self.assertEqual(["こんにちは", "良い", "天気", "です", "ね"], tokenizer.texts_to_words("こんにちは良い天気ですね"))
        self.assertEqual(["こんにちは", "良い", "天気", "です", "ね"], tokenizer.texts_to_words(" こんにちは 良い天気ですね "))

        self.assertEqual("", tokenizer.words_to_texts([]))
        self.assertEqual("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts([" Hello ", " World "]))
        self.assertEqual("Hello", tokenizer.words_to_texts(["Hello"]))
        self.assertEqual("こんにちは", tokenizer.words_to_texts(["こんにちは"]))
        self.assertEqual("こんにちは 良い天気ですね", tokenizer.words_to_texts(["こんにちは", "", "良い", "天気", "です", "ね"]))
        self.assertEqual("こんにちは 良い 天気 です ね", tokenizer.words_to_texts([" こんにちは ", " 良い ", " 天気 ", " です ", " ね "]))

    def test_tokenizer_texts_to_words_en(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello,", "he", "is", "Mr.A", "(No", "name)"], tokenizer.texts_to_words("Hello, he is Mr.A (No name)"))

    def test_tokenizer_texts_to_words_jp(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        self.assertEqual(["こんにちは", "「", "良い", "天気", "」", "です", "ね"], tokenizer.texts_to_words("こんにちは「良い天気」ですね"))

    def test_tokenizer_texts_to_words_mix(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        self.assertEqual(["こんにちは", "happy"], tokenizer.texts_to_words("こんにちはhappy"))
        self.assertEqual(["こんにちは", "happy", "です", "か"], tokenizer.texts_to_words("こんにちはhappyですか"))
        self.assertEqual(["こんにちは", "happy", "です", "か"], tokenizer.texts_to_words("こんにちは happy ですか"))
        self.assertEqual(["こんにちは", "(happy)", "です", "か"], tokenizer.texts_to_words("こんにちは（happy）ですか"))

        self.assertEqual(["Hello", "ハッピー"], tokenizer.texts_to_words("Hello ハッピー"))
        self.assertEqual(["Hello", "ハッピー", "です", "か"], tokenizer.texts_to_words("Helloハッピーですか"))
        self.assertEqual(["Hello", "(", "ハッピー", ")", "です", "か"], tokenizer.texts_to_words("Hello (ハッピー)ですか"))
        self.assertEqual(["Hello", "ハッピー", "you"], tokenizer.texts_to_words("Helloハッピーyou"))
        self.assertEqual(["Hello", "ハッピー", "you"], tokenizer.texts_to_words("Hello　ハッピー　you"))

    def test_tokenizer_texts_to_words_en_with_punctation(self):
        punctations = ';\'",!()[]：’”；、。！（）「」'
        tokenizer = TokenizerJP(punctuation_chars=punctations)
        self.assertIsNotNone(tokenizer)

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello", "he", "is", "Mr.A", "No", "name"], tokenizer.texts_to_words("Hello, he is Mr.A (No name)"))

    def test_tokenizer_texts_to_words_jp_with_punctation(self):
        punctations = ';\'",!()[]：’”；、。！（）「」'
        tokenizer = TokenizerJP(punctuation_chars=punctations)

        self.assertEqual(["こんにちは", "良い", "天気", "です", "ね"], tokenizer.texts_to_words("こんにちは「良い天気」ですね"))

    def test_tokenizer_texts_to_words_mix_with_punctation(self):
        punctations = ';\'",!()[]：’”；、。！（）「」'
        tokenizer = TokenizerJP(punctuation_chars=punctations)
        self.assertIsNotNone(tokenizer)

        self.assertEqual(["こんにちは", "happy", "です", "か"], tokenizer.texts_to_words("こんにちはhappyですか"))
        self.assertEqual(["こんにちは", "happy", "です", "か"], tokenizer.texts_to_words("こんにちは happy ですか"))
        self.assertEqual(["こんにちは", "happy", "です", "か"], tokenizer.texts_to_words("こんにちは（happy）ですか"))
        self.assertEqual(["こんにちは", "happy", "です", "か"], tokenizer.texts_to_words("こんにちは「happy]ですか"))
        self.assertEqual(["こんにちは", "happy", "unhappy", "です", "か"], tokenizer.texts_to_words("こんにちは happy, unhappy ですか"))

    def test_tokenizer_template_texts_to_words_en(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)
        tokenizer.is_template = True

        self.assertEqual([], tokenizer.texts_to_words(""))
        self.assertEqual(["Hello, he is Mr.A (No name)"], tokenizer.texts_to_words("Hello, he is Mr.A (No name)"))

    def test_tokenizer_template_texts_to_words_jp(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)
        tokenizer.is_template = True

        self.assertEqual(["こんにちは「良い天気」ですね"], tokenizer.texts_to_words("こんにちは「良い天気」ですね"))

    def test_tokenizer_template_texts_to_words_mix(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)
        tokenizer.is_template = True

        self.assertEqual(["こんにちはhappyですか"], tokenizer.texts_to_words("こんにちはhappyですか"))
        self.assertEqual(["こんにちは happy ですか"], tokenizer.texts_to_words("こんにちは happy ですか"))
        self.assertEqual(["こんにちは（happy）ですか"], tokenizer.texts_to_words("こんにちは（happy）ですか"))

    def test_tokenizer_words_to_texts_en(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "World"]))
        self.assertEqual("Hello World", tokenizer.words_to_texts(["Hello", "", "World"]))
        self.assertEqual("Hello 1 World", tokenizer.words_to_texts(["Hello", "1", "World"]))
        self.assertEqual("Hello < 1 > World", tokenizer.words_to_texts(["Hello", "<", "1", ">", "World"]))
        self.assertEqual("Hello1 1World", tokenizer.words_to_texts(["Hello1", "1World"]))
        self.assertEqual("= Hello1 World =", tokenizer.words_to_texts(["=", "Hello1", "World", "="]))

    def test_tokenizer_words_to_texts_jp(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        self.assertEqual("こんにちは 良い天気ですね", tokenizer.words_to_texts(["こんにちは", "", "良い", "天気", "です", "ね"]))
        self.assertEqual("こんにちは<良い天気>ですね", tokenizer.words_to_texts(["こんにちは", "<", "良い", "天気", ">", "です", "ね"]))
        self.assertEqual("こんにちは<良い天気>ですね", tokenizer.words_to_texts(["こんにちは", "<", "良い", "天気", ">", "です", "ね"]))
        self.assertEqual("<こんにちは良い天気ですね>", tokenizer.words_to_texts(["<", "こんにちは", "良い", "天気", "です", "ね", ">"]))

    def test_tokenizer_words_to_texts_mix(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        self.assertEqual("こんにちは10日はHappy dayですね", tokenizer.words_to_texts(["こんにちは", "10", "日", "は", "Happy", "day", "です", "ね"]))
        self.assertEqual("=こんにちは10日はHappy dayですね=", tokenizer.words_to_texts(["=", "こんにちは", "10", "日", "は", "Happy", "day", "です", "ね", "="]))
        self.assertEqual("pen lightはありますか", tokenizer.words_to_texts(['pen', 'light', 'は', 'あり', 'ます', 'か']))

    def test_tokenizer_words_to_texts_url(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        self.assertEqual("http :// 192.168.1.10 / index.html", tokenizer.words_to_texts(["http", "://", "192.168.1.10", "/", "index.html"]))

    def test_tokenizer_words_to_texts_en_with_symbol(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        self.assertEqual("http :// 192.168.1.10 / index.html", tokenizer.words_to_texts(["http", "://", "192.168.1.10", "/", "index.html"]))

        self.assertEqual("Hello world", tokenizer.words_to_texts(["Hello", " ", " ", "world"]))
        self.assertEqual("Hello . i don ' t know", tokenizer.words_to_texts(["Hello", ".", "i", "don", "'", "t", "know"]))
        self.assertEqual("Hello _ 1 friend_ 1", tokenizer.words_to_texts(["Hello", "_", "1", "friend_", "1"]))
        self.assertEqual("Hello < my friend >", tokenizer.words_to_texts(["Hello", "<", "my", "friend", ">"]))
        self.assertEqual('Hello " my friend "', tokenizer.words_to_texts(["Hello", '"', "my", "friend", '"']))
        self.assertEqual('Hello ` my friend `', tokenizer.words_to_texts(["Hello", "`", "my", "friend", "`"]))

    def test_tokenizer_words_to_texts_with_quote(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        self.assertEqual('Hello " very good " World', tokenizer.words_to_texts(["Hello", '"', "very", "good", '"', "World"]))
        self.assertEqual('Hello "very good" World', tokenizer.words_to_texts(["Hello", '"very', 'good"', "World"]))
        self.assertEqual('こんにちは"良い天気"ですね', tokenizer.words_to_texts(["こんにちは", '"', "良い天気", '"', "です", "ね"]))
        self.assertEqual('こんにちは"良い天気"ですね', tokenizer.words_to_texts(["こんにちは", '"良い天気"', "です", "ね"]))

    def test_tokenizer_words_to_texts_json_tag(self):
        JSON_CHILD_IN = '\uF010'
        JSON_CHILD_OUT = '\uF011'

        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        words1 = [JSON_CHILD_IN, "json", "data", JSON_CHILD_OUT]
        self.assertEqual("\uF010json data\uF011", tokenizer.words_to_texts(words1))

        words2 = [JSON_CHILD_IN, "データ", "設定", JSON_CHILD_OUT]
        self.assertEqual("\uF010データ設定\uF011", tokenizer.words_to_texts(words2))

        words1 = [JSON_CHILD_IN, "json", "設定", JSON_CHILD_OUT]
        self.assertEqual("\uF010json設定\uF011", tokenizer.words_to_texts(words1))

        words2 = [JSON_CHILD_IN, "データ", "json", JSON_CHILD_OUT]
        self.assertEqual("\uF010データjson\uF011", tokenizer.words_to_texts(words2))

        words1 = [JSON_CHILD_IN, "json", "設定", "data", JSON_CHILD_OUT]
        self.assertEqual("\uF010json設定data\uF011", tokenizer.words_to_texts(words1))

        words2 = [JSON_CHILD_IN, "データ", "json", "設定", JSON_CHILD_OUT]
        self.assertEqual("\uF010データjson設定\uF011", tokenizer.words_to_texts(words2))

    def test_tokenizer_words_to_texts_with_json_en(self):
        JSON_CHILD_IN = '\uF010'
        JSON_CHILD_OUT = '\uF011'

        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        words0 = [JSON_CHILD_IN, "json-data", JSON_CHILD_OUT]
        self.assertEqual("\uF010json-data\uF011", tokenizer.words_to_texts(words0))

        words1 = ["Hello", JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, "you"]
        self.assertEqual("Hello \uF010json-data\uF011 you", tokenizer.words_to_texts(words1))

        words2 = ["Hello", '"', JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, '"', "you"]
        self.assertEqual('Hello "\uF010json-data\uF011" you', tokenizer.words_to_texts(words2))

        words3 = ["Hello", JSON_CHILD_IN, "json-data", JSON_CHILD_OUT]
        self.assertEqual('Hello \uF010json-data\uF011', tokenizer.words_to_texts(words3))

        words4 = ["Hello", '"', JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, '"']
        self.assertEqual('Hello "\uF010json-data\uF011"', tokenizer.words_to_texts(words4))

        words5 = [JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, "you"]
        self.assertEqual('\uF010json-data\uF011 you', tokenizer.words_to_texts(words5))

        words6 = ['"', JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, '"', "you"]
        self.assertEqual('"\uF010json-data\uF011" you', tokenizer.words_to_texts(words6))

    def test_tokenizer_words_to_texts_with_json_jp(self):
        JSON_CHILD_IN = '\uF010'
        JSON_CHILD_OUT = '\uF011'

        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        words0 = [JSON_CHILD_IN, "データ", JSON_CHILD_OUT]
        self.assertEqual("\uF010データ\uF011", tokenizer.words_to_texts(words0))

        words1 = ["こんにちは", JSON_CHILD_IN, "データ", JSON_CHILD_OUT, "です", "ね"]
        self.assertEqual("こんにちは\uF010データ\uF011ですね", tokenizer.words_to_texts(words1))

        words2 = ["こんにちは", '"', JSON_CHILD_IN, "データ", JSON_CHILD_OUT, '"', "です", "ね"]
        self.assertEqual('こんにちは"\uF010データ\uF011"ですね', tokenizer.words_to_texts(words2))

        words3 = ["こんにちは", JSON_CHILD_IN, "データ", JSON_CHILD_OUT]
        self.assertEqual('こんにちは\uF010データ\uF011', tokenizer.words_to_texts(words3))

        words4 = ["こんにちは", '"', JSON_CHILD_IN, "データ", JSON_CHILD_OUT, '"']
        self.assertEqual('こんにちは"\uF010データ\uF011"', tokenizer.words_to_texts(words4))

        words5 = [JSON_CHILD_IN, "データ", JSON_CHILD_OUT, "です", "ね"]
        self.assertEqual('\uF010データ\uF011ですね', tokenizer.words_to_texts(words5))

        words6 = ['"', JSON_CHILD_IN, "データ", JSON_CHILD_OUT, '"', "です", "ね"]
        self.assertEqual('"\uF010データ\uF011"ですね', tokenizer.words_to_texts(words6))

    def test_tokenizer_words_to_texts_with_text_jp_json_en(self):
        JSON_CHILD_IN = '\uF010'
        JSON_CHILD_OUT = '\uF011'

        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        words1 = ["こんにちは", JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, "です", "ね"]
        self.assertEqual("こんにちは\uF010json-data\uF011ですね", tokenizer.words_to_texts(words1))

        words2 = ["こんにちは", '"', JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, '"', "です", "ね"]
        self.assertEqual('こんにちは"\uF010json-data\uF011"ですね', tokenizer.words_to_texts(words2))

        words3 = ["こんにちは", JSON_CHILD_IN, "json-data", JSON_CHILD_OUT]
        self.assertEqual('こんにちは\uF010json-data\uF011', tokenizer.words_to_texts(words3))

        words4 = ["こんにちは", '"', JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, '"']
        self.assertEqual('こんにちは"\uF010json-data\uF011"', tokenizer.words_to_texts(words4))

        words5 = [JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, "です", "ね"]
        self.assertEqual('\uF010json-data\uF011ですね', tokenizer.words_to_texts(words5))

        words6 = ['"', JSON_CHILD_IN, "json-data", JSON_CHILD_OUT, '"', "です", "ね"]
        self.assertEqual('"\uF010json-data\uF011"ですね', tokenizer.words_to_texts(words6))

    def test_tokenizer_words_to_texts_with_text_en_json_jp(self):
        JSON_CHILD_IN = '\uF010'
        JSON_CHILD_OUT = '\uF011'

        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        words1 = ["Hello", JSON_CHILD_IN, "データ", JSON_CHILD_OUT, "you"]
        self.assertEqual("Hello\uF010データ\uF011you", tokenizer.words_to_texts(words1))

        words2 = ["Hello", '"', JSON_CHILD_IN, "データ", JSON_CHILD_OUT, '"', "you"]
        self.assertEqual('Hello "\uF010データ\uF011" you', tokenizer.words_to_texts(words2))

        words3 = ["Hello", JSON_CHILD_IN, "データ", JSON_CHILD_OUT]
        self.assertEqual('Hello\uF010データ\uF011', tokenizer.words_to_texts(words3))

        words4 = ["Hello", '"', JSON_CHILD_IN, "データ", JSON_CHILD_OUT, '"']
        self.assertEqual('Hello "\uF010データ\uF011"', tokenizer.words_to_texts(words4))

        words5 = [JSON_CHILD_IN, "データ", JSON_CHILD_OUT, "you"]
        self.assertEqual('\uF010データ\uF011you', tokenizer.words_to_texts(words5))

        words6 = ['"', JSON_CHILD_IN, "データ", JSON_CHILD_OUT, '"', "you"]
        self.assertEqual('"\uF010データ\uF011" you', tokenizer.words_to_texts(words6))

    def test_tokenizer_words_from_current_pos_en(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        with self.assertRaises(Exception):
            tokenizer.words_from_current_pos(None, 0)

        words = ["Yes", "or", "No"]
        self.assertEqual("Yes or No", tokenizer.words_from_current_pos(words, 0))
        self.assertEqual("or No", tokenizer.words_from_current_pos(words, 1))
        self.assertEqual("No", tokenizer.words_from_current_pos(words, 2))
        self.assertEqual("", tokenizer.words_from_current_pos(words, 3))
        self.assertEqual("No", tokenizer.words_from_current_pos(words, -1))
        self.assertEqual("or No", tokenizer.words_from_current_pos(words, -2))
        self.assertEqual("Yes or No", tokenizer.words_from_current_pos(words, -3))
        self.assertEqual("Yes or No", tokenizer.words_from_current_pos(words, -4))

    def test_tokenizer_words_from_current_pos_jp(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        with self.assertRaises(Exception):
            tokenizer.words_from_current_pos(None, 0)

        words = ["ハイ", "か", "イイエ"]
        self.assertEqual("ハイかイイエ", tokenizer.words_from_current_pos(words, 0))
        self.assertEqual("かイイエ", tokenizer.words_from_current_pos(words, 1))
        self.assertEqual("イイエ", tokenizer.words_from_current_pos(words, 2))
        self.assertEqual("", tokenizer.words_from_current_pos(words, 3))
        self.assertEqual("イイエ", tokenizer.words_from_current_pos(words, -1))
        self.assertEqual("かイイエ", tokenizer.words_from_current_pos(words, -2))
        self.assertEqual("ハイかイイエ", tokenizer.words_from_current_pos(words, -3))
        self.assertEqual("ハイかイイエ", tokenizer.words_from_current_pos(words, -4))

    def test_tokenizer_words_from_current_pos_mix(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        with self.assertRaises(Exception):
            tokenizer.words_from_current_pos(None, 0)

        words = ["Yes", "か", "No"]
        self.assertEqual("YesかNo", tokenizer.words_from_current_pos(words, 0))
        self.assertEqual("かNo", tokenizer.words_from_current_pos(words, 1))
        self.assertEqual("No", tokenizer.words_from_current_pos(words, 2))
        self.assertEqual("", tokenizer.words_from_current_pos(words, 3))
        self.assertEqual("No", tokenizer.words_from_current_pos(words, -1))
        self.assertEqual("かNo", tokenizer.words_from_current_pos(words, -2))
        self.assertEqual("YesかNo", tokenizer.words_from_current_pos(words, -3))
        self.assertEqual("YesかNo", tokenizer.words_from_current_pos(words, -4))

    def test_tokenizer_no_test(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        words = tokenizer._texts_to_words_en(None)
        self.assertEqual(0, len(words))
        words = tokenizer._texts_to_words_en('')
        self.assertEqual(0, len(words))

        words = tokenizer._texts_to_words_jp(None)
        self.assertEqual(0, len(words))
        words = tokenizer._texts_to_words_jp('')
        self.assertEqual(0, len(words))

        words = tokenizer._template_texts_to_words_jp(None)
        self.assertEqual(0, len(words))
        words = tokenizer._template_texts_to_words_jp('')
        self.assertEqual(0, len(words))

        texts = tokenizer._words_to_texts(None)
        self.assertEqual("", texts)
        words = tokenizer._words_to_texts('')
        self.assertEqual("", texts)

    def test_tokenizer_convert_url(self):
        tokenizer = TokenizerJP()
        self.assertIsNotNone(tokenizer)

        tokenizer.set_configuration_before_concatenation_rule('.*[ -~]')
        tokenizer.set_configuration_after_concatenation_rule('[ -~].*')

        words = tokenizer.texts_to_words("http://192.168.1.10/index.html")
        self.assertEqual(["http://192.168.1.10/index.html"], words)
        self.assertEqual("http://192.168.1.10/index.html", tokenizer.words_to_texts(words))

        words_en = tokenizer._texts_to_words_en("http://192.168.1.10/index.html")
        self.assertEqual(["http://192.168.1.10/index.html"], words_en)
        self.assertEqual("http://192.168.1.10/index.html", tokenizer.words_to_texts(words_en))

        words_jp = tokenizer._texts_to_words_jp("http://192.168.1.10/index.html")
        self.assertEqual(["http", "://", "192", ".", "168", ".", "1", ".", "10", "/", "index", ".", "html"], words_jp)
        self.assertEqual("http :// 192 . 168 . 1 . 10 / index . html", tokenizer.words_to_texts(words_jp))

        words_mix = tokenizer.texts_to_words("URLはhttp://192.168.1.10/index.html")
        self.assertEqual(["URL", "は", "http://192.168.1.10/index.html"], words_mix)
        self.assertEqual("URLはhttp://192.168.1.10/index.html", tokenizer.words_to_texts(words_mix))
