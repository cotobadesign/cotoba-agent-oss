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
from programy.utils.files.filefinder import FileFinder


class TestFileFinder(FileFinder):

    def __init__(self):
        FileFinder.__init__(self)
        self.files = []

    def load_file_contents(self, id, filename, userid="*"):
        self.files.append(filename)


class FileFinderTests(unittest.TestCase):

    def test_find_files_no_subdir(self):
        file_finder = TestFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__) + os.sep + "test_files", subdir=False, extension=".txt")
        self.assertEqual(len(files), 3)
        self.assertEqual("file1.txt", files[0][0])
        self.assertEqual("file2.txt", files[1][0])
        self.assertEqual("file3.txt", files[2][0])

    def test_find_files_subdir(self):
        file_finder = TestFileFinder()
        files = file_finder.find_files(os.path.dirname(__file__) + os.sep + "test_files", subdir=True, extension=".txt")
        self.assertEqual(len(files), 4)
        self.assertEqual("file1.txt", files[0][0])
        self.assertEqual("file2.txt", files[1][0])
        self.assertEqual("file3.txt", files[2][0])
        self.assertEqual("file4.txt", files[3][0])

    def test_load_dir_contents_no_subdir(self):
        file_finder = TestFileFinder()
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__) + os.sep + "test_files", subdir=False, extension=".txt")

        self.assertEqual(len(file_finder.files), 3)

        self.assertTrue("FILE1"in collection)
        self.assertTrue("FILE2"in collection)
        self.assertTrue("FILE3"in collection)

        self.assertTrue("FILE1"in file_maps)
        self.assertTrue("FILE2"in file_maps)
        self.assertTrue("FILE3"in file_maps)

    def test_load_dir_contents_subdir(self):
        file_finder = TestFileFinder()
        collection, file_maps = file_finder.load_dir_contents(os.path.dirname(__file__) + os.sep + "test_files", subdir=True, extension=".txt")

        self.assertEqual(len(file_finder.files), 4)

        self.assertTrue("FILE1"in collection)
        self.assertTrue("FILE2"in collection)
        self.assertTrue("FILE3"in collection)
        self.assertTrue("FILE4"in collection)

        self.assertTrue("FILE1"in file_maps)
        self.assertTrue("FILE2"in file_maps)
        self.assertTrue("FILE3"in file_maps)
        self.assertTrue("FILE4"in collection)
