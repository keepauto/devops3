#!/usr/bin/python
import sys

def read_file(filename):  
	file_object = open(filename)
	try:
		text = file_object.read( )
		return text
	finally:
		 file_object.close( )

def dealdate(txt):
	data = txt.replace(',',' ').replace('.',' ')
	print len(data.split())



	

 
if __name__ == '__main__':
	file = sys.argv[1]
	txt = read_file("dome.txt")
	dealdate(txt)