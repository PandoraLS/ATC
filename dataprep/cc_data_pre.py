import os, sys, io,re
sys.path.append(os.path.abspath('.'))
import argparse
import subprocess
# from data.utils import create_manifest
from tqdm import tqdm
import shutil  # pytest-shutil
import random
import math
import logging
import fnmatch

random.seed(10086)
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s [%(levelname)s] %(name)s:%(message)s')
log = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='处理民航数据')
parser.add_argument("--target-dir", default='/home/chenc/workspace/datesets',
                    type=str, help="Directory to store the dataset.")
parser.add_argument('--sample-rate', default=16000, type=int, help='Sample rate')

parser.add_argument('--min-duration', default=0, type=int,
                    help='Prunes training samples shorter than the min duration (given in seconds, default 1)')
parser.add_argument('--max-duration', default=27, type=int,
                    help='Prunes training samples longer than the max duration (given in seconds, default 15)')
parser.add_argument('--extract-dir', type=str, default='/home/chenc/workspace/datesets',
                    help='待提取的文件夹位置')
parser.add_argument('--seen', default=True, help='待提取的文件夹位置')
args = parser.parse_args()

# 全局变量
DATASET_SPLIT = {"train": 8, "val": 1, "test": 1}  # 数据集划分
NAME_SET = set()  # 所有名字集合,用于分辨unseen与seen
DATASET_LIST = []


def _preprocess_transcript(phrase):
    return phrase.strip().upper()


def _process_file(wav_path, txt_path, new_name, target_dir):
    target_wav_path = os.path.join(target_dir, 'wav', new_name + '.wav')
    target_txt_path = os.path.join(target_dir, 'txt', new_name + '.txt')
    if (os.path.exists(target_wav_path)) or os.path.exists(target_txt_path):
        log.warning('target 目录有重复文件，已经覆盖' + target_wav_path)
    subprocess.call(["sox {}  -r {} -b 16 -c 1 {}".format(wav_path,
                                                          str(args.sample_rate), target_wav_path)], shell=True)
    # process transcript
    transcriptions = ""
    with open(txt_path, 'r') as raw_transcript_file:
        transcriptions = raw_transcript_file.read().strip().split('\n')[0]
        if transcriptions == "":
            print("翻译文本不存在" + txt_path)

    with open(target_txt_path, "w") as f:
        f.write(_preprocess_transcript(transcriptions))
        f.flush()


def prep_en_data(source, target):
    target_dir = target  # 存放处理后的目录
    extracted_dir = source  # 存放将要处理的文件
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for split_type, _ in DATASET_SPLIT.items():
        # 创建target文件夹
        split_dir = os.path.join(target_dir, split_type)
        if not os.path.exists(split_dir):
            os.makedirs(split_dir)
        split_wav_dir = os.path.join(split_dir, "wav")
        if not os.path.exists(split_wav_dir):
            os.makedirs(split_wav_dir)
        split_txt_dir = os.path.join(split_dir, "txt")
        if not os.path.exists(split_txt_dir):
            os.makedirs(split_txt_dir)
            # 提取所有文件路径到list中
    if not os.path.exists(extracted_dir):
        log.error('源路徑不存在')
        return
    for root, subdirs, files in tqdm(os.walk(extracted_dir)):
        for f in files:
            std_name = root.split('/')[-2]
            NAME_SET.add(std_name)  # 将名字加入集合
            if f.find('.wav') != -1:
                wav_file_path = os.path.join(root, f)
                DATASET_LIST.append(wav_file_path)

    train_weight = DATASET_SPLIT['train']  # 训练集比例
    val_weight = DATASET_SPLIT['val']  # 验证集比例
    test_weight = DATASET_SPLIT['test']  # 测试集比例
    all_weight = train_weight + val_weight + test_weight
    train_weight = (float)(train_weight / all_weight)
    val_weight = (float)(val_weight / all_weight)
    test_weight = (float)(test_weight / all_weight)
    trainset = []
    valset = []
    testset = []
    # 根据是否seen划分数据集
    if args.seen:
        random.shuffle(DATASET_LIST)
        trainset_size = math.floor(train_weight * DATASET_LIST.__len__())
        val_size = math.ceil(val_weight * DATASET_LIST.__len__())
        trainset = DATASET_LIST[:trainset_size]
        valset = DATASET_LIST[trainset_size:trainset_size + val_size]
        testset = DATASET_LIST[trainset_size + val_size:]
    #  unseen
    else:
        NAME_LIST = list(NAME_SET)
        random.shuffle(NAME_LIST)
        #  属于train val集中的名字个数
        train_val_name_number = math.floor((train_weight + val_weight)
                                           * NAME_LIST.__len__())
        test_name_list = NAME_LIST[train_val_name_number:]  # test 名字列表
        for item in DATASET_LIST:
            if item.split('/')[-3] in test_name_list:
                testset.append(item)
            else:
                trainset.append(item)
        random.shuffle(testset)
        random.shuffle(trainset)
        trainset_size = math.floor((train_weight / (train_weight + val_weight))
                                   * trainset.__len__())
        valset = trainset[trainset_size:]
        trainset = trainset[:trainset_size]

    # 处理划分的数据集中的文件，并且复制到另一个文件夹中
    process_pre_dataset(trainset, 'train', target_dir)
    process_pre_dataset(valset, 'val', target_dir)
    process_pre_dataset(testset, 'test', target_dir)

    # 生成mainfest文件
    for split_type, _ in DATASET_SPLIT.items():
        if args.seen:
            create_manifest(os.path.join(target_dir, split_type), 'mingang_en_seen_' +
                        split_type + '.csv', args.min_duration, args.max_duration)
        else:
            create_manifest(os.path.join(target_dir, split_type), 'mingang_en_unseen_' +
                        split_type + '.csv', args.min_duration, args.max_duration)


