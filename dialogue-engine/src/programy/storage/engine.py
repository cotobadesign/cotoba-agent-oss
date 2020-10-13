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


class StorageEngine(object):

    def __init__(self, configuration):
        self._configuration = configuration

    @property
    def configuration(self):
        return self._configuration

    def user_store(self):
        raise NotImplementedError("Engine does not support user storage")

    def linked_account_store(self):
        raise NotImplementedError("Engine does not support linked account storage")

    def link_store(self):
        raise NotImplementedError("Engine does not support link storage")

    def category_store(self):
        raise NotImplementedError("Engine does not support category storage")

    def errors_store(self):
        raise NotImplementedError("Engine does not support errors storage")

    def duplicates_store(self):
        raise NotImplementedError("Engine does not support duplicates storage")

    def errors_collection_store(self):
        raise NotImplementedError("Engine does not support errors_collection storage")

    def learnf_store(self):
        raise NotImplementedError("Engine does not support learnf storage")

    def conversation_store(self):
        raise NotImplementedError("Engine does not support conversation storage")

    def logs_store(self):
        raise NotImplementedError("Engine does not support logs storage")

    def nlu_store(self):
        raise NotImplementedError("Engine does not support NLU storage")

    def bot_names_store(self):
        raise NotImplementedError("Engine does not support Bot Names storage")

    def rest_templates_store(self):
        raise NotImplementedError("Engine does not support REST_templates storage")

    def sets_store(self):
        raise NotImplementedError("Engine does not support sets storage")

    def maps_store(self):
        raise NotImplementedError("Engine does not support maps storage")

    def rdf_store(self):
        raise NotImplementedError("Engine does not support rdf storage")

    def denormal_store(self):
        raise NotImplementedError("Engine does not support denormal storage")

    def normal_store(self):
        raise NotImplementedError("Engine does not support normal storage")

    def gender_store(self):
        raise NotImplementedError("Engine does not support gender storage")

    def person_store(self):
        raise NotImplementedError("Engine does not support person storage")

    def person2_store(self):
        raise NotImplementedError("Engine does not support person2 storage")

    def regex_store(self):
        raise NotImplementedError("Engine does not support regex storage")

    def property_store(self):
        raise NotImplementedError("Engine does not support property storage")

    def property_json_store(self):
        raise NotImplementedError("Engine does not support property_json storage")

    def defaults_store(self):
        raise NotImplementedError("Engine does not support defaults storage")

    def spelling_store(self):
        raise NotImplementedError("Engine does not support spelling storage")

    def license_store(self):
        raise NotImplementedError("Engine does not support license storage")

    def pattern_nodes_store(self):
        raise NotImplementedError("Engine does not support pattern nodes storage")

    def template_nodes_store(self):
        raise NotImplementedError("Engine does not support template nodes storage")

    def binaries_store(self):
        raise NotImplementedError("Engine does not support binaries storage")

    def braintree_store(self):
        raise NotImplementedError("Engine does not support braintree storage")

    def preprocessors_store(self):
        raise NotImplementedError("Engine does not support preprocessor storage")

    def postprocessors_store(self):
        raise NotImplementedError("Engine does not support postprocessor storage")

    def usergroups_store(self):
        raise NotImplementedError("Engine does not support user groups storage")

    def triggers_store(self):
        raise NotImplementedError("Engine does not support trigger storage")

    def rdf_updates_store(self):
        raise NotImplementedError("Engine does not support rdf updates storage")
