#!/usr/bin/python
# coding=utf-8

import unittest
import pdb


def stringCount(str):
    # 存放结果的字典
    counters = {}

    # 遍历字符串如果在结果字典中，则统计次数 +1，否则，就设为初始值 1
    for item in list(str):
        if item in counters:
            counters[item] += 1
        else:
            counters[item] = 1

    return counters


class TestStringCount(unittest.TestCase):
    # 初始化工作
    def setUp(self):
        pass

    # 退出的清理工作
    def tearDown(self):
        pass

    # 测试实例
    def teststringcount(self):
        string = "aaaabbbbccccddddffffeeee"
        res = {'a': 4, 'b': 4, 'c': 4, 'd':4, 'f': 4, 'e': 4}
        self.assertEqual(stringCount(string), res)


if __name__ == "__main__":
    text = "sfdhsfksdhfidshfiwfhqiufjdnfkdsnkfsdiuvojf;qewkfepqwjelfndskfndsnfuadsknfkdasbnfudsakbnfkdasn"

    for i in stringCount(text).items():
        print "字符：{0}, 出现次数: {1}".format(i[0],stringCount(text)[i[0]])

    print "出现最多的字符: ", sorted([(counters, word) for word, counters in stringCount(text).items()], reverse=True)[0][1]
    print '-' * 20

    unittest.main()