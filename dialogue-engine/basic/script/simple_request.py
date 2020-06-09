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
import requests
import json


def dialogue(utternce):

    appUrl = 'http://localhost:5100/v1.0/ask'

    params = {
        "userId": "testuser",
        "utterance": utternce,
    }

    headers = {'Content-Type': 'application/json'}
    r = requests.post(url=appUrl, headers=headers, data=json.dumps(params))
    r.encoding = r.apparent_encoding
    r.encoding = 'UTF-8'
    return r.text


if __name__ == '__main__':
    while True:
        utterance = input('>>>')
        result = dialogue(utterance)
        dict = json.loads(result)
        try:
            print(dict["response"])
        except Exception:
            print(dict["error"])
            pass
