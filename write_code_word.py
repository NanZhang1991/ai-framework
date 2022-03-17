# -*- coding: utf-8 -*-

import os
from pathlib import Path

# 获取当前的路径
def getfilepath_write_word():
    file = open('allcode.docx','a+',encoding='utf-8')
    for parent,dirnames,filenames in os.walk(os.getcwd()):
        for filename in filenames:
            path = Path(os.path.join(parent, filename)).as_posix() 
            if path.endswith('.py'):
                with open(path,'r',encoding='utf-8') as f:
                    for line in f.readlines():
                        print(line, file=file)
    print('代码写入成功')


if __name__ == '__main__':
   getfilepath_write_word()

