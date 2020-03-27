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

from programy.extensions.scheduler.scheduler import SchedulerExtension
from programy.utils.substitutions.substitues import Substitutions

from programytest.client import TestClient


class SchedulerExtensionClient(TestClient):

    def __init__(self, mock_scheduler=None):
        self._mock_scheduler = mock_scheduler
        TestClient.__init__(self)

    def load_configuration(self, arguments, subs: Substitutions = None):
        super(SchedulerExtensionClient, self).load_configuration(arguments, subs)

    def load_scheduler(self):
        if self._mock_scheduler is not None:
            self._scheduler = self._mock_scheduler
        else:
            super(SchedulerExtensionClient, self).load_scheduler()


class SchedulerExtensionTests(unittest.TestCase):

    # SCHEDULE IN|EVERY X SECS|MINS|HOURS|DAYS|WEEKS TEXT|SRAI TEXT ...........

    def test_remind_in_n_seconds(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 SECONDS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_in_n_minutes(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 MINUTES TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_in_n_hours(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 HOURS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_in_n_days(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 DAYS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_in_n_weeks(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE IN 10 WEEKS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_every_n_seconds(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 SECONDS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_every_n_minutes(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 MINUTES TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_every_n_hours(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 HOURS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_every_n_days(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 DAYS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)

    def test_remind_every_n_weeks(self):
        client = SchedulerExtensionClient()
        client_context = client.create_client_context("testid")
        extension = SchedulerExtension()
        response = extension.execute(client_context, "SCHEDULE EVERY 10 WEEKS TEXT WAKEY WAKEY")
        self.assertEqual("OK", response)
