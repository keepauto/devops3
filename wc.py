#!/usr/bin/env python
# encoding: utf-8

t = open("th.txt", "r")
a = t.read().split(" ")
words = {}
for t in a:
    words.setdefault(t, 1)
    words[t] = int(words.get(t)) + 1

print words
