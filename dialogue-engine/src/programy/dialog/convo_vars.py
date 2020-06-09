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

import copy


class ConversationVariables(object):

    def __init__(self, conversation):
        self._init_names = {}
        self._init_datas = {}
        self._init_vars = {}

        if conversation is not None:
            self._init_names = copy.copy(conversation.properties)
            self._init_datas = copy.copy(conversation.data_properties)
            question = conversation.current_question()
            if question is not None:
                self._init_vars = copy.copy(question._properties)

    def different_variables(self, conversation):
        before_variables = {}
        after_variables = {}
        if conversation is None:
            return before_variables, after_variables

        diff_names = self._get_diff_list(conversation.properties, self._init_names)
        before_names, after_names = self._make_variables(diff_names,
                                                         self._init_names, conversation.properties)
        if len(after_names) > 0:
            before_variables["name_properties"] = before_names
            after_variables["name_properties"] = after_names

        diff_datas = self._get_diff_list(conversation.data_properties, self._init_datas)
        before_datas, after_datas = self._make_variables(diff_datas,
                                                         self._init_datas, conversation.data_properties)
        if len(after_datas) > 0:
            before_variables["data_properties"] = before_datas
            after_variables["data_properties"] = after_datas

        question = conversation.current_question()
        if question is not None:
            diff_vars = self._get_diff_list(question._properties, self._init_vars)
            before_vars, after_vars = self._make_variables(diff_vars,
                                                           self._init_vars, question._properties)
            if len(after_vars) > 0:
                before_variables["var_properties"] = before_vars
                after_variables["var_properties"] = after_vars

        return before_variables, after_variables

    def _get_diff_list(self, dict1, dict2):
        diff_1 = dict(dict1.items() - dict2.items())
        diff_2 = dict(dict2.items() - dict1.items())
        diff_list = dict(diff_1.items() | diff_2.items())

        return diff_list

    def _make_variables(self, diff, before, after):
        before_vars = {}
        after_vars = {}

        for key in diff.keys():
            if key in before:
                before_vars[key] = before[key]
            else:
                before_vars[key] = None
            if key in after:
                after_vars[key] = after[key]
            else:
                after_vars[key] = None

        return before_vars, after_vars
