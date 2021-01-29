import random
import time
import multiprocessing
import codecs

from tools.tokenizer.wordCut import WordCut

BASIC_DIR = '../data/'

DATA_FILE = BASIC_DIR + 'proc_result.txt'
TRAIN_FILE = BASIC_DIR + 'intent_train.txt'
TEST_FILE = BASIC_DIR + 'intent_test.txt'

file_list = [BASIC_DIR + 'intent_train.txt', BASIC_DIR + 'intent_test.txt']
write_list = [BASIC_DIR + 'train_token.txt', BASIC_DIR + 'test_token.txt']


# index2type = {
#     "0":"遥感影像数据查询类",
#     "1":"航天运控查询类",
#     "2":"需求创建和录入",
#     "3":"需求搜索",
#     "4":"弹窗",
#     "5":"指令下达"
# }
# 导入数据 根据text_gen.txt 生成对应标签
def load_data():
    sent = []
    with codecs.open(DATA_FILE, encoding="utf-8") as f:
        for l in f.readlines():
            sent.append(l.strip())

    label = [0]*500*2 + [1]*600*2 + [2]*2200*2 + [3]*1050*2 + [4]*150*2 + [5]*300*2

    if len(sent) != len(label):
        raise ValueError("数据集错误")

    return sent, label


def write_file(filename, content):
    with codecs.open(filename, "w", encoding='utf-8') as f:
        for c in content:
            f.write(str(c) + '\n')

def construct_str(x):
    return str(x[0])+'\t'+str(x[1])

# 打乱sentences及label
def shuffle_data(sent, label):
    random.seed(0)
    random.shuffle(sent)
    random.seed(0)
    random.shuffle(label)

    return sent, label
    

# 切分训练集及测试集
def split_data(sent, label, tr=0.8):
    sp = int(len(label) * tr)
    trSent, trLabel = sent[:sp], label[:sp]
    tsSent, tsLabel = sent[sp:], label[sp:]

    return (trSent, trLabel), (tsSent, tsLabel)


# 分词
def token_file(file_path, write_path):
    word_divider = WordCut()
    with codecs.open(write_path, 'w', encoding='utf-8') as w:
        with codecs.open(file_path, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                label, sent = line.split('\t')
                sent = sent.strip()
                token_sen = word_divider.seg_sentence(sent)
                w.write(str(label) + '\t' + token_sen + '\n') 
    print(file_path + ' has been token and token_file_name is ' + write_path)


# 多线程分词
def get_tocken_file():
    pool = multiprocessing.Pool(processes=4)
    for file_path, write_path in zip(file_list, write_list):
        result = pool.apply_async(token_file, (file_path, write_path, ))
        result.get()
        # token_file(file_path, write_path)
    pool.close()
    pool.join() # 调用join()之前必须先调用close()
    print("Sub-process(es) done.")


def main():
    print(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))
    sent, label = load_data()
    sent, label = shuffle_data(sent, label)
    tr, ts = split_data(sent, label)
    write_file(TRAIN_FILE, map(construct_str, (zip(tr[1], tr[0]))))
    write_file(TEST_FILE, map(construct_str, (zip(ts[1], ts[0]))))
    print("dump ok")
    get_tocken_file()
    print(time.strftime("%Y-%m-%d %H-%M-%S", time.localtime()))

if __name__ == '__main__':
    main()
