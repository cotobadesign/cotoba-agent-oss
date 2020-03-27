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
    def test_oob_stripping(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        response, oob = brain.strip_oob("<oob>command</oob>")
        self.assertEqual("", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob>")
        self.assertEqual("This ", response)
        self.assertEqual("<oob>command</oob>", oob)

        response, oob = brain.strip_oob("This <oob>command</oob> That")
        self.assertEqual("This That", response)
        self.assertEqual("<oob>command</oob>", oob)

    def test_oob_processing(self):

        yaml = YamlConfigurationFile()
        self.load_os_specific_configuration(yaml, "test_brain.yaml", "test_brain.windows.yaml")

        brain_config = BrainConfiguration()
        brain_config.load_configuration(yaml, ".")

        client = TestClient()
        client_context = client.create_client_context("testid")
        brain = Brain(client_context.bot, brain_config)

        self.assertEqual("", brain.process_oob("console", "<oob></oob>"))

"""
