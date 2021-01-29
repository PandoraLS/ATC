# -*- coding: utf-8 -*-
# @Time : 2020/11/30 下午12:25

"""
处理音频文件，将acc文件修改为wav文件
参考链接：https://blog.csdn.net/buki26/article/details/85005576

命令：ffmpeg -i 2.aac -ar 16000 2.wav
"""

import os
import shutil
import tqdm
# import logger

def creat_dir(d):
    """
    新建文件夹
    Args:
        d: 文件夹路径
    Returns:
    """
    if not os.path.exists(d):
        os.makedirs(d)

def forceCopyFile(sfile, dfile):
    """
    将文件覆盖拷贝
    Args:
        sfile: 源文件path
        dfile: 目标文件path
    Returns:
    """
    if os.path.isfile(sfile):
        shutil.copy2(sfile, dfile)

def trans_one_audio(aac_path, wav_path):
    # aac_path = "/home/lisen/uestc/atc/dataset/yuyin_20201120/2.aac"
    # wav_path = "/home/lisen/uestc/atc/dataset/yuyin_20201120/2.wav"
    
    cmd = "ffmpeg -i " + aac_path + " -ar 16000 " + wav_path
    with os.popen(cmd) as pipe:
        cmd_output = pipe.read()
        
def trans_dir_audio(src_dir, tar_dir):
    """
    将甲方的aac格式的文件转换为wav文件
    :param src_dir: 
    :param tar_dir: 
    :return: 
    """
    # src_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin"
    # tar_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin_wav"
    
    if not os.path.exists(tar_dir):
        creat_dir(tar_dir)
    
    files = os.listdir(src_dir)
    for file in files:
        if file[-4:] == '.wav':
            forceCopyFile(os.path.join(src_dir, file), os.path.join(tar_dir, file))
        elif file[-4:] == '.aac':
            trans_one_audio(os.path.join(src_dir, file), os.path.join(tar_dir, file[:-4] + '.wav'))
        else:
            print(os.path.join(src_dir, file))
            

if __name__ == '__main__':
    # trans_one_audio()
    
    src_dir = "/home/lisen/uestc/atc/dataset/exam02/audio02"
    tar_dir = "/home/lisen/uestc/atc/dataset/exam02/audio02_wav"
    trans_dir_audio(src_dir, tar_dir)
    
