# -*- coding: utf-8 -*-
# Author：lisen
# Date：20-1-7 上午11:03
import os, random, shutil
def PrepPilot900():
    import os
    en_list = []
    cn_list = []
    srcFile = "/home/lisen/uestc/code/DS2-pytorch/data/pilot1.txt"
    enFile = "/home/lisen/uestc/code/DS2-pytorch/data/pilot900_en.txt"
    cnFile = "/home/lisen/uestc/code/DS2-pytorch/data/pilot900_cn.txt"
    f = open(srcFile, 'r')
    raw_list = f.readlines()
    for i in range(len(raw_list)):
        if i % 2 == 0:
            en_list.append(raw_list[i])
        else:
            cn_list.append(raw_list[i])
    print(en_list)
    print(cn_list)
    f_dst = open(enFile, 'w')
    for i in en_list:
        f_dst.writelines(i)
    f_dst = open(cnFile, 'w')
    for i in cn_list:
        f_dst.writelines(i)
    f_dst.close()


def pilot900en_split():
    """
    将文本分为一个个的文件存入.txt文件中,转录文本不带序号,序号在文件名中得以体现
    :return: 
    """
    import re
    filename = "/home/lisen/uestc/code/DS2-pytorch/data/pilot900_en.txt"
    pilot900_en_trns = "/home/lisen/uestc/code/DS2-pytorch/data/pilot900_en_trns.txt"
    new_list = []
    f = open(filename, 'r')
    raw_list = f.readlines()
    dotIndexList = []
    for i in range(len(raw_list)):
        line = raw_list[i]
        if ". " in line:
            dot_index = [m.start() for m in re.finditer(". ", line)]
            dotIndexList.append(dot_index[0])
            new_line = line[dot_index[0] + 2:]
            new_list.append(new_line)
    path = "/home/lisen/uestc/code/DS2-pytorch/data/pilot900en_split/"
    for i in range(900):
        print("序号: ", i + 1, new_list[i], end="")
        fileNam = "en" + str(i + 1).zfill(3) + ".txt"
        f_in = open(path + fileNam, "w")
        f_in.write(new_list[i])
        f_in.close()

    print()


def pilot900en_wav():
    """
    将音频文件重命名并分配到文件夹,一个一个人的处理
    处理后的文件存储到另一个位置路径/
    :return: 
    /home/lisen/uestc/dataset/minhang/JiaFang/cuted900/李森_民航已处理数据/1~100寇帅201809/
    /home/lisen/uestc/dataset/minhang/JiaFang/Procuted900/koushuai/
    """
    import os
    path = "/home/lisen/uestc/dataset/minhang/JiaFang/cuted900/杨腾林-民航已处理数据/"
    wavDir = "/home/lisen/uestc/dataset/minhang/JiaFang/cuted900/吕忆蓝_民航已处理数据/尹楠1810班 20180111482"
    WAVDIR = []

    files = sorted(os.listdir(wavDir))
    tempNameSet = set()
    for file in files:
        print("文件: ", file, "数字标识:", file[2:8])
        tempNameSet.add(file[2:8])
        # tempNameSet.add(file[:3])
    tempNameList = sorted(list(tempNameSet))
    print(".........................")

    for file in files:
        if file[-4:] == ".wav":
            # print(file)
            oldname = wavDir + "/" + file
            for name in tempNameList:
                if name in file:
                    pre = name[:3]
                    idx2 = file[-6:-4]
                    newidx2 = int(pre) + int(idx2) - 1
                    newidx2 = str(newidx2).zfill(3)
                    newname2 = wavDir + "/" + "en" + str(newidx2) + ".wav"
                    print(oldname, "新名称--:", newname2)
                    os.rename(oldname, newname2)

    # for root, dirs, files in os.walk(path, topdown=False):
    #     for name in dirs:
    #         print(os.path.join(root, name))
    #         WAVDIR.append(os.path.join(root, name))
    # 
    # for wavDir in WAVDIR:
    #     files = sorted(os.listdir(wavDir))
    # 
    #     tempNameSet = set()
    #     for file in files:
    #         # print("文件: ", file, "前缀:", file[:10])
    #         tempNameSet.add(file[:12])
    # 
    #     tempNameList = sorted(list(tempNameSet))
    #     for i in tempNameList:
    #         print(i)
    # 
    #     print(".........................")
    #     for file in files:
    #         if file[-4:] == ".wav":
    #             # print(file)
    #             oldname = wavDir +"/" +file
    #             for name in tempNameList:
    #                 if name in file:
    #                     pre = name[:3]
    #                     idx2 = file[-6:-4]
    #                     newidx2 = int(pre) - 1 + int(idx2)
    #                     newidx2 = str(newidx2).zfill(3)
    #                     newname2 = wavDir+"/"+"en" + str(newidx2) +".wav"
    #                     print("old:", oldname, "new:", newname2)
    #                     os.rename(oldname, newname2)
    #     print("###############################################################################################")
    # print("文件名:", file, "前缀:", pre, "后缀序号:", idx2, "新后缀:", newidx2)

    pass


