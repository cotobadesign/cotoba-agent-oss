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

from programy.security.linking.extension import AccountLinkingExtension


class AccountLinkerExtensionAsserts(unittest.TestCase):

    def assert_unknown_command(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, "UNKNOWN COMMAND"))
        self.assertEquals("ACCOUNT LINK FAILED UNKNOWN COMMAND", extension.execute(context, "LINK UNKNOWN"))

    def assert_primary_account_link_success(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"

        result = extension.execute(context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("PRIMARY ACCOUNT LINKED"))
        words = result.split(" ")
        self.assertEqual(4, len(words))

    def assert_primary_account_link_failures(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT"))
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT USERID"))
        self.assertEquals("INVALID PRIMARY ACCOUNT COMMAND", extension.execute(context, "LINK PRIMARY ACCOUNT USERID CLIENT"))

    def assert_secondary_account_link_success(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        command = "LINK PRIMARY ACCOUNT TESTUSER CONSOLE PASSWORD123"
        result = extension.execute(context, command)
        words = result.split(" ")
        self.assertEqual(4, len(words))

        command = "LINK SECONDARY ACCOUNT TESTUSER TESTUSER2 FACEBOOK PASSWORD123 %s" % words[3]

        result = extension.execute(context, command)
        self.assertIsNotNone(result)
        self.assertTrue(result.startswith("SECONDARY ACCOUNT LINKED"))

    def assert_secondary_account_link_failures(self, context):

        extension = AccountLinkingExtension()
        self.assertIsNotNone(extension)

        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER"))
        self.assertEquals("INVALID SECONDARY ACCOUNT COMMAND", extension.execute(context, "LINK SECONDARY ACCOUNT PRIMARY_USER SECONDARY_CLIENT PRIMARY_USER GIVEN_TOKEN"))
