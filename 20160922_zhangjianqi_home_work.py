#!/usr/bin/python

import unittest
#my_str=raw_input("input str: ")
#print "str: ",my_str


def homework(my_str):
    my_dic={}
    
    for s in my_str:
    
       if s not in my_dic.keys():
         my_dic[s]=1
       else:
         my_dic[s] += 1
    over_list = sorted(my_dic.items(),key=lambda a: a[1],reverse=True)
    print over_list
    print "The first three character",over_list[0:2]
    return my_dic



#print homework('asdasd')
#print my_dic.items()



class myunittest(unittest.TestCase):
    def mytestcase(self):
        test_str = "asdasd"
        my_result= {'a': 2, 's': 2, 'd': 2}
        self.assertEqual(mytestcase(test_str), my_result)



if __name__ == "__main__":
    unittest.main()
