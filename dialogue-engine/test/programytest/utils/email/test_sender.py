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

from programy.utils.email.sender import EmailSender
from programy.utils.email.config import EmailConfiguration


class MockSMTPServer(object):

    def __init__(self, host, port):
        self._ehlo = False
        self._starttls = False
        self._login = False
        self._send_message = False
        self._quit = False

    def ehlo(self):
        self._ehlo = True

    def starttls(self):
        self._starttls = True

    def login(self, username, password):
        self._login = True

    def send_message(self, msg):
        self._send_message = True

    def quit(self):
        self._quit = True


class TestEmailSender(EmailSender):

    def __init__(self, config: EmailConfiguration):
        EmailSender.__init__(self, config)

    def _smtp_server(self, host, port):
        return MockSMTPServer(host, port)


class EmailSenderTests(unittest.TestCase):

    def test_send(self):

        config = EmailConfiguration()

        sender = EmailSender(config)

        sender.send("fred@west.com", "New patio", "Do you need any help with the slabs?")
