# -*- coding: utf-8 -*-
# Author：sen
# Date：2020/3/10 17:40

import os
import random
import shutil
from pprint import pprint
from collections import defaultdict


def cross5(src_dir):
    # 将原始数据打乱并分配到5个文件夹里面
    # src_dir = "C:\\Users\\M\\Desktop\\seen_cross5_origin\\pilot101_200"
    count = 0
    basename = os.path.basename(src_dir)
    # dirs = os.listdir(src_dir)
    for dir_name in os.listdir(src_dir):
        print(dir_name)
        for en_name in os.listdir(os.path.join(src_dir, dir_name)):
            os.rename(os.path.join(src_dir, dir_name, en_name),
                      os.path.join(src_dir, dir_name, basename + '_' + dir_name + '_' + en_name))    


def copy_dirs():
    dest_dir = r'C:\Users\M\Desktop\pilot900_Processed_'
    # shutil.move(r'C:\Users\M\Desktop\hello', dest_dir)
    
    root_dir=  r'C:\UESTC\项目-民航语音\pilot900_Processed'
    for pilot_x in os.listdir(root_dir):
        print(pilot_x)
        pilot_x_path = os.path.join(root_dir, pilot_x)
        for name in os.listdir(pilot_x_path):
            name_path = os.path.join(pilot_x_path, name)
            print(name_path)
            for en_name in os.listdir(name_path):
                en_path = os.path.join(name_path, en_name)
                # print(en_path)
                # shutil.move(en_path, dest_dir)
        

def shuffle_move():
    src_dir = r'C:\UESTC\项目-民航语音\pilot900_Processed2'
    dest_dir = r'C:\UESTC\项目-民航语音\pilot900_Processed3'
    path = list(os.listdir(src_dir))
    # path = [i for i in range(11276)]
    random.shuffle(path)
    part_cnt = len(path) // 5
    dest_idx = 0

    for i in range(4):
        part_path = path[i*part_cnt:(i+1)*(part_cnt)]
        dest_path = os.path.join(dest_dir, 'dataset' + str(i))
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for p in part_path:    
            shutil.move(os.path.join(src_dir, p), dest_path)
        print(len(part_path))
    last_path = path[(i+1)*part_cnt:len(path)]
    dest_path = os.path.join(dest_dir, 'dataset' + str(i+1))
    if not os.path.exists(dest_path):
        os.makedirs(dest_path)
    for p in last_path:
        shutil.move(os.path.join(src_dir, p), dest_path)
    print(len(last_path))
    
    
    
    pass


def moveFile():
    src = "C:\\Users\\M\\Desktop\\seen_cross5_origin\\pilot101_200\\liuzhilin\\en001"

    # filenumber = len(pathDir)
    # # rate = 0.1  # 自定义抽取图片的比例，比方说100张抽10张，那就是0.1
    # # picknumber = int(filenumber * rate)  # 按照rate比例从文件夹中取一定数量图片
    # picknumber = 50
    # sample = random.sample(pathDir, picknumber)  # 随机选取picknumber数量的样本图片
    # print(sample)
    # # for name in sample:
    # #     # shutil.move(fileDir + name, tarDir + name)
    # return

def list_split(n, part, shuffle):
    assert part > 0, 'part should > 0'
    idx = [i for i in range(n)]
    if shuffle:
        random.shuffle(idx)
    parts = []
    part_cnt = n // part
    for i in range(part-1):
        each_part = idx[i*part_cnt:(i+1)*(part_cnt)]
        parts.append(each_part)
    last_part = idx[(i+1)*part_cnt:n]
    parts.append(last_part)
    return parts


def people():
    root = r'C:\UESTC\项目-民航语音\pilot900_Processed2'
    dest_dir = r'C:\UESTC\项目-民航语音\pilot900_Processed_unseen'
    names = defaultdict(list)
    for name in os.listdir(root):
        x = name.split('_')[-2]
        names[x].append(name)
    
    names_key = list(names.keys())
    names_parts = list_split(len(names_key), 5, shuffle=True)
    
    for i, part in enumerate(names_parts):
        print(i, '-' * 30)
        name_part = []
        dest_path = os.path.join(dest_dir, 'dataset' + str(i))
        if not os.path.exists(dest_path):
            os.makedirs(dest_path)
        for idx in part:
            name_part.append(names_key[idx])
        for name in name_part:
            print(name)
            for dir_name in names[name]:
                shutil.move(os.path.join(root, dir_name), dest_path)
            


if __name__ == '__main__':
    pass