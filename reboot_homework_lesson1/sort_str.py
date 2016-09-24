#!/usr/bin/env pyhon
#coding=utf-8
import os
import sys
import unittest
import time
os.system('stty erase ^H')
str_input = raw_input("please input your str: ").decode(sys.stdin.encoding)

def sort_str(str_in):
    letterCounts = {}
    for letter in str_in:
        letterCounts[letter] = letterCounts.get(letter,0)+1
        sorted_str = sorted(letterCounts.items(), key=lambda x:x[1],reverse=True)
    for i,j in sorted_str:
        print "%s has appers %s times" %(i,j)
	
    return sorted_str

class Testsort_str(unittest.TestCase):
    def test(self):
        input_str = u"付付付  天天  时时是是时   ak47awk47@@***&&&"
        result_lst = [(u' ', 7), (u'&', 3), (u'*', 3), (u'\u65f6', 3), (u'\u4ed8', 3), (u'a', 2), (u'@', 2), (u'\u5929', 2), (u'k', 2), (u'\u662f', 2), (u'4', 2), (u'7', 2), (u'w', 1)]
        self.assertEqual(sort_str(input_str),result_lst)

if __name__ == "__main__":
    sort_str(str_input)
    print "i will test after 3s:"
    print "-------------------------------"
    time.sleep(3)
    unittest.main()
