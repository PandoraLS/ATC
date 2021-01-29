# -*- coding: utf-8 -*-
# @Time    : 2020/12/21 15:02
# @Author  : sen

import json
import re
import random
import math

tag_lists = {
    1:"TIME",2:"TIMED",3:"ADMIN_AREA",4:"COUNTRY_AREA",5:"GEOGRAPHY_AREA",6:"SATELLITE",7:"LOAD",
    8:"RESOLUTION",9:"LEVEL",10:"CODE",11:"SITE",12:"EVENT",13:"EVENT_NAME",14:"TARGET_NAME",15:"LATITUDE",
    16:"TARGET_RESPO",17:"TRACE_TIME",18:"TRACE_TARGET",19:"WINDOWS_COMMAND",20:"WINDOWS_NAME",
    21:"INSTRACT",22:"INSTRACT_NUM", 23:"ADD_23", 24:"ADD_24", 25:"ADD_25", 26:"ADD_26", 27:"ADD_27",
    28:"ADD_28",29:"ADD_29", 30:"ADD_30", 31:"ADD_31", 32:"ADD_32", 33:"ADD_33",34:"ADD_34", 35:"ADD_35", 36:"ADD_36",
    37:"ADD_37", 38:"ADD_38", 39:"ADD_39", 40:"ADD_40",41:"ADD_41", 42:"ADD_42", 43:"ADD_43",
    44:"ADD_28",45:"ADD_29", 46:"ADD_30", 47:"ADD_31", 48:"ADD_32", 49:"ADD_33",50:"ADD_34", 51:"ADD_35", 52:"ADD_36",
    53:"ADD_37", 54:"ADD_38", 55:"ADD_39", 56:"ADD_40",57:"ADD_41", 58:"ADD_42", 59:"ADD_43"
}

index2type = {
    "0": "高度的描述",
    "1": "高度的改变、报告和升降率及TCAS指令",
    "2": "管制移交及转换频率",
    "3": "呼号的改变",
    "4": "飞行活动通报",
    "5": "气象情报",
    "6": "位置报告",
    "7": "附加报告",
    "8": "机场情报",
    "9": "助航设备工作状况"
}

base_sentences = json.load(open("sentence.json", mode="r", encoding="utf-8"))
short_sentences = json.load(open("short_sentence.json",mode='r',encoding='utf-8'))


def get_rand_short(short_value_list):
    '''
    根据类型随机获取一个短语
    :param short_value_list: [1,2]
    :return: str
    '''
    # s = re.sub("#1#","chenc",string="#1##2",count=1)
    random_i = random.randint(0,len(short_value_list)-1)
    index = short_value_list[random_i] # 0-22
    types = short_sentences[str(index)]
    random_i = random.randint(0,len(types)-1)
    moban = list(types.items())[random_i]
    sentence = moban[0]
    for position in moban[1].keys():
        re_str = '#'+position+'#'
        if moban[1][position]['type'] == 'num':
            start = moban[1][position]['range'][0]
            end = moban[1][position]['range'][1]
            if 0 < start and start < 1:
                value = float(random.randint(math.ceil(start), end*10))/10
            else:
                value = random.randint(start, end)
            value = num2hanzi(value)
        else:
            ranges = list(moban[1][position]['range'])
            value = ranges[random.randint(0,len(ranges)-1)]
        sentence = re.sub(re_str,str(value),string=sentence,count=1)
    return sentence,index

def num2hanzi(num,is_public=True):
    '''
    数字转汉字
    :param num:
    :param is_public:数字读法是否为公共读法
    :return:
    '''
    lists_num = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9"
    }
    hanzi = ""
    if num - math.ceil(num) != 0: # 小数
        integer = math.floor(num)
        hanzi_integer = num2hanzi(integer)
        re_str = r"[\d]+\.([\d]+)"
        hanzi_decimal = ""
        for match in re.finditer(re_str,str(num)):
            for char in match.group(1):
                hanzi_decimal += lists_num[char]
        hanzi_decimal = "点" + hanzi_decimal
        hanzi = hanzi_integer+hanzi_decimal
    else:
        for char in str(num):
            hanzi += lists_num[char]
    return hanzi


def num2hanzi_simple(sentence):
    '''
    简单的处理数字转汉字
    :param sentence:
    :return:
    '''
    lists_num = {
        "0": "0",
        "1": "1",
        "2": "2",
        "3": "3",
        "4": "4",
        "5": "5",
        "6": "6",
        "7": "7",
        "8": "8",
        "9": "9"
    }
    for c in sentence:
        if c in lists_num.keys():
            sentence = re.sub(c,lists_num[c],sentence,count=1)
    return sentence


