# -*- coding: utf-8 -*-
# Author：sen
# Date：2020/3/10 11:49

def pilot900en_wavandtrn():
    import os
    import shutil
    ProductPath = "C:\\Users\\M\\Desktop\\limeng\\"
    trnDir = "C:\\Education\\code\\ATC\\pilot900en_split_origin\\"
    trnFiles = sorted(os.listdir(trnDir))
    # print(trnFiles)
    for root, dirs, files in os.walk(ProductPath):
        for name in files:
            if name[-4:] == '.txt':
                src_file = os.path.join(trnDir, name)
                tar_file = os.path.join(root, name)
                f_src = open(src_file, 'r')
                src_list = f_src.readlines()
                f_dst = open(tar_file, 'w')
                for i in src_list:
                    f_dst.writelines(i)
                f_src.close()
                f_dst.close()

if __name__ == '__main__':
    pilot900en_wavandtrn()
