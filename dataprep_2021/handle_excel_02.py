# -*- coding: utf-8 -*-
# @Time : 2020/11/30 下午12:07

"""
处理excel文件,将序号，文件名，转录结果一一对应起来
"""


import os

def rename_files():
    """
    根据audio02.txt文件来对wav音频重命名
    重新命的名为对应的序号
    :return: 
    """
    atc_num_file_wav_path = "/home/lisen/uestc/atc/code/atc_2021/audio01.txt"
    wav_dir = "/home/lisen/uestc/atc/dataset/exam02/audio01_wav"
    num_to_wav_dict = {}
    with open(atc_num_file_wav_path) as src_file:
        for line in src_file:
            num, wav, reference = line.strip().split('\t')
            # print(num, wav)
            # num_to_wav_dict[wav] = num.zfill(3)     # 将数据变成固定位数的，不够的前面补零
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
    
def handle_reference2():
    """
    根据wav文件是否存在来对txt中的某些行进行删除
    :return: 
    """
    wav_dir = "/home/lisen/uestc/atc/dataset/exam02/audio01_wav"
    txt_path = "/home/lisen/uestc/atc/code/atc_2021/audio01.txt"
    target_txt_path = "/home/lisen/uestc/atc/code/atc_2021/audio01_target.txt"
    tar_file = open(target_txt_path, "w", encoding='utf8')

    wav_list = os.listdir(wav_dir)
    with open(txt_path) as txt_file:
        for line in txt_file:
            wav, reference = line.strip().split('\t')
            if wav in wav_list:
                tar_file.write(line)
            else:
                print(os.path.join(wav_dir, wav))
                # pass


            
if __name__ == '__main__':
    print()
    # rename_files()

    # handle_reference()
    
    handle_reference2()
    