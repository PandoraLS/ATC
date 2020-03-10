# -*- coding: utf-8 -*-
# Author：sen
# Date：2020/3/10 11:07

def pilot900en_wav():
    import os
    wavDir = "C:\\Users\\M\\Desktop\\yewenzheng\\"

    for root, dirs, files in os.walk(wavDir):
        for name in files:
            oldname = os.path.join(root, name)
            newname = oldname[:-7] + 'en' + oldname[-7:]
            os.rename(oldname, newname)


def pilot900en_wavandtrn():
    import os
    import shutil
    _wavDir = "C:\\Users\\M\\Desktop\\yewenzheng\\"
    _trnDir = "C:\\Education\\code\\ATC\\pilot900en_split_origin\\"
    trnFiles = sorted(os.listdir(_trnDir))
    ProductPath = "C:\\Users\\M\\Desktop\\yewenzheng2"
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
        speaker = wav_dir.split('\\')[-1]
        speaker_dir_name = ProductPath + "\\" + str(speaker)
        os.mkdir(speaker_dir_name)
        # print(speaker)
        # print(wav_dir)
        wavfiles = sorted(os.listdir(wav_dir))
        for wavfile in wavfiles:
            dirname = ProductPath + "\\" + str(speaker) + "\\" + str(wavfile[:-4])
            os.mkdir(dirname)
            transfile_source = _trnDir + "\\" + str(wavfile[:-4]) + ".txt"
            wav_source = wav_dir + "\\" + str(wavfile)
            transfile_target = dirname + "\\" + str(wavfile[:-4]) + ".txt"
            wav_target = dirname + "\\" + str(wavfile)
            shutil.copyfile(transfile_source, transfile_target)
            shutil.copyfile(wav_source, wav_target)

        # print(wavfiles)
    pass


if __name__ == '__main__':
    pass
    # pilot900en_wavandtrn()