def process_pre_dataset(trainset, types, target_dir):
    """
    用于将数据集中的音频文件转码与文件夹的重新分配
    :param trainset: 训练集
    :param type: 类型 train、test、val
    :param target_dir: 存放转换后的文件夹
    """
    for item in trainset:
        wav_name = item.split('/')[-1].split('.')[-2]  # wav名
        std_name = item.split('/')[-3]  # 学生姓名
        new_name = std_name + wav_name
        target_dir_pre = target_dir + '/' + types
        # 翻译文件path
        raw_txt_path = item.replace('wav', 'txt')
        if not os.path.exists(raw_txt_path):
            log.error("wav对应的txt文件不存在" + raw_txt_path)
            continue
        _process_file(item, raw_txt_path, new_name, target_dir_pre)

def create_manifest(data_path,
                    output_path,
                    min_duration=None,
                    max_duration=None):
    file_paths = [
        os.path.join(dirpath, f)
        for dirpath, dirnames, files in os.walk(data_path)
        for f in fnmatch.filter(files, '*.wav')
    ]
    # file_paths = order_and_prune_files(file_paths, min_duration, max_duration)
    with io.FileIO(output_path, "w") as file:
        for wav_path in tqdm(file_paths, total=len(file_paths)):
            transcript_path = wav_path.replace('/wav/', '/txt/').replace(
                '.wav', '.txt')
            trans = ''
            with open(transcript_path) as f:
                trans = f.readline()
                trans = replace_useless_char(trans)
            wav_filesize = os.path.getsize(wav_path)
            sample = os.path.abspath(wav_path) + ',' + str(wav_filesize)+',' + trans + '\n'
            file.write(sample.encode('utf-8'))
    print('\n')

def replace_useless_char(line):
    # 所有非字母符号
    ALL_NON_ALPH_CHAR = [
        ' ', '!', "'", '(', ')', ',', '-', '.', ':', '?', '’', '“', '”', '（',
        '）', '，', '？'
    ]  # 17 [' ', "'", ',', '-'] 4
    # 需要直接删除的字母
    DELETE_CHAR_LIST = ['.', '?', '!', '？', '”', '“']  # 6 .比较特殊
    # 需要被替换的字母,注释有对应的文本
    REPLACE_CHAR_DICT = {'，': ',', '’': '\'', ':': ','}  # 3
    # 需要删除括号中的字母
    DELETE_MID_CHAR_LIST = ['(', ')', '（', '）']  # 4

    # 因为有小数点，所以需要特别处理
    for find in re.findall(r'.{1}\.[a-zA-Z| ]', string=line):  # 居中.转,
        line = re.sub(r'.{1}\.[a-zA-Z| ]',
                      find.replace('.', ', '),
                      line,
                      count=1)
    line = re.sub(r'\.$', '', line, count=1)  # 末尾.
    # 删除处理
    for char in line:
        if char in DELETE_CHAR_LIST:
            if char == '.':  # 防止处理小数点
                continue
            line = line.replace(char, '')
    # 替换
    for char in line:
        if char in REPLACE_CHAR_DICT.keys():
            line = line.replace(char, REPLACE_CHAR_DICT.get(char))
    # 替换掉,为/,给csv文件特殊处理
    line = line.replace(',', '/')

    # 删除括号中的注释
    line = re.sub(r'(\(.+?\)|（.+?）)', ' ', line)

    # 删除多余空格
    line = re.sub(r' +', ' ', line.strip())
    return line

if __name__ == "__main__":
    en_src = "/share/datasets/minhang/pilot900_Processed"
    en_dst = "/share/datasets/minhang/processed_seen2"
    log.debug("hello")
    prep_en_data(en_src, en_dst)

