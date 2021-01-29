import codecs
import random
import os
import numpy as np

BASE_DIR = './'
GEN_RES = BASE_DIR + 'txt_gen_gen_result.txt'
SOURCE = BASE_DIR + 'source_test_cropus.txt'

def gen_same_random_cropus(filename, writefile):
    with codecs.open(filename, 'r', encoding='utf-8') as f:
        corpus = []
        for line in f:
            # 生成数据时同时保留了原数据和处理后的数据 所以此处要添加两次
            corpus.append(line.strip())
            corpus.append(line.strip())

        random.seed(0)
        random.shuffle(corpus)
        with codecs.open(writefile, 'w', encoding='utf-8') as w:
            # 0.8 来自dataSplit.py/split_data/tr=0.8
            for c in corpus[int(len(corpus)*0.8):]:
                w.write(c + '\n')


# 打印预测结果矩阵 mat[i][j]=n 表示有n个样本标签为i预测结果为j
def get_err_matrix(label, pred, show=True):
    lab = set(label)
    mat = np.zeros([len(lab), len(lab)], dtype=np.int32)
    for l, p in zip(label, pred):
        mat[l][p] += 1

    # def print_mat(ls, st=''):
    #     print('\t'+st, end='')
    #     for x in ls:
    #         print('\t'+str(x), end='')
    #     print()

    # if show:
    #     print_mat(map(lambda x:'[{}]'.format(x),range(len(mat))))
    #     for i in range(len(mat)):
    #         print_mat(mat[i], st='[{}]'.format(i))
    if show:
        print(mat)

    return mat

# show_err: 仅展示错误分类结果
def compare_result(corpus, pred, label, show_err=False, out='compare_result.txt', source=SOURCE):
    if not os.path.exists(source):
        gen_same_random_cropus(GEN_RES, source)

    with codecs.open(source, 'r', encoding='utf-8') as f:
        with codecs.open(out, 'w', encoding='utf-8') as w:
            get_err_matrix(label, pred)
            for s, l, c, p in zip(f, label, corpus, pred):
                if show_err and l != p:
                    w.write(str(l)+'\t'+str(s.strip())+'\n')
                    w.write(str(p)+'\t'+str(c.replace(' ', '').strip())+'\n')
