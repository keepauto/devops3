#coding:utf-8
import pdb
import sys
import unittest
import re

def read_in_chunks(input_file,chunk_size):
    with open(input_file,'r') as f:
	while True:
	    data = f.read(chunk_size)
	    if data:
	        match = re.findall(r'[^a-zA-Z0-9]+', data)
	        for i in match:
	      	    data = data.replace(i,' ')
	    	    yield data
	    else:
	        break

def make_dict(input_file,chunk_size):  
    for words in read_in_chunks(input_file,chunk_size):
        words = words.split()
    dict_word = {}  
    for word in words:  
        dict_word[word] = dict_word.get(word,0)+1
    return dict_word

def word_sort(input_file,chunk_size):  
    dict_word = make_dict(input_file,chunk_size)
    return sorted(dict_word.items(), key=lambda x: x[1], reverse=True)

class TestWordSort(unittest.TestCase):
    def test_word_sort(self):
	input_file = './testfile'
        chunk_size = 1024
	sort = word_sort(input_file,chunk_size)
	test_sort = [('sc', 3), ('Tom', 2), ('st', 1)]
	self.assertEqual(sort, test_sort)

if __name__ == "__main__":
    unittest.main()
