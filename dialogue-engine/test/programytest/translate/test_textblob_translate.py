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

from programy.translate.textblob_translator import TextBlobTranslator


class TestTextBlobTranslator(unittest.TestCase):

    def test_languages(self):
        translator = TextBlobTranslator()
        languages = translator.languages()
        self.assertTrue(languages.startswith("AFRIKAANS, ALBANIAN, "))

        self.assertTrue(translator.supports_language('ENGLISH'))
        self.assertFalse(translator.supports_language('KLINGON'))

    def test_language_codes(self):
        translator = TextBlobTranslator()
        self.assertEqual("EN", translator.language_code("ENGLISH"))
        self.assertEqual("UNKNOWN", translator.language_code("KLINGON"))

    def test_detect_language(self):
        translator = TextBlobTranslator()
        self.assertEqual("EN", translator.detect("Hello"))
        self.assertEqual("FR", translator.detect("Bonjour"))
        # Cantonese, currently not supported by Google Translate
        self.assertEqual("UNKNOWN", translator.detect("粵語", "UNKNOWN"))

    def test_translate(self):
        translator = TextBlobTranslator()
        translated = translator.translate("Hello", from_lang='EN', to_lang='FR')
        self.assertTrue("Bonjour", translated)
