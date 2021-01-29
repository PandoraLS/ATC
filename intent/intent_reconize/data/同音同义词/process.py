import codecs
import jieba
import random
import time
import logging
from functools import reduce
import multiprocessing

jieba.setLogLevel(logging.INFO)
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s: %(name)s: %(levelname)s: %(message)s")


CORPUS = '../txt_gen_gen_result.txt'
PROCESSED_CORPUS = '../proc_result.txt'

# 同义字词
CILIN = 'DIAC/cilin.txt'
# 同音字
SAMEPIN = 'DIAC/same_pinyin.txt'
# 同音字
HOMOPHONE_CHAR = 'ChineseHomophones/chinese_homophone_char.txt'
# 同音词
HOMOPHONE_WORD = 'ChineseHomophones/chinese_homophone_word.txt'

RANDOM_SEED = 0
KEEP_ROANDOM_STATE = False


def write_file(filename, content, mode='w'):
    with codecs.open(filename, mode, encoding='utf-8') as f:
        for c in content:
            f.write(str(c) + "\n")

def set_random_seed():
    if KEEP_ROANDOM_STATE:
        random.seed(0)

# 获取cilin.txt中的同义词列表
# TODO: 根据语料库的词汇过滤不相关的list
def gen_synonyms_dict(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        synonyms_dict = []
        for s in f:
            synonyms_dict.append(s.strip().split(' ')[1:])
        return synonyms_dict

# 获取word的同义词列表
def get_synonyms(word, synonyms_dict):
    for synonyms in synonyms_dict:
        if word in synonyms:
            return synonyms

    return []

# 随机替换同义词
def random_replace_synonyms(n_sent, synonyms_dict):
    ret = []
    tokens = jieba.cut(n_sent)
    for w in tokens:
        # 以一定的概率 替换为一个同义词
        set_random_seed()
        pb = random.random()
        if pb < 0.3:
            synonyms = get_synonyms(w, synonyms_dict)
            set_random_seed()
            nw = random.choice(synonyms) if synonyms!=[] else w
        else:
            nw = w

        ret.append(nw)

    return "".join(ret)

# 获取chinese_homophone_word.txt中的同音词列表
# 由于词汇表过大 只截取前2w行 设置shorter=-1可读取整个文件
def gen_homophone_dict(filename, shorter=20000):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        homophone_dict = []
        count = 0
        for h in f:
            homophone_dict.append(h.strip().split('\t')[1:])
            count += 1
            if count >= shorter:
                break
        return homophone_dict

# 获取word的同音词列表
def get_homophone(word, homophone_dict):
    for homophone in homophone_dict:
        if word in homophone:
            return homophone

    return []

# 随机替换同音词
def random_replace_homophone(n_sent, homophone_dict):
    ret = []
    tokens = jieba.cut(n_sent)
    for w in tokens:
        # 以一定的概率 替换为一个同音词
        set_random_seed()
        pb = random.random()
        if pb < 0.3:
            homophone = get_homophone(w, homophone_dict)
            set_random_seed()
            nw = random.choice(homophone) if homophone!=[] else w
        else:
            nw = w

        ret.append(nw)

    return "".join(ret)

# 获取同音字词典
def gen_same_pin(filename):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        samepin_dict = []
        for sp in f:
            samepin_dict.append(reduce(lambda x,y:x+y, sp.strip().split('\t')))
        return samepin_dict

# 获取与word同音的字列表
def get_samepin(word, samepin_dict):
    for samepin in samepin_dict:
        if word in samepin:
            return samepin

    return []

# 随机增加同音字(代表该字被重复识别(如回音))
def random_add_word(n_sent, samepin_dict):
    ret = []
    for w in n_sent:
        set_random_seed()
        pb = random.random()
        if pb < 0.1:
            samepin = get_samepin(w, samepin_dict)
            # 20%概率重复两次
            set_random_seed()
            nw = random.choice(samepin)*random.choice([1,1,1,1,2]) if samepin!=[] else w
        else:
            nw = w

        ret.append(nw)

    return "".join(ret)

# 随机删减一些字(代表没有识别到该字(如发音较弱))
def random_remove_word(n_sent):
    ret = []
    for w in n_sent:
        set_random_seed()
        pb = random.random()
        # 以80%的概率保留这个字
        if pb > 0.1:
            ret.append(w)

    return "".join(ret)

# 对句子进行多次变换处理
def sentence_process(sent, synonyms_dict, homophone_dict, samepin_dict):
    n_sent = sent.strip()

    # 1. 随机同义词替换
    n_sent = random_replace_synonyms(n_sent, synonyms_dict)
    # 2. 随机同音词替换
    n_sent = random_replace_homophone(n_sent, homophone_dict)
    # 3. 随机掩码插入同音字
    n_sent = random_add_word(n_sent, samepin_dict)
    # 4. 随机掩码丢失字词
    n_sent = random_remove_word(n_sent)

    return n_sent

def main():
    logger.info("loading data")
    with codecs.open(CORPUS, 'r', encoding='utf-8') as f:
        synonyms_dict = gen_synonyms_dict(CILIN)
        homophone_dict = gen_homophone_dict(HOMOPHONE_WORD)
        samepin_dict = gen_same_pin(SAMEPIN)

        logger.info("processing")
        ret = []
        for line in f:
            ret.append(line.strip())
            ret.append(sentence_process(line, synonyms_dict, homophone_dict, samepin_dict))

        logger.info("writing file")
        write_file(PROCESSED_CORPUS, ret)
    
if __name__ == '__main__':
    main()
