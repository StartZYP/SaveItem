# -*- coding: utf-8 -*-
import random

#import random
def getHash(text):
     hashcode = getmidstring(text, 'formhash" value="', '"')
     #print(hashcode)
     return hashcode

def getagreebbrule(text):
    agreebbrule = getmidstring(text, 'agreebbrule" value="', '"')
    return agreebbrule

def layer_login_(text):
    logincode = getmidstring(text,'layer_login_','"')
    #print(logincode)
    return logincode
def getmidstring(html, start_str, end):
    #print(html)
    start = html.find(start_str)
    if start >= 0:
        start += len(start_str)
        end = html.find(end, start)
        if end >= 0:
            return html[start:end].strip()


def confusion(filePath):
   #打开文件，读取数据
    f =open(filePath, 'r')
    str0=f.read()
    str1=""
    list = str0.splitlines()
    print(list)
    filter(None, list)
    random.shuffle(list)
    for i in list:
        str1+=i+"\n"
    print(str1)
    w =open(filePath, 'w')
    w.write(str1)
    w.close()
