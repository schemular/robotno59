#-*- coding:utf-8 -*-
#   Author  :   schemular(Tang Wei)
#   E-mail  :   schemular@gmail.com
#   Desc    :   Pickle数据库

from config import DATABASE_FOLDER
import cPickle as pickle
import os

dic = dict()

for filename in os.listdir(DATABASE_FOLDER):
    path = DATABASE_FOLDER + '/' + filename
    if (not (filename.startswith('.') and filename.endswith('~'))) and os.path.isfile(path):
        filehandle = open(path)
        dic[filename] = pickle.load(filehandle)

def store(name):
    path = DATABASE_FOLDER + '/' + name
    filehandle = open(path, 'w')
    pickle.dump(dic[name], filehandle)
    filehandle.close()
