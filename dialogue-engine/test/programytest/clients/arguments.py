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
class MockArguments(object):

    def __init__(self, bot_root=".",
                 logging=None,
                 config=None,
                 cformat="yaml",
                 noloop=False,
                 substitutions='subs.txt',
                 stdoutlog=False,
                 stderrlog=False):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop
        self.substitutions = substitutions
        self.stdoutlog = stdoutlog
        self.stderrlog = stderrlog


class MockArgumentParser(object):

    def __init__(self, bot_root=".", logging=None, config=None, cformat="yaml", noloop=False, substitutions='subs.txt', stdoutlog=False, stderrlog=False):
        self.bot_root = bot_root
        self.logging = logging
        self.config = config
        self.cformat = cformat
        self.noloop = noloop
        self.substitutions = substitutions
        self.stdoutlog = stdoutlog
        self.stderrlog = stderrlog

    def add_argument(self, argument, dest=None, action=None, help=None, default=False):
        pass

    def parse_args(self):
        return MockArguments(bot_root=self.bot_root,
                             logging=self.logging,
                             config=self.config,
                             cformat=self.cformat,
                             noloop=self.noloop,
                             substitutions=self.substitutions,
                             stdoutlog=False,
                             stderrlog=False)
