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
import datetime
import iso8601
import pytz

from programy.parser.exceptions import ParserException
from programy.parser.template.nodes.attrib import TemplateAttribNode


class TemplateDateNode(TemplateAttribNode):

    def __init__(self, date_format=None):
        TemplateAttribNode.__init__(self)
        if date_format is None:
            self._format = "%c"
        else:
            self._format = date_format

    def resolve_to_string(self, client_context):
        time_now = None
        if hasattr(client_context, 'userInfo') is True:
            user_time = client_context.userInfo.get('__USER_TIME__')
            if user_time != 'None':
                try:
                    time_now = iso8601.parse_date(user_time)
                except Exception:
                    pass

        if time_now is None:
            time_now = datetime.datetime.now()

        if hasattr(client_context, 'userInfo') is True:
            user_locale = client_context.userInfo.get('__USER_LOCALE__')
            if user_locale != 'None':
                try:
                    locale_text = client_context.userInfo.get('__USER_LOCALE__')
                    locale_params = locale_text.split('-')
                    if len(locale_params) >= 2:
                        timezone = self._get_timezone(locale_params[1])
                        if timezone is not None:
                            time_now = time_now.astimezone(timezone)
                except Exception:
                    pass

        resolved = time_now.strftime(self._format)
        YLogger.debug(client_context, "[%s] resolved to [%s]", self.to_string(), resolved)
        return resolved

    def to_string(self):
        return "[DATE format=%s]" % (self._format)

    def set_attrib(self, attrib_name, attrib_value):
        if attrib_name != 'format':
            raise ParserException("Invalid attribute name %s" % attrib_name, nodename='date')
        self._format = attrib_value

    def to_xml(self, client_context):
        xml = '<date format="%s" >' % self._format
        xml += self.children_to_xml(client_context)
        xml += "</date>"
        return xml

    def _get_timezone(self, country):
        timezone = None
        try:
            country = country.lower()
            timelist = pytz.country_timezones[country]
            if len(timelist) > 0:
                timezone = pytz.timezone(timelist[0])
        except Exception:
            pass
        return timezone

    #######################################################################################################
    # DATE_ATTRIBUTES ::== (format="LISP_DATE_FORMAT") | (jformat="JAVA DATE FORMAT")
    # DATE_ATTRIBUTE_TAG ::== <format>TEMPLATE_EXPRESSION</format> | <jformat>TEMPLATE_EXPRESSION</jformat>
    # DATE_EXPRESSION ::== <date( DATE_ATTRIBUTES)*/> | <date>(DATE_ATTRIBUTE_TAG)</date>
    # Pandorabots supports three extension attributes to the date element in templates:
    #     	locale
    #       format
    #       timezone

    def parse_expression(self, graph, expression):
        self._parse_node_with_attrib(graph, expression, "format", "%c")
