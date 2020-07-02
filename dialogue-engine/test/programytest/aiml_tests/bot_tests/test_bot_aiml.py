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
import os

from programytest.client import TestClient


class BotAIMLTestClient(TestClient):

    def __init__(self):
        TestClient.__init__(self)

    def load_storage(self):
        super(BotAIMLTestClient, self).load_storage()
        self.add_default_stores()
        self.add_categories_store([os.path.dirname(__file__)])
        self.add_properties_store(os.path.dirname(__file__) + os.sep + "properties.txt")


class BotAIMLTests(unittest.TestCase):

    def setUp(self):
        client = BotAIMLTestClient()
        self._client_context = client.create_client_context("testid")

    def test_bot_property_xxx(self):
        response = self._client_context.bot.ask_question(self._client_context,  "BOT PROPERTY XXX")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Unknown.")

    def test_bot_property_url(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY URL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Http://www.keithsterling.com/aiml.")

    def test_bot_property_name(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY NAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "KeiffBot 1.0.")

    def test_bot_property_firstname(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY FIRSTNAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keiff.")

    def test_bot_property_middlename(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY MIDDLENAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "AIML.")

    def test_bot_property_lastname(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY LASTNAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "BoT.")

    def test_bot_property_email(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY EMAIL")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Info@keiffbot.org.")

    def test_bot_property_gender(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY GENDER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Male.")

    def test_bot_property_botmaster(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BOTMASTER")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keith Sterling.")

    def test_bot_property_organisation(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY ORGANISATION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Keithsterling.com.")

    def test_bot_property_version(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY VERSION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "0.0.1.")

    def test_bot_property_birthplace(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BIRTHPLACE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Edinburgh, Scotland.")

    def test_bot_property_birthday(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BIRTHDAY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "September 9th.")

    def test_bot_property_sign(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY SIGN")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Virgo.")

    def test_bot_property_birthdate(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY BIRTHDATE")
        self.assertIsNotNone(response)
        self.assertEqual(response, "September 9th, 2016.")

    def test_bot_property_job(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY JOB")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Mobile virtual assistant.")

    def test_bot_property_species(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY SPECIES")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Robot.")

    def test_bot_property_religion(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY RELIGION")
        self.assertIsNotNone(response)
        self.assertEqual(response, "No religion, I am an Atheist.")

    def test_bot_property_logo(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY LOGO")
        self.assertIsNotNone(response)
        self.assertEqual(response, '<img src="http://www.keithsterling.com/aiml/logo.png" width="128"/>.')

    def test_bot_property_default_get(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY DEFAULT GET")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Unknown.")

    def test_bot_property_default_map(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY DEFAULT MAP")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Unknown.")

    def test_bot_property_default_property(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY DEFAULT PROPERTY")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Unknown.")

    def test_bot_property_default_learn_filename(self):
        response = self._client_context.bot.ask_question(self._client_context, "BOT PROPERTY LEARN FILENAME")
        self.assertIsNotNone(response)
        self.assertEqual(response, "Learn.aiml.")
