#!/usr/bin/env python
#encoding: utf-8
import unittest

# 第一步:统计每个字符的个数并放在字典里面

def str_count(mystr,total):
    user_dict = {}
    for i in mystr:
        user_dict.setdefault(i, 0)
        user_dict[i] += 1

    #第二步： 做颠倒
    tmp_dict = {}
    for _key, _value in user_dict.items():
        tmp_dict.setdefault(_value, [])
        tmp_dict[_value].append(_key)

    num_list = tmp_dict.keys()
    num_list.sort(reverse=True)
    _count = 0
    tmp1_dict = []
    for i in num_list:
        _chars = tmp_dict[i]
        _chars.sort()
        for x in _chars:
            tmp1_dict.append(x)
            _count += 1
            if _count >= total:
                break
        if _count >= total:
            break
    return tmp1_dict

class TestCameltoUnderline(unittest.TestCase):
    def test_count(self):
        teststr = "dasdxasdfasassdasaasdasda"
        underline = ['a', 's', 'd', 'f', 'x']
        self.assertEqual(str_count(teststr,10),underline)

if  __name__ == "__main__":
    unittest.main()