def detectedMissing():
    import os

    wavDir = "/home/lisen/uestc/dataset/minhang/JiaFang/Procuted900/lichenzhao/"
    files = sorted(os.listdir(wavDir))
    for i in range(0, 100):
        if "en" + str(i + 1).zfill(3) + ".wav" not in files:
            print("en" + str(i + 1).zfill(3) + ".wav")

def copyFile(fileDir):
    fileDir = "/home/lisen/uestc/data/DataMixTest/train_clean/"
    tarDir = '/home/lisen/uestc/data/DataMixTest/dev_clean/'
    # 1
    pathDir = os.listdir(fileDir)
    # 2
    sample = random.sample(pathDir, 750)
    print(sample)
    # 3
    for name in sample:
        shutil.copyfile(fileDir + name, tarDir + name)

def pilot900en_wavandtrn():
    import os
    _wavDir = "/home/lisen/uestc/dataset/minhang/JiaFang/Procuted900/301-400"
    _trnDir = "/home/lisen/uestc/dataset/minhang/JiaFang/pilot900en_split"
    trnFiles = sorted(os.listdir(_trnDir))
    ProductPath = "/home/lisen/uestc/dataset/minhang/JiaFang/Procuted900/pilot301_400"
    endDir = []
    for trnfile in trnFiles:
        endDir.append(trnfile[:-4])
    print(endDir)
    print(trnFiles)
    speakerDIR = []
    for root, dirs, files in os.walk(_wavDir, topdown=False):
        for name in dirs:
            # print("说话人:", os.path.join(root, name))
            speakerDIR.append(os.path.join(root, name))
    for i in sorted(speakerDIR):
        print(i)
    for wav_dir in sorted(speakerDIR):
        speaker = wav_dir.split('/')[-1]
        speaker_dir_name = ProductPath+"/"+str(speaker)
        os.mkdir(speaker_dir_name)
        # print(speaker)
        # print(wav_dir)
        wavfiles = sorted(os.listdir(wav_dir))
        for wavfile in wavfiles:
            dirname = ProductPath + "/" + str(speaker) + "/" + str(wavfile[:-4])
            os.mkdir(dirname)
            transfile_source = _trnDir + "/" + str(wavfile[:-4]) + ".txt"
            wav_source = wav_dir + "/" + str(wavfile)
            transfile_target = dirname + "/" + str(wavfile[:-4]) + ".txt"
            wav_target = dirname + "/" + str(wavfile)
            shutil.copyfile(transfile_source,transfile_target)
            shutil.copyfile(wav_source,wav_target)
            
            
        # print(wavfiles)
    pass


if __name__ == '__main__':
    # pilot900en_wavandtrn()
    # print(files)
    # pilot900en_wav()
    # detectedMissing()
    pass
    # pilot900en_split()
    # PrepPilot900()
