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
import xml.etree.ElementTree as ET

from programytest.parser.base import ParserTestsBaseClass
from programy.dialog.sentence import Sentence
from programy.parser.template.nodes.word import TemplateWordNode


class PatternMatcherBaseClass(ParserTestsBaseClass):

    def add_pattern_to_graph(self, pattern, topic="*", that="*", template="test"):

        pattern_element = ET.fromstring("<pattern>%s</pattern>" % (pattern))
        topic_element = ET.fromstring("<topic>%s</topic>" % (topic))
        that_element = ET.fromstring("<that>%s</that>" % (that))
        template_node = TemplateWordNode(template)

        self._client_context.brain.aiml_parser.pattern_parser.add_pattern_to_graph(pattern_element, topic_element, that_element, template_node)

    def match_sentence(self, sentence, topic="*", that="*"):

        return self._client_context.brain.aiml_parser.match_sentence(self._client_context,
                                                                     Sentence(self._client_context.brain.tokenizer, sentence),
                                                                     topic,
                                                                     that)
