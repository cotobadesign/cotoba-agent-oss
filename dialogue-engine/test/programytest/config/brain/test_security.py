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

from programy.config.file.yaml_file import YamlConfigurationFile
from programy.config.brain.security import BrainSecurityAuthorisationConfiguration
from programy.config.brain.security import BrainSecurityAuthenticationConfiguration
from programy.clients.events.console.config import ConsoleConfiguration


class BrainSecurityConfigurationTests(unittest.TestCase):

    def test_authorisation_with_data_denied_srai(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_srai: AUTHORISATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityAuthorisationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual("AUTHORISATION_FAILED", service_config.denied_srai)
        self.assertEqual(BrainSecurityAuthorisationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

    def test_authorisation_with_data_denied_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
                    denied_text: Authorisation Failed
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityAuthorisationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual("Authorisation Failed", service_config.denied_text)
        self.assertIsNone(service_config.denied_srai)

    def test_authorisation_with_data_neither_denied_srai_or_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authorisation:
                    classname: programy.security.authorise.passthrough.PassThroughAuthorisationService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityAuthorisationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authorise.passthrough.PassThroughAuthorisationService", service_config.classname)
        self.assertEqual(BrainSecurityAuthorisationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
        self.assertIsNone(service_config.denied_srai)

    def test_authentication_with_data_denied_srai(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_srai: AUTHENTICATION_FAILED
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityAuthenticationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual("AUTHENTICATION_FAILED", service_config.denied_srai)
        self.assertEqual(BrainSecurityAuthenticationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)

    def test_authentication_with_data_denied_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
                    denied_text: Authentication failed
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityAuthenticationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual("Authentication failed", service_config.denied_text)
        self.assertIsNone(service_config.denied_srai)

    def test_authentication_with_data_neither_denied_srai_or_text(self):
        yaml = YamlConfigurationFile()
        self.assertIsNotNone(yaml)
        yaml.load_from_text("""
        brain:
            security:
                authentication:
                    classname: programy.security.authenticate.passthrough.PassThroughAuthenticationService
        """, ConsoleConfiguration(), ".")

        brain_config = yaml.get_section("brain")
        self.assertIsNotNone(brain_config)
        services_config = yaml.get_section("security", brain_config)
        self.assertIsNotNone(services_config)

        service_config = BrainSecurityAuthenticationConfiguration()
        service_config.load_config_section(yaml, services_config, ".")

        self.assertEqual("programy.security.authenticate.passthrough.PassThroughAuthenticationService", service_config.classname)
        self.assertEqual(BrainSecurityAuthenticationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
        self.assertEqual(BrainSecurityAuthenticationConfiguration.DEFAULT_ACCESS_DENIED, service_config.denied_text)
