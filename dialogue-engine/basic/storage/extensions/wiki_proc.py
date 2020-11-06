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
import requests


class WikipediaProc:

    def call(self, params):

        params["format"] = "json"
        params["action"] = "query"

        headers = {
            "User-Agent": "python-requests"
        }

        response = requests.get("http://ja.wikipedia.org/w/api.php", params=params, headers=headers)
        return response.json()

    def search(self, query):

        params = {
            "list": "search",
            "srprop": "",
            "srlimit": 5,
            "limit": 5,
            "srsearch": query
        }

        results = self.call(params)

        if "error" in results:
            return None
        search_results = (d["title"] for d in results["query"]["search"])
        return list(search_results)

    def page(self, title):
        params = {
            "prop": "info|pageprops",
            "inprop": "url",
            "ppprop": "disambiguation",
            "redirects": "",
            "titles": title
        }
        result = self.call(params)

        pageid = list(result["query"]["pages"].keys())[0]
        return pageid

    def summary(self, title, pageid):
        params = {
            "prop": "extracts",
            "exintro": "",
            "explaintext": "",
            "titles": title
        }

        result = self.call(params)

        summary = result["query"]["pages"][pageid]["extract"]
        return summary


if __name__ == "__main__":

    proc = WikipediaProc()

    while True:

        user_input = input("検索したい単語を入力してください。：")
        if not user_input:
            break

        try:
            print("----------------")
            search_result = proc.search(user_input)
            print("search result:", search_result)

            if search_result is not None:
                pageid = proc.page(search_result[0])
                print("pageid:", pageid)

                contents = proc.summary(search_result[0], pageid)
                result = contents.split("。")[0] + "。"
            else:
                result = "わかりませんでした"
            print("summary:", result)
            print("----------------")

        except Exception:
            print("結果取得に失敗しました")
            pass
