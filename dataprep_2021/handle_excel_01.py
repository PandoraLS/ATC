# -*- coding: utf-8 -*-
# @Time : 2020/11/30 下午12:07

"""
处理excel文件,将序号，文件名，转录结果一一对应起来
"""

import os

def rename_files():
    """
    根据atc_num_file_wav.txt文件来对wav音频重命名
    重新命的名为对应的序号
    :return: 
    """
    atc_num_file_wav_path = "/home/lisen/uestc/atc/code/atc_2021/atc_num_file_wav.txt"
    wav_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin_wav"
    num_to_wav_dict = {}
    with open(atc_num_file_wav_path) as src_file:
        for line in src_file:
            num, wav = line.strip().split('\t')
            # print(num, wav)
            num_to_wav_dict[wav] = num
            
    # for k, v in num_to_wav_dict.items():
    #     print(k, v)
        
    wav_list = os.listdir(wav_dir)
    for wav_item in wav_list:
        if wav_item in num_to_wav_dict.keys():
            new_wav_name = num_to_wav_dict[wav_item] + ".wav"
            os.rename(os.path.join(wav_dir,wav_item), os.path.join(wav_dir, new_wav_name))
        else:
            print(os.path.join(wav_dir, wav_item))
            

def handle_reference():
    """
    将文件名和reference对应起来
    后面再根据wav文件是否存在对txt某些行删除
    :return: 
    """
    src_file_path = "/home/lisen/uestc/atc/code/atc_2021/atc_num_reference.txt"
    tar_file_path = "/home/lisen/uestc/atc/code/atc_2021/atc_num_reference_target.txt"
    tar_file = open(tar_file_path, "w", encoding='utf8')
    
    with open(src_file_path) as src_file:
        for line in src_file:
            num, reference = line.strip().split('\t')
            new_line = num + '.wav\t' + reference
            tar_file.write(new_line)
            tar_file.write('\n')
    
def handle_reference2():
    """
    根据wav文件是否存在来对txt中的某些行进行删除
    :return: 
    """
    wav_dir = "/home/lisen/uestc/atc/dataset/yuyin_20201120/yuyin_wav"
    tar_file_path = "/home/lisen/uestc/atc/code/atc_2021/atc_num_reference_target.txt"
    tar2_file_path = "/home/lisen/uestc/atc/code/atc_2021/atc_num_reference_target2.txt"
    tar2_file = open(tar2_file_path, "w", encoding='utf8')

    wav_list = os.listdir(wav_dir)
    with open(tar_file_path) as tar_file:
        for line in tar_file:
            wav, reference = line.strip().split('\t')
            if wav in wav_list:
                tar2_file.write(line)
            else:
                # print(os.path.join(wav_dir, wav))
                pass

            
if __name__ == '__main__':
    print()
    # rename_files()

    # handle_reference()
    
    # handle_reference2()
    