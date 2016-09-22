#!/usr/bin/python
# coding=utf-8

import unittest


def sum(x, y):
    return x + y

def sub(x, y):
    return x - y


class testmytest(unittest.TestCase):

    # 初始化工作
    def setUp(self):
        pass

    # 退出的清理工作
    def tearDown(self):
        pass

    # 具体的测试用例，一定要以 test 开头
    def testsum(self):
        self.assertEqual(sum(1, 2), 3, 'test sum faild')

    # 另一个具体的测试用例
    def testsub(self):
        self.assertEqual(sub(1, 2), -1, 'test sub faild')

# 测试入口
if __name__ == '__main__':
    unittest.main()
