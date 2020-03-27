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
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

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

import mojimoji


class JapaneseLanguage(object):

    @staticmethod
    def is_CJKword(word):
        for ch in word:
            if JapaneseLanguage.is_CJKchar(ch):
                return True
        return False

    @staticmethod
    def is_CJKchar(c):
        if JapaneseLanguage.is_Symbol(c) is False:
            if JapaneseLanguage.is_Alphabet(c) is False:
                if JapaneseLanguage.is_Numeric(c) is False:
                    return True
        return False

    @staticmethod
    def is_Symbol(c):
        r = [
                (0x0009, 0x0009),   # TAB
                (0x000a, 0x000a),   # LF
                (0x000d, 0x000d),   # CR
                (0x0020, 0x002f),   # 半角記号
                (0x003a, 0x0040),
                (0x005b, 0x0060),
                (0x007b, 0x007e),
                (0x00a1, 0x00ac),
                (0x00ae, 0x00bf),
                (0xff01, 0xff0f),   # 全角記号
                (0xff1a, 0xff20),
                (0xff3b, 0xff40),
                (0xff5b, 0xff60)
            ]
        return any(s <= ord(c) <= e for s, e in r)

    @staticmethod
    def is_Alphabet(c):
        r = [
                (0x0041, 0x005a),   # 半角 英大文字
                (0x0061, 0x007a),   # 半角 英小文字
                (0x00c0, 0x00ff),   # 特殊文字
                (0xff21, 0xff3a),   # 全角 英大文字
                (0xff41, 0xff5a)    # 半角 英小文字
            ]
        return any(s <= ord(c) <= e for s, e in r)

    @staticmethod
    def is_Numeric(c):
        r = [
                (0x0030, 0x0039),   # 半角数字
                (0xff10, 0xff19)    # 全角数字
            ]
        return any(s <= ord(c) <= e for s, e in r)

    @staticmethod
    def zenhan_normalize(texts):
        han_texts = mojimoji.zen_to_han(texts, kana=False)
        zen_texts = mojimoji.han_to_zen(han_texts, digit=False, ascii=False)
        return zen_texts
