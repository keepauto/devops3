#coding:utf-8
import pdb
import sys
import unittest

keep=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',' ','-',"'"]  
def normalize(chars):  
    result=''  
    for char in chars.lower():  
        if char in keep:  
            result += char  
#    pdb.set_trace()
    return result  

def make_dict(chars):  
    words = normalize(chars).split()  
#    pdb.set_trace()
    dict_word = {}  
    for word in words:  
        dict_word[word] = dict_word.get(word,0)+1
    return dict_word

def word_sort(f):  
    chars = open(f).read()  
    dict_word = make_dict(chars)
    list_word = [(dict_word[word],word) for word in dict_word]  
#    pdb.set_trace()
    list_word.sort()  
    list_word.reverse()  
    return list_word
#    print('前10名出现次数最多的单词和次数是：')  
#    i=1  
#    for count,word in list_word[:10]:  
#        print('%d.%4d %s'%(i,count,word))  
#        i+=1  

#word_sort(sys.argv[1])

class TestWordSort(unittest.TestCase):
    def test_word_sort(self):
	f = './tomcat'
	sort = word_sort(f)
	test_sort = [(3, 'sc'), (2, 'tom'), (1, 'st')]
	self.assertEqual(sort, test_sort)

if __name__ == "__main__":
    unittest.main()
