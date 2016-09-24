import unittest
import sys
from wc_w import mainReadpipe, mainReadfile

class SimpleWordcount(unittest.TestCase):
    def testfile(self):
        count = mainReadfile("test.txt")
        self.assertEqual(count, 52)
    def testpipe(self):
        count = mainReadpipe()
        self.assertEqual(count, 52)

file_Test = SimpleWordcount("testfile")
file_Test.run()
pipe_test = SimpleWordcount("testpipe")
pipe_test.run()
