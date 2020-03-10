# -*- coding: utf-8 -*-
# Author：sen
# Date：2020/3/10 21:00

from pprint import pprint
import shutil
import os.path
import os


def move():
    root = r'C:\Users\M\Desktop\cn_wav'
    for dir_name in os.listdir(root):
        pass


def txt_write(src):
    # src = r'C:\Users\M\Desktop\cn_wav\A1'
    txtfile = os.path.join(src, src.split('\\')[-1] + '.txt')
    with open(txtfile,'r',encoding='utf-8') as f:
        for line in f:
            elems = line.strip().split()
            name = elems[0] + '.txt'
            sentense = ' '.join(elems[1:]) + '\n'
            with open(os.path.join(src,name),'w',encoding='utf-8') as dst_f:
                dst_f.write(sentense)    
    # for i in files:
    #     if i[-4:] == '.txt':
    #         print(os.path.join(src, i))
    #         f = open(os.path.join(src, i),'r')
    #         file_list = f.readlines()
    pass


def folder_create(src):
    # src = r"C:\Users\M\Desktop\testA1"
    files = os.listdir(src)
    for file in files:
        if file[-4:] == '.txt':
            # print(file[:-4])
            dest_dir = os.path.join(src, file[:-4])
            # print(dest_path)
            if not os.path.exists(dest_dir):
                os.makedirs(dest_dir)
            src_txt_path = os.path.join(src,file)
            src_wav_path = os.path.join(src,file[:-4]+'.wav')
            print(src_txt_path)
            print(src_wav_path)
            shutil.move(src_txt_path, dest_dir)
            shutil.move(src_wav_path, dest_dir)


if __name__ == '__main__':
    root =r"C:\Users\M\Desktop\cn_wav"
    path = os.listdir(root)
    for i in path:
        new_path = os.path.join(root,i)
        print(new_path)
        folder_create(new_path)
        
        # os.remove(rm_path)
        # txt_write(new_path)
    # txt_write()
    # folder_create()