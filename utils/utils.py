# -*- coding: UTF-8 -*-

try:
    import cPickle as pickle
except ImportError:
    import pickle

import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def write_file(filename, content):
    with open(filename, "w") as fo:
        fo.write(content)

def serialize_result(filename, result):
    with open(filename, "w") as fo:
        pickle.dump(result, fo)

def merge_dict(x,y):
    for k,v in y.items():
                if k in x.keys():
                    x[k] += v
                else:
                    x[k] = v

def list_cmp(a, b):
    a = a['data']
    b = b['data']
    if cmp(a['wb'], b['wb']) != 0:
        if len(a['wb']) - len(b['wb']) != 0:
            return len(a['wb']) - len(b['wb'])
        else:
            return cmp(a['wb'], b['wb'])
    else:
        if len(a['aaa_mode']) - len(b['aaa_mode']) != 0:
            return len(a['aaa_mode']) - len(b['aaa_mode'])
        else:
            return cmp(a['aaa_mode'], b['aaa_mode'])


def list_cmp1(a, b):
    temp = list_cmp(a, b)
    a = a['data']
    b = b['data']
    if temp != 0:
        return temp
    else:
        return cmp(a['long_shutter'], b['long_shutter'])
