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
Copyright (c) 2016-2019 Keith Sterling http://www.keithsterling.com

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
import json

from programy.parser.template.nodes.base import TemplateNode
from programy.parser.template.nodes.get import TemplateGetNode
from programy.parser.template.nodes.word import TemplateWordNode
from programy.parser.exceptions import ParserException
from programy.utils.text.text import TextUtils
from programy.utils.language.japanese import JapaneseLanguage


class QueryBase(object):

    def __init__(self, subj, pred, obj):
        self._subj = subj
        self._pred = pred
        self._obj = obj

    @property
    def subj(self):
        return self._subj

    @property
    def pred(self):
        return self._pred

    @property
    def obj(self):
        return self._obj

    def to_xml(self, client_context):
        xml = "<subj>%s</subj>" % self._subj
        xml += "<pred>%s</pred>" % self._pred
        xml += "<obj>%s</obj>" % self._obj
        return xml

    def execute(self, client_context):
        return []

    def get_rdf(self, client_context, vars):
        subj = None
        pred = None
        obj = None
        is_error = False

        if self.subj is not None:
            subj = self.subj.resolve(client_context)
            if subj.startswith("?") is True:
                if vars is None or subj not in vars:
                    YLogger.debug(self, "selecet : Subject variable [%s] defined, but not in vars!", subj)
                    is_error = True
                    return subj, pred, obj, is_error
            elif subj == '':
                subj = None
        if self.pred is not None:
            pred = self.pred.resolve(client_context)
            if pred.startswith("?") is True:
                if vars is None or pred not in vars:
                    YLogger.debug(self, "selecet : Predicate variable [%s] defined, but not in vars!", pred)
                    is_error = True
                    return subj, pred, obj, is_error
            elif pred == '':
                pred = None
        if self.obj is not None:
            obj = self.obj.resolve(client_context)
            if obj.startswith("?") is True:
                if vars is None or obj not in vars:
                    YLogger.debug(self, "selecet : Object variable [%s] defined, but not in vars!", obj)
                    is_error = True
                    return subj, pred, obj, is_error
            elif obj == '':
                obj = None

        return subj, pred, obj, is_error


class Query(QueryBase):

    def __init__(self, subj, pred, obj):
        QueryBase.__init__(self, subj, pred, obj)

    def to_xml(self, client_context):
        xml = "<q>"
        xml += super(Query, self).to_xml(client_context)
        xml += "</q>"
        return xml

    def execute(self, client_context, vars=None):
        subj, pred, obj, is_error = self.get_rdf(client_context, vars)
        if is_error is True:
            return []

        if vars is None:
            tuples = client_context.brain.rdf.matched_as_tuples(subj, pred, obj)
            results = []
            for atuple in tuples:
                results.append([["subj", atuple[0]], ["pred", atuple[1]], ["obj", atuple[2]]])
            return results
        else:
            tuples = client_context.brain.rdf.match_to_vars(subj, pred, obj)
            return tuples


class NotQuery(QueryBase):

    def __init__(self, subj, pred, obj):
        QueryBase.__init__(self, subj, pred, obj)

    def get_xml_type(self):
        return "notq"

    def to_xml(self, client_context):
        xml = "<notq>"
        xml += super(NotQuery, self).to_xml(client_context)
        xml += "</notq>"
        return xml

    def execute(self, client_context, vars=None):
        subj, pred, obj, is_error = self.get_rdf(client_context, vars)
        if is_error is True:
            return []

        if vars is None:
            tuples = client_context.brain.rdf.not_matched_as_tuples(subj, pred, obj)
            results = []
            for atuple in tuples:
                results.append([["subj", atuple[0]], ["pred", atuple[1]], ["obj", atuple[2]]])
            return results
        else:
            tuples = client_context.brain.rdf.not_match_to_vars(subj, pred, obj)
            return tuples


