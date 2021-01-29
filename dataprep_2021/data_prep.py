# -*- coding: utf-8 -*-
# @Time : 2020/12/1 下午2:29

"""
将甲方的所给的 20201120标注工况.zip 筛选出可用的数据
已经筛选出的数据：/home/lisen/uestc/atc/dataset/yuyin_20201120_2000.txt

"""
import os
from handel_audio import creat_dir, forceCopyFile

#TODO 甲方给的数据会存在一些中文乱码(标点符号)，这部分需要用程序替换一下，而不是每次都手动替换

def prep_20201120_data():
    """
    整理出20201120标注工况数据中有用的部分
    :return: 
    """
    txt_file_path = "/home/lisen/uestc/atc/dataset/yuyin_20201120_2000.txt"
    src_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin_wav"
    tar_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin_wav_valid"
    
    if not os.path.exists(tar_dir):
        creat_dir(tar_dir)
        
    with open(txt_file_path) as src_file:
        for line in src_file:
            wav = line.strip().split(',')[0]  # 有效文件
            forceCopyFile(os.path.join(src_dir, wav), os.path.join(tar_dir, wav))
            

def prep_txt():
    """
    根据1983条数据找到对应的文本
    :return: 
    """
    wav_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin_wav_valid_8h"
    wav_list = os.listdir(wav_dir)
    src_txt_file_path = "/home/lisen/uestc/atc/code/atc_2021/groundtruth.txt"
    tar_txt_file_path = "/home/lisen/uestc/atc/code/atc_2021/yuyin_20201120_1983.txt"
    tar_file = open(tar_txt_file_path, "w", encoding="utf8")
    with open(src_txt_file_path) as src_file:
        for line in src_file:
            new_line = line.strip().split('\t')  # 有效文件
            if new_line[0] + '.wav' in wav_list:
                tar_file.write(new_line[0] + '\t' + new_line[-1] + '\n')
    

if __name__ == '__main__':
    print()
    # prep_20201120_data()
    
    prep_txt()
