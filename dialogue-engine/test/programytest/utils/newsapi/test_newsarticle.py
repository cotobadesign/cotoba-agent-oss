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
import json

from programy.utils.newsapi.newsapi import NewsArticle


class NewsArticleTests(unittest.TestCase):

    def test_init(self):
        article = NewsArticle()
        self.assertIsNotNone(article)
        self.assertIsNone(article.title)
        self.assertIsNone(article.description)
        self.assertIsNone(article.published_at)
        self.assertIsNone(article.author)
        self.assertIsNone(article.url)
        self.assertIsNone(article.url_to_image)

    def test_missing_values(self):
        article = NewsArticle()
        data = json.loads("""
        {
            "title": "title",
            "description": "description",
            "publishedAt": "published_at",
            "author": "author",
            "url": "url",
            "urlToImage": "url_to_image"
        }
        """)

        self.assertIsNone(article._get_json_attribute(data, "other_value"))
        self.assertEqual("Default", article._get_json_attribute(data, "other_value", "Default"))

    def test_parse_json(self):
        article = NewsArticle()
        data = json.loads("""
        {
            "title": "title",
            "description": "description",
            "publishedAt": "published_at",
            "author": "author",
            "url": "url",
            "urlToImage": "url_to_image"
        }
        """)
        article.parse_json(data)
        self.assertEqual("title", article.title)
        self.assertEqual("description", article.description)
        self.assertEqual("published_at", article.published_at)
        self.assertEqual("author", article.author)
        self.assertEqual("url", article.url)
        self.assertEqual("url_to_image", article.url_to_image)

        json_data = article.to_json()
        self.assertIsNotNone(json_data)
        self.assertEqual({
            "title": "title",
            "description": "description",
            "publishedAt": "published_at",
            "author": "author",
            "url": "url",
            "urlToImage": "url_to_image"
        }, json_data)
