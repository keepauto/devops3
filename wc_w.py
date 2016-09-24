import sys

def wordJudeg(chars):
    alphabetCount=0
    wordCount=0
    Status=0
    for i in chars:
        if ((i >= 'A' and i <= 'Z') or (i >= 'A' and i <= 'z')):
            alphabetCount+=1
            Status=0
        elif ((i == ' ') and (alphabetCount > 0) and (Status == 0)):
            wordCount+=1
            Status=1
        elif ((i == ',') and (alphabetCount > 0)):
            wordCount+=1
            Status=1
        elif ((i == '.') and (alphabetCount > 0)):
            wordCount+=1
            Status=1
    if chars[-1] == '-': wordCount-=1
    return wordCount


def mainReadpipe():
    textLength=0
    while True:
        content = sys.stdin.read()
        if len(content) > 0:
            textLength+=wordJudeg(content)
        else:
            break
    return textLength

def mainReadfile(fname):
    textLength=0
    with open(fname) as f:
        content = f.read(4096)
        textLength+=wordJudeg(content)
    return textLength

if __name__ == "__main__":
    if len(sys.argv) != 2:
        count = mainReadpipe()
        print("%d" % (count))
    else:
        count = mainReadfile(sys.argv[1])
        print("%d %s" % (count, sys.argv[1]))
