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
from programy.extensions.base import Extension

from wiki_proc import WikipediaProc


class WikipediaExtension(Extension):

    def execute(self, context, data):
        conversation = context.bot.get_conversation(context)
        wiki = WikipediaProc()
        try:
            search_result = wiki.search(data)
            logs_msg = {"debug": "Wikipedia search result:" + search_result[0]}
            conversation.append_log(logs_msg)

            if search_result is not None:
                pageid = wiki.page(search_result[0])

                logs_msg = {"debug": "Wikipedia pageid:" + str(pageid)}
                conversation.append_log(logs_msg)

                contents = wiki.summary(search_result[0], pageid)
                result = contents.split("。")[0] + "。"
            else:
                result = ""

            logs_msg = {"debug": "Wikipedia summary:" + result}
            conversation.append_log(logs_msg)

            return result

        except Exception:
            logs_msg = {"error": "Wikipedia get error"}
            conversation.append_log(logs_msg)
            return None