def generate_txt():
    sentences = []
    train_sentences = []
    for key, value in base_sentences.items():
        moban = key
        moban_count = value['count'] * 5
        short_type = value['index']
        moban_position = list(short_type.keys())
        moban_position.sort()
        for i in range(moban_count):
            temp_dict = dict()
            sentence = moban
            init_end_index = sentence.index('#')
            temp_dict['word'] = []
            temp_dict['tag'] = []
            # for j in range(init_end_index):
            #     temp_dict['word'].append(sentence[j])
            #     temp_dict['tag'].append('O')
            prev_idx = 0
            for index in moban_position:
                re_str = '#' + index + '#'
                start_index = sentence.index('#')
                # 当前槽前面的非槽字符
                for j in range(prev_idx, start_index):
                    temp_dict['word'].append(sentence[j])
                    temp_dict['tag'].append('O')
                short_value_lists = short_type[index]
                short_sentence, type = get_rand_short(short_value_lists)  # type表示短语类别
                short_sentence = num2hanzi_simple(short_sentence)  # 将所有数字转成汉字
                sentence = re.sub(re_str, short_sentence, string=sentence, count=1)
                end_index = len(short_sentence) + start_index - 1
                prev_idx = end_index + 1
                temp_dict['word'].append(sentence[start_index])
                temp_dict['tag'].append('B-' + tag_lists[type])
                for j in range(start_index + 1, end_index):
                    temp_dict['word'].append(sentence[j])
                    temp_dict['tag'].append('I-' + tag_lists[type])
                temp_dict['word'].append(sentence[end_index])
                temp_dict['tag'].append('I-' + tag_lists[type])
            else:
                # 最后一个槽后面的非槽字符
                for j in range(prev_idx, len(sentence)):
                    temp_dict['word'].append(sentence[j])
                    temp_dict['tag'].append('O')

            train_sentences.append(temp_dict)
            sentences.append(sentence)
        # print(sentences)

    random.shuffle(train_sentences)
    train_datasets = train_sentences[:int(8 * len(train_sentences) / 10)]
    test_datasets = train_sentences[int(8 * len(train_sentences) / 10):int(9 * len(train_sentences) / 10)]
    dev_datasets = train_sentences[int(9 * len(train_sentences) / 10):]
    # train_file = "train.char.bmes"
    # test_file = "test.char.bmes"
    # dev_file = "dev.char.bmes"
    # f_train = open(train_file, mode='w', encoding='utf-8')
    # f_test = open(test_file, mode='w', encoding='utf-8')
    # f_dev = open(dev_file, mode='w', encoding='utf-8')
    # for f, d in zip([f_dev, f_test, f_train], [dev_datasets, test_datasets, train_datasets]):
    #     for item in d:
    #         words = item['word']
    #         entitys = item['tag']
    #         for word, entity in zip(words, entitys):
    #             f.write(word + ' ' + entity + '\n')
    #         f.write('\n')

    with open("gen_result.txt", 'w', encoding='utf-8') as f:
        for s in sentences:
            f.write(s + '\n')




"""
当sentence.json中的count=1时,generate_txt()会产生
m * 5条语句
对应的分类为[start,end)：
    数目:5        [0,5):              "1":"高度的描述",
    数目:165      [6,170):            "2":"高度的改变、报告和升降率及TCAS指令",
    数目:65       [171,235):          "3":"管制移交及转换频率",
    数目:20       [236,255):          "4":"呼号的改变",
    数目:40       [256,295):          "5":"飞行活动通报",
    数目:105      [296,400):          "6":"气象情报",
    数目:15       [401,415):          "7":"位置报告",
    数目:25       [416,440):          "8":"附加报告",
    数目:55       [441,495):          "9":"机场情报",
    数目:25       [496,520):          "10":"助航设备工作状况"
count>1时，start和end均变成count * m * 5
"""

def class_id(count, class_num):
    """
    根据sentence.json中的count创建id编号
    :param count: sentence.json中的数值
    :parm class_num: 种类数, 这里为10
    :return: id编号list
    """
    # id_count = [5, 165, 65, 20, 40, 105, 15, 25, 55, 25]
    # id_count = [5, 10]
    id_count = [40, 25, 15, 20, 140, 25, 25, 50]
    ID = []
    for i in range(class_num):
        ID.extend([str(i)] * id_count[i-1] * count)
    return ID

def concat_id_txt(ID):
    """
    将id和sentence组合起来
    :param ID: 对应的分类id
    :return:
    """
    src_file = open('gen_result.txt')
    tar_file = open('id_sentence_order.txt', 'w', encoding='utf8')
    sentence_list = src_file.readlines()
    for i in range(len(ID)):
        new_line = ID[i] + '\t' + sentence_list[i].strip(' ')
        tar_file.write(new_line)

def shuffle_file():
    tar_file_out_order = open('id_sentence_out_order.txt', 'w', encoding='utf8')
    src_file = open('id_sentence_order.txt')
    sentence_list = src_file.readlines()
    random.shuffle(sentence_list)
    for line in sentence_list:
        tar_file_out_order.write(line)


if __name__ == '__main__':
    # 注意count要和sentence.json中保持一致
    generate_txt()
    print("Module!")
    ID = class_id(count=20, class_num=8)
    concat_id_txt(ID=ID)
    shuffle_file()
