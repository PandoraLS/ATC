# -*- coding: utf-8 -*-
# @Time : 2020/12/23 下午2:00

"""
根据gen_result.txt 产生vocab.pkl
根据id_sentence_out_order.txt 产生
"""
import re, os, collections
import pickle

def delete_punctuation(text):
    """
    去掉句子中任意地方的英文标点符号
    :param text: 句子
    :return: 
    """
    text = re.sub(r'[^\w\s]', '', text)
    return text

def replace_time(text):
    """
    正则表达式匹配所有的时间,并将其替换为<TIME>
    如果没有时间, 则不进行替换
    :param text: 
    :return: 替换后的文本
    """
    # date_all = re.findall(r"(\d{1,2}:\d{1,2})", text)
    return re.sub(r'(\d{1,2}:\d{1,2})', '<TIME>', text)

def replace_num(text):
    """
    正则表达式匹配所有的数字并替换掉
    该程序在replace_time()之后运行
    # TODO 暂时不考虑小数
    :param text: 
    :return: 
    """
    return re.sub(r'(\d+)', '<NUM>', text)


def get_words(file):
    with open (file) as f:
        words_box=[]
        for line in f:                         
            if re.match(r'[a-zA-Z0-9]*',line): #避免中文影响
                words_box.extend(line.strip().split())               
    return (collections.Counter(words_box))


def gen_vocab():
    """
    根据gen_result.txt产生词表
    :return: 
    """
    tar_file = open('gen_result_rep.txt', 'w', encoding='utf8')
    with open('gen_result.txt') as src_file:
        for line in src_file:
            line = delete_punctuation(line)
            new_sentence = replace_time(line)
            new_sentence = replace_num(new_sentence)
            tar_file.write(new_sentence)
    
    
    words = get_words('gen_result_rep.txt')
    vocab_list = []
    for k, v in words.items():
        vocab_list.append(k)
    lent = len(vocab_list)
    vocab_dict = {}
    for i in range(lent):
        vocab_dict[vocab_list[i]] = i
    vocab_dict['<PAD>'] = lent + 1
    vocab_dict['<UNK>'] = lent + 2
    vocab_dict['##'] = lent + 3
    
    # print(vocab_dict)
    with open('vocab.pkl', 'wb') as pk:
        pickle.dump(vocab_dict, pk)

def replace_order_file():
    """
    根据id_sentence_order.txt产生词表
    :return: 
    """
    tar_file = open('id_sentence_out_order_rep.txt', 'w', encoding='utf8')
    with open('id_sentence_out_order.txt') as src_file:
        for line in src_file:
            line = delete_punctuation(line)
            _, sentence = line.split('\t')
            new_sentence = replace_time(sentence)
            new_sentence = replace_num(new_sentence)
            tar_file.write(_ + '\t' + new_sentence)
    
def generate_dataset():
    """
    将数据集分成train.txt, dev.txt, test.txt
    其中的时间全部替换成<TIME>, 数字全部替换成<NUM>
    :return: 
    """
    replace_order_file() # 其中的文件不能搞错了
    src_file = open('id_sentence_out_order_rep.txt')
    train_file = open('train.txt', 'w', encoding='utf8')
    dev_file = open('dev.txt', 'w', encoding='utf8')
    test_file = open('test.txt', 'w', encoding='utf8')
    src_lines = src_file.readlines()
    lent = len(src_lines)
    for i in range(lent):
        if 0 <= i < int(lent * 0.8):
            train_file.write(src_lines[i])
        elif int(lent * 0.8) <= i < int(lent * 0.9):
            dev_file.write(src_lines[i])
        else:
            test_file.write(src_lines[i])
    
def clean_file():
    """
    清除多余文件
    :return: 
    """
    os.remove('gen_result.txt')
    os.remove('gen_result_rep.txt')
    os.remove('id_sentence_out_order.txt')
    os.remove('id_sentence_out_order_rep.txt')


if __name__ == '__main__':
    gen_vocab()                 # 生成vocab.pkl
    generate_dataset()            # 生成train.txt, dev.txt, test.txt
    clean_file()                  # 清除必要文件
    
