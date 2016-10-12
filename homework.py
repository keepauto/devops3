#!/usr/bin/env python
#！_*_encoding:utf-8_*_
import  re

#匹配文件中的关键字

def find_line_by_key(keyword):
    def grep_file(filepath):
        with open(filepath, 'r') as f:
            for line in f.readlines():
                strLine = line.strip()         #去除空格
                m = re.search(keyword,strLine)
                if m:
                    print m.string
    return grep_file

#filt=find_line_by_key('fpay')
#filt('./passwd')


#保留闭包内函数执行后的值，做个小加法
def additive():
    DEFULTZERO = [0,]
    def myadd(number1):
        DEFULTZERO[0] = number1 + DEFULTZERO[0]
        #count[0] = mycount
        return DEFULTZERO
    return myadd

#单元测试,和断点测试
import unittest,pdb
class testAdditive(unittest.TestCase):
    def testAdd(self):
        addNmber=10
        countNumber1=10
        countNumber2=20
        functionAdd=additive()
        self.assertEqual(functionAdd(addNmber)[0],countNumber1) #第一次加法为10
        self.assertEqual(functionAdd(addNmber)[0],countNumber2) #第二次加法为20
        functionAdd=additive() #初始化后重新加法
        self.assertEqual(functionAdd(addNmber)[0],countNumber1) #初始化后 再执行为10
if __name__ == "__main__":
    unittest.main()







