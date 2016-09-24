#!/usr/bin/python
#coding=utf-8
import unittest


def Count(s):
    countDict = {}
    countList = []
    #统计各字符的个数
    for _s_ in s:
       if _s_ in countDict:
           countDict[_s_] += 1
       else:
           countDict[_s_] = 1
     
    #找出频率前10的字符
    countList = countDict.values()
    #排序
    countList = list(set(countList))
    countList.sort()
    countList.reverse()
    #取出前10频率
    HighFreqCount = countList[:10]
    #找到前10频率的字符
    HighStr = []
    num = 0
    for num in HighFreqCount:
        for _c_ in countDict.keys():
             if countDict[_c_] == num and len(HighStr) < 10:
                  HighStr.append(_c_)
    return HighStr


class TestStrCount(unittest.TestCase):
    def testCount(self):
        s = "aaabbbbbbccfjakhfhwqlncvlav;oewfnllaksscj"
        HighStr = Count(s)
        HoghStrTest = ['a', 'b', 'c', 'l', 'f', 'h', 'k', 'j', 'n', 's']
        self.assertEqual(HighStr, HoghStrTest)


if __name__ == '__main__':
    unittest.main()
