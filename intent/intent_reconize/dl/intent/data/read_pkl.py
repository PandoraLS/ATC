# -*- coding: utf-8 -*-
# @Time : 2020/12/23 下午1:30

import pickle
from pprint import pprint

with open('vocab.pkl', 'rb') as fo:
    list_data = pickle.load(fo, encoding='bytes')
    
pprint(list_data)

# with open('dev.txt','r') as f:
#     for line in f:
#         print(line)