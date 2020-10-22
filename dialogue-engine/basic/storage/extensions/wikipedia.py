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
from programy.utils.logging.ylogger import YLogger
from programy.extensions.base import Extension

from wiki_proc import WikipediaProc


class WikipediaExtension(Extension):

    def execute(self, context, data):
        wiki = WikipediaProc()

        try:
            search_result = wiki.search(data)
            YLogger.debug(context, "Wikipedia search result: %s", search_result)

            if search_result is not None:
                pageid = wiki.page(search_result[0])
                YLogger.debug(context, "Wikipedia pageid: %d", pageid)

                contents = wiki.summary(search_result[0], pageid)
                result = contents.split("。")[0] + "。"
            else:
                result = None

            YLogger.debug(context, "Wikipedia summary: %s", result)
            return result

        except Exception:
            return None
