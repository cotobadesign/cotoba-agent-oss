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

# zipcode api : see http://zip.cgis.biz/

import requests
import re
import xmltodict


def get_zipcode(data):
    zipcode = re.sub("\\D", "", data)
    params = {
        "zn": zipcode
    }
    response = requests.get("http://zip.cgis.biz/xml/zip.php", params=params)
    xml_dict = xmltodict.parse(response.text)
    address = xml_dict["ZIP_result"]["ADDRESS_value"]["value"]

    result = ""
    address_keys = {"@state", "@city", "@word", "@company"}

    for words in address:
        for key, value in words.items():
            if key in address_keys and value != "none":
                result += value

    return result


if __name__ == "__main__":
    print(get_zipcode("163-8001"))
