#!/usr/bin/env python
#��_*_encoding:utf-8_*_
import  re

#ƥ���ļ��еĹؼ���

def find_line_by_key(keyword):
    def grep_file(filepath):
        with open(filepath, 'r') as f:
            for line in f.readlines():
                strLine = line.strip()         #ȥ���ո�
                m = re.search(keyword,strLine)
                if m:
                    print m.string
    return grep_file

#filt=find_line_by_key('fpay')
#filt('./passwd')


#�����հ��ں���ִ�к��ֵ������С�ӷ�
def additive():
    DEFULTZERO = [0,]
    def myadd(number1):
        DEFULTZERO[0] = number1 + DEFULTZERO[0]
        #count[0] = mycount
        return DEFULTZERO
    return myadd

#��Ԫ����,�Ͷϵ����
import unittest,pdb
class testAdditive(unittest.TestCase):
    def testAdd(self):
        addNmber=10
        countNumber1=10
        countNumber2=20
        functionAdd=additive()
        self.assertEqual(functionAdd(addNmber)[0],countNumber1) #��һ�μӷ�Ϊ10
        self.assertEqual(functionAdd(addNmber)[0],countNumber2) #�ڶ��μӷ�Ϊ20
        functionAdd=additive() #��ʼ�������¼ӷ�
        self.assertEqual(functionAdd(addNmber)[0],countNumber1) #��ʼ���� ��ִ��Ϊ10
if __name__ == "__main__":
    unittest.main()







