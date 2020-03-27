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
import os
import shutil

from programy.utils.files.filewriter import ConversationFileWriter, ContentFileWriter, ErrorsFileWriter, DuplicatesFileWriter


class MockFileConfiguration(object):

    def __init__(self, dirs=None, filename=None, format=None, encoding='utf_8', delete_on_start=False):
        self._filename = dirs + os.sep + filename
        self._file_format = format
        self._encoding = encoding
        self._delete_on_start = delete_on_start

    @property
    def filename(self):
        return self._filename

    @property
    def file_format(self):
        return self._file_format

    @property
    def encoding(self):
        return self._encoding

    @property
    def delete_on_start(self):
        return self._delete_on_start


class FileWriterTests(unittest.TestCase):

    def test_conversation_file_write(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "conversation.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=False)
        fileWriter = ConversationFileWriter(configuration)
        fileWriter.write_header()
        fileWriter.log_question_and_answer("client-id", "question", "answer")

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_conversation_file_delete_on_start(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "conversation_init.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=True)
        fileWriter = ConversationFileWriter(configuration)

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=False)
        fileWriter = ConversationFileWriter(configuration)
        fileWriter.write_header()
        fileWriter.log_question_and_answer("client-id", "question", "answer")

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=True)
        fileWriter = ConversationFileWriter(configuration)

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_content_file_write(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "contents.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=False)
        fileWriter = ContentFileWriter(configuration, "txt")
        fileWriter.save_entry("content", "filename")
        self.assertEqual("content", fileWriter.entries[0][1])
        self.assertEqual("filename", fileWriter.entries[0][2])
        fileWriter.save_content()
        fileWriter.print_content()
        fileWriter.display_debug_info()

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_content_file_write_with_lineinfo(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "contents_line.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=False)
        fileWriter = ContentFileWriter(configuration, "txt")
        fileWriter.save_entry("content", "filename", "startline", "endline")
        fileWriter.save_content()

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_content_file_write_csv(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "contents_csv.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="csv", delete_on_start=False)
        fileWriter = ContentFileWriter(configuration, "csv")
        fileWriter.save_entry("content", "filename", "startline", "endline")
        fileWriter.save_content()

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_content_file_write_invalid(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "contents.xml"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="xml", delete_on_start=False)
        with self.assertRaises(Exception):
            ContentFileWriter(configuration, "xml")

        target = tmpdir + os.sep + tmpfile
        self.assertFalse(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_errors_file_write(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "errors.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=False)
        fileWriter = ErrorsFileWriter(configuration)
        fileWriter.write_header()
        fileWriter.save_entry("error-info", "filename", "10", "11")
        fileWriter.save_content()

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

    def test_duplicates_file_write(self):
        tmpdir = os.path.dirname(__file__) + os.sep + "tmp"
        tmpfile = "duplicates.txt"

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))

        configuration = MockFileConfiguration(dirs=tmpdir, filename=tmpfile, format="txt", delete_on_start=False)
        fileWriter = DuplicatesFileWriter(configuration)
        fileWriter.write_header()
        fileWriter.save_entry("duplicate-info", "filename", "10", "11")
        fileWriter.save_content()

        target = tmpdir + os.sep + tmpfile
        self.assertTrue(os.path.exists(target))

        if os.path.exists(tmpdir):
            shutil.rmtree(tmpdir)
        self.assertFalse(os.path.exists(tmpdir))
