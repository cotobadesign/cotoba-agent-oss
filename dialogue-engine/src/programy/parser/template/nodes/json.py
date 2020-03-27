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
Copyright (c) 2016-2018 Keith Sterling http://www.keithsterling.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

from programy.utils.logging.ylogger import YLogger

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
import json


class TemplateJsonNode(TemplateNode):

    JSON_CHILD_MARK = '\uF000'
    JSON_CHILD_IN = '\uF010'
    JSON_CHILD_OUT = '\uF011'

    def __init__(self):
        TemplateNode.__init__(self)
        self._name = None
        self._type = None
        self._function = None
        self._index = None
        self._item = None
        self._key = None
        self._is_convert = True

    def resolve_children(self, client_context):
        if self._children:
            return self.resolve_children_to_string(client_context)
        return ""

    def _json_set_elements(self, client_context, json_dict, resolved):
        if self.index != "":
            try:
                indexNo = int(self.index)
            except Exception:
                YLogger.debug(client_context, "JSON set failed %s(invalid index[%s])", self.keys, self.index)
                return ''

        is_success = False
        first = True
        dic = json_dict
        is_listParam = False
        is_JsonParam = False

        if resolved[0] == self.JSON_CHILD_IN:
            check_text = resolved[1:].strip()
            check_chr = check_text[0]
        else:
            check_chr = resolved[0]
        if check_chr == '{':
            resolved = self._delete_child_mark(resolved, is_json=True)
            try:
                words = json.loads(resolved)
                is_JsonParam = True
            except Exception:
                YLogger.debug(client_context, "JSON set failed %s(Not JSON-Format[%s])", self.keys, resolved)
                return ''
        else:
            resolved = self._delete_child_mark(resolved)
            split_words, _ = self._text_to_list(resolved)
            words = []
            if len(split_words) == 1:
                word = self._word_to_data(split_words[0], True)
                if word is None:
                    return ''
                if self.function == 'insert':
                    words.append(word)
                else:
                    if word == '""':
                        word = ''
                    words = word
            elif len(split_words) > 1:
                is_listParam = True
                for temp in split_words:
                    word = self._word_to_data(temp, False)
                    if word is None:
                        return ''
                    words.append(word)
            else:
                return ''

        try:
            for key in self.keys:
                if first:
                    first = False
                    continue
                if key == self.keys[-1]:
                    if self.index != "":
                        if key not in dic:
                            if indexNo == 0 or indexNo == -1:
                                dic[key] = []
                            else:
                                break
                        elif type(dic[key]) is not list:
                            break

                        diclen = len(dic[key])
                        if self.function == 'insert':
                            if indexNo == -1 or indexNo == diclen:
                                if is_JsonParam is True:
                                    dic[key].append(words)
                                else:
                                    for word in words:
                                        value = self._convert_json_value(word)
                                        dic[key].append(value)
                                is_success = True
                            else:
                                if indexNo < 0:
                                    indexNo += diclen + 1
                                if indexNo < 0 or indexNo >= diclen:
                                    break

                                if is_JsonParam is True:
                                    dic[key].insert(indexNo, words)
                                else:
                                    for word in words:
                                        value = self._convert_json_value(word)
                                        dic[key].insert(indexNo, value)
                                        indexNo += 1
                                is_success = True
                        else:
                            if indexNo < 0:
                                indexNo += diclen
                            if indexNo < 0 or indexNo >= diclen:
                                break

                            dic = dic[key]
                            if is_listParam is True:
                                dic[indexNo] = []
                                for word in words:
                                    value = self._convert_json_value(word)
                                    dic[indexNo].append(value)
                            elif is_JsonParam is True:
                                dic[indexNo] = words
                            else:
                                value = self._convert_json_value(words)
                                dic[indexNo] = value
                            is_success = True
                    else:
                        if is_listParam is True:
                            dic[key] = []
                            for word in words:
                                value = self._convert_json_value(word)
                                dic[key].append(value)
                        elif is_JsonParam is True:
                            dic[key] = words
                        else:
                            value = self._convert_json_value(words)
                            dic[key] = value
                        is_success = True
                else:
                    if key in dic.keys():
                        if type(dic[key]) is not dict:
                            dic[key] = {}
                            dic = dic[key]
                        else:
                            dic = dic[key]
                    else:
                        dic[key] = {}
                        dic = dic[key]

        except Exception:
            pass

        if is_success is False:
            YLogger.debug(client_context, "JSON set failed %s func=[%s] index=[%s] string [%s]", self.keys, self.function, self.index, resolved)
        else:
            conversation = client_context.bot.get_conversation(client_context)
            if self._type == "var":
                if conversation.has_current_question():
                    conversation.current_question().set_property(self.keys[0], json.dumps(json_dict, ensure_ascii=False))
            elif self._type == "data":
                conversation.set_data_property(self.keys[0], json.dumps(json_dict, ensure_ascii=False))
            elif self._type == "name":
                conversation.set_property(self.keys[0], json.dumps(json_dict, ensure_ascii=False))
            YLogger.debug(client_context, "JSON set complete %s func=[%s] index=[%s] string [%s]", self.keys, self.function, self.index, resolved)
        return ''

    def _convert_json_value(self, word):
        if word == '""':
            return ''

        if self._is_convert is True:
            if word == 'null':
                return None
            elif word == 'true':
                return True
            elif word == 'false':
                return False
            else:
                try:
                    value = float(word)
                    if '.' not in word:
                        return int(word)
                    else:
                        if word[-1] == '.':
                            return word
                        else:
                            return value
                except ValueError:
                    pass

        return word

    def _json_delete_elements(self, client_context, json_dict):
        if self.index != "":
            try:
                indexNo = int(self.index)
            except Exception:
                YLogger.debug(client_context, "JSON delete failed %s(invalid index[%s])", self.keys, self.index)
                return ''

        is_success = False
        if json_dict is not None:
            try:
                first = True
                dic = json_dict
                for key in self.keys:
                    if first:
                        first = False
                        continue
                    if key == self.keys[-1]:
                        break
                    elif key in dic.keys():
                        dic = dic[key]
                    else:
                        return ''

                if self.index != "":
                    dic = dic[key]
                    diclen = len(dic)
                    if indexNo < 0:
                        indexNo += diclen
                    if indexNo >= 0 and indexNo < diclen:
                        if type(dic) is dict:
                            for loop, indexKey in enumerate(dic):
                                if loop == indexNo:
                                    del dic[indexKey]
                                    is_success = True
                                    break
                        else:
                            del dic[indexNo]
                            is_success = True
                else:
                    del dic[key]
                    is_success = True

                if is_success is True:
                    conversation = client_context.bot.get_conversation(client_context)
                    if self._type == "var":
                        if conversation.has_current_question():
                            conversation.current_question().set_property(self.keys[0], json.dumps(json_dict, ensure_ascii=False))
                    elif self._type == "data":
                        conversation.set_data_property(self.keys[0], json.dumps(json_dict, ensure_ascii=False))
                    elif self._type == "name":
                        conversation.set_property(self.keys[0], json.dumps(json_dict, ensure_ascii=False))

            except Exception:
                pass

        if is_success is False:
            YLogger.debug(client_context, "Template-JSON delete failed %s index[%s]", self.keys, self.index)
        else:
            YLogger.debug(client_context, "Template-JSON  delete complete %s index[%s]", self.keys, self.index)
        return ''

    def _json_get_elements(self, client_context, json_dict):
        if self.index != "":
            try:
                indexNo = int(self.index)
            except Exception:
                resolved = TemplateGetNode.get_default_value(client_context)
                YLogger.debug(client_context, "Template-JSON failed to get (invalid index[%s])", self.index)
                return resolved

        resolved = ''
        if json_dict is not None:
            try:
                first = True
                for key in self.keys:
                    if first:
                        first = False
                        continue
                    json_dict = json_dict[key]

                if type(json_dict) is dict or type(json_dict) is list:
                    dic_len = len(json_dict)
                    if self.function == 'len':
                        resolved = str(dic_len)
                    elif self.index != "":
                        if indexNo < 0:
                            indexNo += dic_len
                            if indexNo < 0:
                                indexNo = dic_len
                        if indexNo < dic_len:
                            if type(json_dict) is dict:
                                for loop, indexKey in enumerate(json_dict):
                                    if loop == indexNo:
                                        if self.item == 'key':
                                            resolved = indexKey
                                        else:
                                            resolved = json_dict[indexKey]
                                        break
                            else:
                                resolved = json_dict[indexNo]
                                if resolved is None:
                                    resolved = 'null'
                    else:
                        resolved = json_dict
                else:
                    if self.function == 'len':
                        resolved = "1"
                    else:
                        if self.index != "":
                            if indexNo == 0 or indexNo == -1:
                                resolved = json_dict
                            else:
                                resolved = ''
                        else:
                            if json_dict is None:
                                resolved = 'null'
                            else:
                                if type(json_dict) is str and len(json_dict) == 0:
                                    resolved = '""'
                                else:
                                    resolved = json_dict

                if type(resolved) is dict or type(resolved) is list:
                    resolved = json.dumps(resolved, ensure_ascii=False)
                elif type(resolved) is int or type(resolved) is float or type(resolved) is complex:
                    resolved = str(resolved)
                elif type(resolved) is bool:
                    resolved = str(resolved).lower()
            except Exception as e:
                YLogger.exception(self, "JSON failed to load JSON", e)

        if resolved == '':
            YLogger.debug(client_context, "TemplateJsonNode get failed %s index=[%s]", self.keys, self.index)
            resolved = TemplateGetNode.get_default_value(client_context)

        YLogger.debug(client_context, "JSON get %s resolved to [%s]", self.keys, resolved)
        return resolved

    def resolve_to_string(self, client_context):
        resolved = self.resolve_children(client_context)
        resolved = resolved.strip()
        conversation = client_context.bot.get_conversation(client_context)
        name = self._name.resolve(client_context)

        try:
            key = self._key.resolve(client_context)
            name = name + "." + key
        except Exception:
            pass

        try:
            self.function = self._function.resolve(client_context)
            if self.function not in ['len', 'delete', 'insert']:
                YLogger.debug(self, "JSON unknown function type [%s]", self.function)
                return ''
        except Exception:
            self.function = 'None'
        try:
            self.index = self._index.resolve(client_context)
            try:
                int(self.index)
            except ValueError:
                YLogger.debug("JSON index not numeric [%s]", self.index)
        except Exception:
            self.index = ""
        try:
            self.item = self._item.resolve(client_context)
        except Exception:
            self.item = "value"

        if self.function == 'insert' and self.index == "":
            YLogger.debug(self, "JSON insert-function needs index parameter")
            return ''

        if self.function == 'delete':
            resolved = ''

        try:
            self.keys = name.split('.')
            if '' in self.keys:
                YLogger.debug(self, "JSON invalid key")
                return ''
            if self._type == "var":
                if conversation.has_current_question():
                    value = conversation.current_question().property(self.keys[0])
            elif self._type == "data":
                value = conversation.data_property(self.keys[0])
            elif self._type == "name":
                value = conversation.property(self.keys[0])
            else:
                YLogger.debug(self, "JSON invalid variables type")
                return ''
            json_dict = json.loads(value)
        except Exception:
            if len(resolved) == 0:
                json_dict = None
            else:
                json_dict = {}

        if len(resolved) > 0:
            resolved = self._json_set_elements(client_context, json_dict, resolved)
        else:
            if self.function == 'delete':
                resolved = self._json_delete_elements(client_context, json_dict)
            else:
                resolved = self._json_get_elements(client_context, json_dict)

        return resolved

    def to_string(self):
        return "[JSON]"

    def to_xml(self, client_context):
        xml = "<json "
        xml += self._type + '="'
        xml += self._name.to_xml(client_context)
        xml += '"'
        if self._is_convert is False:
            xml += ' type="string"'
        xml += ">"
        if self._function is not None:
            xml += "<function>"
            xml += self._function.to_xml(client_context)
            xml += "</function>"
        if self._index is not None:
            xml += "<index>"
            xml += self._index.to_xml(client_context)
            xml += "</index>"
        if self._item is not None:
            xml += "<item>"
            xml += self._item.to_xml(client_context)
            xml += "</item>"
        if self._key is not None:
            xml += "<key>"
            xml += self._key.to_xml(client_context)
            xml += "</key>"
        xml += self.children_to_xml(client_context)
        xml += "</json>"
        return xml

    # ######################################################################################################
    # JSON_PREDICATE_EXPRESSION ::==
    # <json name="JSONName">TEMPLATE_EXPRESSION</json> |

    def parse_expression(self, graph, expression):
        mode_count = 0
        text_content = ''

        if 'name' in expression.attrib:
            mode_count += 1
            self._name = self.parse_attrib_value_as_word_node(graph, expression, 'name')
            self._type = 'name'

        if 'data' in expression.attrib:
            mode_count += 1
            self._name = self.parse_attrib_value_as_word_node(graph, expression, 'data')
            self._type = 'data'

        if 'var' in expression.attrib:
            mode_count += 1
            self._name = self.parse_attrib_value_as_word_node(graph, expression, 'var')
            self._type = 'var'

        if 'function' in expression.attrib:
            self._function = self.parse_attrib_value_as_word_node(graph, expression, 'function')
            function = expression.attrib['function']
            if function not in ['len', 'delete', 'insert']:
                raise ParserException(("Unknown function type [%s]" % function), xml_element=expression, nodename='json')

        if 'item' in expression.attrib:
            self._item = self.parse_attrib_value_as_word_node(graph, expression, 'item')

        if 'key' in expression.attrib:
            self._key = self.parse_attrib_value_as_word_node(graph, expression, 'key')

        if 'index' in expression.attrib:
            self._index = self.parse_attrib_value_as_word_node(graph, expression, 'index')
            indexNo = expression.attrib['index']
            try:
                int(indexNo)
            except ValueError:
                raise ParserException(("Index value is not numeric [%s]" % indexNo), xml_element=expression, nodename='json')

        if 'type' in expression.attrib:
            value_type = expression.attrib['type']
            if value_type == 'string':
                self._is_convert = False

        expression_text = self.get_text_from_element(expression)
        self.parse_text(graph, expression_text)
        if expression_text is not None:
            text_content += expression_text

        for child in expression:
            tagName = TextUtils.tag_from_text(child.tag)

            if tagName == 'function':
                self._function = self.parse_children_as_word_node(graph, child)
            elif tagName == 'index':
                self._index = self.parse_children_as_word_node(graph, child)
            elif tagName == 'item':
                self._item = self.parse_children_as_word_node(graph, child)
            elif tagName == 'key':
                self._key = self.parse_children_as_word_node(graph, child)
            else:
                self._set_child_mark(graph, self.JSON_CHILD_IN)
                graph.parse_tag_expression(child, self)
                self._set_child_mark(graph, self.JSON_CHILD_OUT)
                text_content += self.JSON_CHILD_MARK

            expression_text = self.get_tail_from_element(child)
            self.parse_text(graph, expression_text)
            if expression_text is not None:
                text_content += expression_text

        if mode_count == 0:
            raise ParserException("Missing variable type", xml_element=expression, nodename='json')
        elif mode_count > 1:
            raise ParserException("Node has multiple variable type", xml_element=expression, nodename='json')

        if len(text_content) > 0:
            if self._format_check(text_content) is False:
                raise ParserException("Invalid contents format", xml_element=expression, nodename='json')

    def _text_to_list(self, text):
        is_invalid = False
        words = []
        if text is None or text == '':
            return words, is_invalid

        is_single = True
        single_word = ''

        word = ''
        is_quote = False
        is_escape = False
        is_valid = True
        for char in text:
            if is_single is True:
                single_word += char

            if is_escape is True:
                is_escape = False
                word += char
            elif char == '"':
                if is_quote is False:
                    is_quote = is_valid = True
                else:
                    is_quote = is_valid = False
                word += char
            elif char == '\\' and is_valid is True:
                is_escape = True
                word += char
            elif is_quote is False and char == ',':
                words.append(word.strip())
                word = ''
                is_single = False
            else:
                if is_valid is True:
                    word += char
                else:
                    if char != ' ' and char != ',':
                        is_invalid = True

        if is_quote is False and len(word) > 0:
            words.append(word.strip())

        if is_single is True:
            words = [single_word]
        else:
            if len(words) > 1:
                if text[0] != '"' or text[-1] != '"':
                    is_invalid = True

        if is_invalid is True:
            words = [text]
        return words, is_invalid

    def _word_to_data(self, word, isSingle):
        if isSingle is True:
            if len(word) > 2:
                if word[0] == '"' and word[-1] == '"':
                    word = word[1:-1]
        else:
            if len(word) < 2:
                return None
            if word[0] != '"' or word[-1] != '"':
                return None
            word = word[1:]
            word = word[:-1]

        new_word = ''
        is_escape = False
        for char in word:
            if is_escape is True:
                is_escape = False
                new_word += char
            elif char == '\\':
                is_escape = True
            else:
                new_word += char

        return new_word

    def _set_child_mark(self, graph, shiftCode):
        word_class = graph.get_node_class_by_name('word')
        word_node = word_class(shiftCode)
        self.children.append(word_node)

    def _delete_child_mark(self, resolved, is_json=False):
        start_pos = 0
        sin_pos = resolved.find(self.JSON_CHILD_IN, start_pos)
        if sin_pos < 0:
            new_resolved = resolved
        else:
            if sin_pos == 0:
                new_resolved = ''
            else:
                new_resolved = resolved[start_pos: sin_pos]
            while sin_pos >= 0:
                sout_pos = resolved.find(self.JSON_CHILD_OUT, start_pos + 1)
                shift_text = resolved[sin_pos + 1: sout_pos]
                if is_json is False:
                    shift_text = shift_text.replace('"', '\\"')
                    # if "," in shift_text:
                    #    shift_text = '"' + shift_text + '"'
                new_resolved += shift_text
                start_pos = sout_pos + 1
                sin_pos = resolved.find(self.JSON_CHILD_IN, start_pos)
                if sin_pos > 0:
                    new_resolved += resolved[start_pos: sin_pos]
                else:
                    new_resolved += resolved[start_pos:]

        return new_resolved

    def _format_check(self, texts):
        texts = texts.strip()
        if len(texts) == 0:
            return True
        if texts[0] == '{':
            texts1 = texts.replace(self.JSON_CHILD_MARK, '""')
            texts2 = texts.replace(self.JSON_CHILD_MARK, '"key": "value"')
            try:
                json.loads(texts1)
                return True
            except Exception:
                pass
            try:
                json.loads(texts2)
            except Exception:
                return False
        else:
            texts = texts.replace(self.JSON_CHILD_MARK, 'x')
            words, is_invalid = self._text_to_list(texts)
            if len(words) == 0 or is_invalid is True:
                return True

        return True