class TemplateSelectNode(TemplateNode):

    def __init__(self, queries=None, vars=None):
        TemplateNode.__init__(self)
        if queries is None:
            self._queries = []
        else:
            self._queries = queries[:]
        if vars is None:
            self._vars = []
        else:
            self._vars = vars[:]

    @property
    def queries(self):
        return self._queries

    @property
    def vars(self):
        return self._vars

    def encode_results(self, client_context, results):
        # At some point put a config item here that allows us to switch between
        # XML, JSON, Yaml, and Picke
        return json.dumps(results, ensure_ascii=False)

    def resolve_to_string(self, client_context):

        resolved = ""
        if len(self.vars) == 0:
            vars = None
        else:
            vars = self.vars

        if self._queries:
            results = []

            for query in self._queries:
                query_results = query.execute(client_context, vars)
                results.append(query_results)

            if vars is None:
                vars = ['subj', 'pred', 'obj']
            results = client_context.brain.rdf.unify(vars, results)

            if len(results) > 0:
                resolved = self.encode_results(client_context, results)
            else:
                resolved = TemplateGetNode.get_default_value(client_context)

        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[SELECT]"

    def to_xml(self, client_context):
        xml = "<select>"
        if self._vars:
            xml += "<vars>"
            xml += " ".join(self._vars)
            xml += "</vars>"
        if self._queries:
            for query in self._queries:
                xml += query.to_xml(client_context)
        xml += "</select>"
        return xml

    #######################################################################################################
    # SELECT_EXPRESSION ::== <person>TEMPLATE_EXPRESSION</person>

    def parse_vars(self, variables):
        if variables is None:
            return
        var_splits = variables.split(" ")
        for var_name in var_splits:
            var = JapaneseLanguage.zenhan_normalize(var_name)
            if var.startswith('?') is True:
                if var not in self.vars:
                    self.vars.append(var)
            else:
                YLogger.warning(self, "Vars name [%s] is not start with '?' in select", var_name)

    def parse_query(self, graph, query_name, query, expression):
        subj = pred = obj = None
        query_vars = []

        for child in query:
            tag_name = TextUtils.tag_from_text(child.tag)

            if tag_name == 'subj':
                subj = self.parse_children_as_word_node(graph, child)
                if len(subj.children) == 0:
                    subj = None
                elif len(subj.children) == 1 and type(subj.children[0]) is TemplateWordNode:
                    var_name = subj.children[0].word
                    var_name = JapaneseLanguage.zenhan_normalize(var_name)
                    if var_name.startswith("?"):
                        if var_name not in query_vars:
                            query_vars.append(var_name)
                        else:
                            raise ParserException(("Same variable_name[%s] used in query" % var_name), xml_element=expression, nodename='select')
            elif tag_name == 'pred':
                pred = self.parse_children_as_word_node(graph, child)
                if len(pred.children) == 0:
                    pred = None
                elif len(pred.children) == 1 and type(pred.children[0]) is TemplateWordNode:
                    var_name = pred.children[0].word
                    var_name = JapaneseLanguage.zenhan_normalize(var_name)
                    if var_name.startswith("?"):
                        if var_name not in query_vars:
                            query_vars.append(var_name)
                        else:
                            raise ParserException(("Same variable_name[%s] used in query" % var_name), xml_element=expression, nodename='select')
            elif tag_name == 'obj':
                obj = self.parse_children_as_word_node(graph, child)
                if len(obj.children) == 0:
                    obj = None
                elif len(obj.children) == 1 and type(obj.children[0]) is TemplateWordNode:
                    var_name = obj.children[0].word
                    var_name = JapaneseLanguage.zenhan_normalize(var_name)
                    if var_name.startswith("?"):
                        if var_name not in query_vars:
                            query_vars.append(var_name)
                        else:
                            raise ParserException(("Same variable_name [%s] used in query" % var_name), xml_element=expression, nodename='select')
            else:
                YLogger.warning(self, "Unknown tag name [%s] in select query", tag_name)

        if subj is None and pred is None and obj is None:
            raise ParserException("Subject/Predicate/Object element missing", xml_element=expression, nodename='select')

        if len(query_vars) > 0:
            for q_var in query_vars:
                if q_var not in self.vars:
                    self.vars.append(q_var)

        if query_name == "q":
            self._queries.append(Query(subj, pred, obj))
        else:
            self._queries.append(NotQuery(subj, pred, obj))

    def parse_expression(self, graph, expression):
        is_valid = False

        variables = expression.findall('./vars')
        if variables:
            if len(variables) > 1:
                YLogger.warning(self, "Multiple <vars> found in select tag, using first")
            self.parse_vars(variables[0].text)

        queries = expression.findall('./*')
        for query in queries:
            tag_name = TextUtils.tag_from_text(query.tag)
            if tag_name == 'q' or tag_name == 'notq':
                self.parse_query(graph, tag_name, query, expression)
                is_valid = True

        if is_valid is False:
            raise ParserException("Tags <q> or <notq> not found", xml_element=expression, nodename='select')

        if self.children:
            raise ParserException("Node Should not contain child text", xml_element=expression, nodename='select')
