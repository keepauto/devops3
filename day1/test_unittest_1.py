#!/usr/bin/env python
#coding=utf-8

import unittest


def camel_to_underline(camel_format):
    """
    驼峰命名格式转下划线命名格式
    """
    underline_format = ''
    if isinstance(camel_format, str):
        for _s_ in camel_format:
            underline_format += _s_ if _s_.islower() else '_' + _s_.lower()
    return underline_format

def underline_to_camel(underline_format):
    """
    下划线命名格式驼峰命名格式
    """
    camel_format = ""
    if isinstance(underline_format, str):
        for _s_ in underline_format.split('_'):
            camel_format += _s_.capitalize()
    return camel_format


class TestCameltoUnderline(unittest.TestCase):
    def test_upper_num(self):
        camel = "aaaC4321"
        underline = "aaa_c4321"
        self.assertEqual(camel_to_underline(camel), underline)

    def test_upper(self):
        camel = "aaaBbbbCccc"
        underline = "aaa_bbb_ccc"
        self.assertEqual(camel_to_underline(camel), underline)


if __name__ == "__main__":
    unittest.main()
