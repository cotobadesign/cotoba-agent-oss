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
import os
import unittest
import json
import unittest.mock

from programy.extensions.weather.weather import WeatherExtension
from programy.utils.weather.metoffice import MetOffice
from programy.utils.geo.google import GoogleMaps

from programytest.client import TestClient


class MockGoogleMaps(GoogleMaps):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self, url):
        with open(self._response_file, "r", encoding="utf-8") as response_data:
            return json.load(response_data)


class MockMetOffice(MetOffice):

    def __init__(self, response_file):
        self._response_file = response_file

    def _get_response_as_json(self):
        with open(self._response_file, "r", encoding="utf-8") as response_data:
            return json.load(response_data)

    def get_forecast_data(self, lat, lon, forecast_type):
        return self._get_response_as_json()

    def get_observation_data(self, lat, lon):
        return self._get_response_as_json()


class MockWeatherExtension(WeatherExtension):

    def __init__(self, maps_file, weather_file):
        self._maps_file = maps_file
        self._weather_file = weather_file

    def get_geo_locator(self, bot):
        return MockGoogleMaps(self._maps_file)

    def get_met_office(self, bot):
        return MockMetOffice(self._weather_file)


class WeatherExtensionTests(unittest.TestCase):

    def setUp(self):
        client = TestClient()
        client.add_license_keys_store()
        self.context = client.create_client_context("testid")

        bot = unittest.mock.Mock()
        self.context.bot = bot
        self.context.brain = bot.brain

    def test_observation(self):
        latlong = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        observation = os.path.dirname(__file__) + os.sep + "observation.json"

        weather = MockWeatherExtension(latlong, observation)
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR WHEN NOW")
        self.assertIsNotNone(result)
        texts = "WEATHER Partly cloudy (day) TEMP 12 3 VISIBILITY V 35000 VF Very Good WIND D SW DF South West S 10 PRESSURE P 1017 PT F PTF Falling HUMIDITY 57 3"
        self.assertEqual(texts, result)

        result = weather.execute(self.context, "OBSERVATION OTHER KY39UR WHEN NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "OBSERVATION LOCATION KY39UR OTHER NOW")
        self.assertIsNone(result)

        result = weather.execute(self.context, "")
        self.assertIsNone(result)

    def test_forecast5day(self):
        latlong = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        forecast = os.path.dirname(__file__) + os.sep + "forecast_daily.json"

        weather = MockWeatherExtension(latlong, forecast)
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST5DAY LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        texts = "WEATHER TYPE Cloudy WINDDIR NW WINDGUST 7 WINDSPEED 4 TEMP 8 FEELS 8 HUMID 76 RAINPROB 8 VISTEXT Very good - Between 20-40 km WEATHER Cloudy"
        self.assertEqual(texts, result)

    def test_forecast24hour(self):
        latlong = os.path.dirname(__file__) + os.sep + "google_latlong.json"
        forecast = os.path.dirname(__file__) + os.sep + "forecast_3hourly.json"

        weather = MockWeatherExtension(latlong, forecast)
        self.assertIsNotNone(weather)

        result = weather.execute(self.context, "FORECAST24HOUR LOCATION KY39UR WHEN 1")
        self.assertIsNotNone(result)
        texts = "WEATHER Overcast TEMP 10 FEELS 10 WINDDIR NW WINDDIRFULL North West WINDSPEED 4 VIS Very good - Between 20-40 km UVINDEX 0 UVGUIDE None RAINPROB 8 HUMIDITY 73"
        self.assertEqual(texts, result)
