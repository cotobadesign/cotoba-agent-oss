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
from xml.etree.ElementTree import ParseError

from programy.bot import Bot
from programy.config.bot.bot import BotConfiguration
from programy.parser.exceptions import ParserException

from programytest.client import TestClient
from programy.utils.classes.loader import ClassLoader


class AIMLParserErrorTests(unittest.TestCase):

    def setUp(self):
        bot_config = BotConfiguration()

        bot = Bot(bot_config, TestClient())

        bot.brain.configuration.debugfiles._save_errors = True
        bot.brain.configuration.debugfiles._save_duplicates = True

        bot.brain.template_factory.add_node("base", ClassLoader.instantiate_class("programy.parser.template.nodes.base.TemplateNode"))
        bot.brain.template_factory.add_node("word", ClassLoader.instantiate_class("programy.parser.template.nodes.word.TemplateWordNode"))

        bot.brain.pattern_factory.add_node("oneormore", ClassLoader.instantiate_class("programy.parser.pattern.nodes.oneormore.PatternOneOrMoreWildCardNode"))
        bot.brain.pattern_factory.add_node("topic", ClassLoader.instantiate_class("programy.parser.pattern.nodes.topic.PatternTopicNode"))
        bot.brain.pattern_factory.add_node("that", ClassLoader.instantiate_class("programy.parser.pattern.nodes.that.PatternThatNode"))
        bot.brain.pattern_factory.add_node("template", ClassLoader.instantiate_class("programy.parser.pattern.nodes.template.PatternTemplateNode"))
        bot.brain.pattern_factory.add_node("bot", ClassLoader.instantiate_class("programy.parser.pattern.nodes.bot.PatternBotNode"))
        bot.brain.pattern_factory.add_node("set", ClassLoader.instantiate_class("programy.parser.pattern.nodes.set.PatternSetNode"))
        bot.brain.pattern_factory.add_node("nlu", ClassLoader.instantiate_class("programy.parser.pattern.nodes.nlu.PatternNluNode"))
        bot.brain.pattern_factory.add_node("word", ClassLoader.instantiate_class("programy.parser.pattern.nodes.word.PatternWordNode"))

        self.parser = bot.brain.aiml_parser

        self.parser.create_debug_storage()
        self.assertIsNotNone(self.parser)

    def test_parse_from_file_invalid(self):
        filename = os.path.dirname(__file__) + '/invalid.aiml'
        self.parser.parse_from_file(filename)

    def test_no_content(self):
        with self.assertRaises(ParseError):
            self.parser.parse_from_text(
                """
                """)

    def test_crud(self):
        with self.assertRaises(ParseError):
            self.parser.parse_from_text(
                """Blah Blah Blah
                """)

    def test_no_aiml(self):
        with self.assertRaises(ParseError) as raised:
            self.parser.parse_from_text(
                """<?xml version="1.0" encoding="UTF-8"?>
                """)
        self.assertTrue(str(raised.exception).startswith("no element found:"))

    def test_invlid_aiml(self):
        with self.assertRaises(ParserException) as raised:
            self.parser.parse_from_text(
                """<?xml version="1.0" encoding="UTF-8"?>
                <aimlx>
                </aimlx>
                """)
        self.assertTrue(str(raised.exception).startswith("Root tag is not <aiml>"))

    def test_base_aiml_category_no_content(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual('No template node found in category', self.parser._errors[0][6])

    def test_base_aiml_invalid_top_tag(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <categori>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </categori>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual('Unknown top level tag [categori]', self.parser._errors[0][6])

    def test_base_aiml_category_no_pattern(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No pattern node found in category", self.parser._errors[0][6])

    def test_base_aiml_category_multi_pattern(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                    <pattern>test</pattern>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Multiple <pattern> nodes found in category", self.parser._errors[0][6])

    def test_base_aiml_category_no_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No template node found in category", self.parser._errors[0][6])

    def test_base_aiml_category_multi_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <template>RESPONSE1</template>
                    <template>RESPONSE2</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Multiple <template> nodes found in category", self.parser._errors[0][6])

    def test_base_aiml_category_multi_topic(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <topic>*</topic>
                    <pattern>*</pattern>
                    <template>RESPONSE1</template>
                    <topic>test</topic>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Multiple <topic> nodes found in category", self.parser._errors[0][6])

    def test_base_aiml_category_multi_that(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>*</pattern>
                    <that>*</that>
                    <template>RESPONSE1</template>
                    <that>test</that>
               </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Multiple <that> nodes found in category", self.parser._errors[0][6])

    def test_base_aiml_topic_empty_parent_node(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="">
                    <category>
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic name empty or null", self.parser._errors[0][6])

    def test_base_aiml_topic_with_something_else(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <xxxx>
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </xxxx>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Unknown child node of topic, xxxx", self.parser._errors[0][6])

    def test_base_aiml_topic_empty_child_node1(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <topic name="" />
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic node text is empty", self.parser._errors[0][6])

    def test_base_aiml_topic_empty_child_node2(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <topic></topic>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic node text is empty", self.parser._errors[0][6])

    def test_base_aiml_that_empty_child_node(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <that></that>
                    <pattern>*</pattern>
                    <template>RESPONSE</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("That node text is empty", self.parser._errors[0][6])

    def test_base_aiml_topic_no_name(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Missing name attribute for topic", self.parser._errors[0][6])

    def test_base_aiml_topic_no_category(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No categories in topic", self.parser._errors[0][6])

    def test_base_aiml_topic_category_no_content(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No template node found in category", self.parser._errors[0][6])

    def test_base_aiml_topic_at_multiple_levels(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <topic name="test2" />
                        <pattern>*</pattern>
                        <template>RESPONSE</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("Topic exists in category AND as parent node", self.parser._errors[0][6])

    def test_base_aiml_topic_category_no_template(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>*</pattern>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._errors)
        self.assertIsNotNone(self.parser._errors)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual("No template node found in category", self.parser._errors[0][6])

    def test_base_aiml_category_duplicate(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST</pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST</pattern>
                    <template>RESPONSE2</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(1, len(self.parser._duplicates))
        self.assertEqual("Duplicate grammar tree found [TEST]", self.parser._duplicates[0][5])

    def test_base_aiml_category_duplicate_nlu(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern><nlu intent="aaa" score="0.9" /></pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern><nlu intent="aaa" score="0.9" /></pattern>
                    <template>RESPONSE2</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(1, len(self.parser._duplicates))
        self.assertEqual("Duplicate grammar tree found [intent=aaa, score=0.9]", self.parser._duplicates[0][5])

    def test_base_aiml_category_duplicate_no_text(self):
        self.parser.brain.properties.add_property("name", "value")
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern><bot name="name" /></pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern><bot name="name" /></pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(1, len(self.parser._duplicates))
        self.assertEqual("Duplicate grammar tree found for [TAG defined]", self.parser._duplicates[0][5])

    def test_base_aiml_topic_category_duplicate(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>TEST</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>TEST</pattern>
                        <template>RESPONSE2</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(1, len(self.parser._duplicates))
        self.assertEqual("Duplicate grammar tree found [TEST]", self.parser._duplicates[0][5])

    def test_base_aiml_topic_category_duplicate_no_text(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>*</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>*</pattern>
                        <template>RESPONSE2</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(1, len(self.parser._duplicates))
        self.assertEqual("Duplicate grammar tree found [*]", self.parser._duplicates[0][5])

    def test_base_aiml_topic_category_not_duplicate(self):
        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST1</pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>TEST1</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test2">
                    <category>
                        <pattern>TEST1</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>TEST2</pattern>
                        <template>RESPONSE2</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST2</pattern>
                    <template>RESPONSE2</template>
                </category>
            </aiml>
            """)
        self.assertIsNotNone(self.parser._duplicates)
        self.assertEqual(0, len(self.parser._duplicates))

    def test_base_aiml_category_over(self):
        self.parser.brain.bot.configuration._max_categories = 2

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST1</pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertEqual(0, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST2</pattern>
                    <template>RESPONSE2</template>
                </category>
            </aiml>
            """)
        self.assertEqual(0, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST3</pattern>
                    <template>RESPONSE3</template>
                </category>
            </aiml>
            """)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))
        self.assertEqual("Max categories [2] exceeded", self.parser._errors[0][6])

    def test_base_aiml_category_over_in_topic(self):
        self.parser.brain.bot.configuration._max_categories = 2

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test1">
                    <category>
                        <pattern>TEST1</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertEqual(0, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test2">
                    <category>
                        <pattern>TEST1</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertEqual(0, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test3">
                    <category>
                        <pattern>TEST1</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))
        self.assertEqual("Max categories [2] exceeded", self.parser._errors[0][6])

    def test_base_aiml_category_over_mix(self):
        self.parser.brain.bot.configuration._max_categories = 2

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST1</pattern>
                    <template>RESPONSE1</template>
                </category>
            </aiml>
            """)
        self.assertEqual(0, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <category>
                    <pattern>TEST2</pattern>
                    <template>RESPONSE2</template>
                </category>
            </aiml>
            """)
        self.assertEqual(0, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))

        self.parser.parse_from_text(
            """<?xml version="1.0" encoding="UTF-8"?>
            <aiml>
                <topic name="test">
                    <category>
                        <pattern>TEST1</pattern>
                        <template>RESPONSE1</template>
                    </category>
                </topic>
            </aiml>
            """)
        self.assertEqual(1, len(self.parser._errors))
        self.assertEqual(0, len(self.parser._duplicates))
        self.assertEqual("Max categories [2] exceeded", self.parser._errors[0][6])
