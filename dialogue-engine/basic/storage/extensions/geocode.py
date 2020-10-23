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
# geocode api : see https://www.geocoding.jp/api/

from programy.utils.logging.ylogger import YLogger
from programy.extensions.base import Extension
import json
import requests
import xmltodict
from vincenty_inverse import CalcDistance


class GeocodeExtension(Extension):

    def get_geocode(self, data):
        params = {
            "q": data
        }
        response = requests.get("https://www.geocoding.jp/api/", params=params)
        xml_dict = xmltodict.parse(response.text)
        lat = xml_dict["result"]["coordinate"]["lat"]
        lng = xml_dict["result"]["coordinate"]["lng"]

        return lat, lng

    def execute(self, context, data):
        try:
            conversation = context.bot.get_conversation(context)
            user_place = conversation.current_question().property("user_place")
            user_lat = float(conversation.current_question().property("user_lat"))
            user_lng = float(conversation.current_question().property("user_lng"))

            lat, lng = self.get_geocode(data)

            coordinate = {"departure": user_place, "arrival": data, "lat": lat, "lng": lng}
            conversation.current_question().set_property("coordinate", json.dumps(coordinate, ensure_ascii=False))

            cd = CalcDistance()
            distance = int(cd.vincenty_inverse(user_lat, user_lng, float(lat), float(lng)))

            return str(distance)

        except Exception:
            YLogger.debug(context, "Extension Zip2Address: None")
            return None
