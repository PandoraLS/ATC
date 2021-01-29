import pickle
import codecs
import sys
import time
from datetime import timedelta
import argparse

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier 
from sklearn.metrics import classification_report
from sklearn.externals import joblib
from sklearn.metrics import accuracy_score

sys.path.append('../data')
from tool import compare_result
from tools.tokenizer.wordCut import WordCut

parser = argparse.ArgumentParser(description='tfidf based intent recognize')
parser.add_argument('--model', type=str, required=True, help='choose a model: logistic, randomforest')
parser.add_argument('-t', '--test', action='store_true', help='train or test')
parser.add_argument('-p', '--predict', action='store_true', help='predict model')
args = parser.parse_args()


id2type = {
    0:"遥感影像数据查询类",
    1:"航天运控查询类",
    2:"需求创建和录入",
    3:"需求搜索",
    4:"弹窗",
    5:"指令下达"
}


class Config():
    """model parameter config"""
    def __init__(self, model_name):
        self.model_name = model_name

        self.data_dir = '../data/'
        self.train_token = self.data_dir + 'train_token.txt'
        self.test_token = self.data_dir + 'test_token.txt'

        self.feature_path = 'feature/tfidf.vec.pkl'
        self.save_path = model_name + '/' + self.model_name + '.ckpt'
        self.log_path = model_name + '/' + self.model_name + '.out.txt'

        self.start_time = time.time()

    def get_time_diff(self):
        """获取已使用时间"""
        end_time = time.time()
        time_diff = end_time - self.start_time
        dt = timedelta(seconds=int(round(time_diff)))
        print('time cost: ', dt)
        return 


class ModelFactory():
    def get_model(self, model_name):
        if model_name == 'logistic':
            return LogisticRegression()
        elif model_name == 'randomforest':
            return RandomForestClassifier()
        else:
            raise ValueError('no such model name, please choose model: logistic, randomforest')
        


# 读取分词后的数据集
def constructDataset(path):
    """
    path: file path
    rtype: lable_list and corpus_list
    """
    label_list = []
    corpus_list = []
    with codecs.open(path, 'r', encoding='utf-8') as p:
        for line in p.readlines():
            label, corpus = line.split('\t')
            label_list.append(int(label))
            corpus_list.append(corpus)
    return label_list, corpus_list


# 计算tf-idf特征
def calTFIDF(config, corpus_set, is_train=True):
    if is_train:
        vectorizer = TfidfVectorizer(min_df=1e-5) # drop df < 1e-5,去低频词
        tfidf = vectorizer.fit_transform(corpus_set)
        words = vectorizer.get_feature_names()
        print("how many words: {0}".format(len(words)))
        print("tf-idf shape: ({0},{1})".format(tfidf.shape[0], tfidf.shape[1]))
        joblib.dump(vectorizer, config.feature_path)
        return tfidf
    else:
        try:
            vectorizer = joblib.load(config.feature_path)
        except FileNotFoundError as e:
            print('[error] no pretrained model, try: python3 --model ' + config.model_name)
            exit(0)
        tfidf = vectorizer.transform(corpus_set)
        words = vectorizer.get_feature_names()
        print("how many words: {0}".format(len(words)))
        print("tf-idf shape: ({0},{1})".format(tfidf.shape[0], tfidf.shape[1]))
        return tfidf


def train(config, train_corpus, train_label, val_corpus, val_label):
    TRAIN_SIZE = len(train_label)
    print("length of corpus is: " + str(TRAIN_SIZE))
    tfidf = calTFIDF(config, train_corpus)
    val = calTFIDF(config, val_corpus, is_train=False)

    print('current model: ', config.model_name)
    model = ModelFactory().get_model(config.model_name)
    model.fit(tfidf, train_label)
    y_pred = model.predict(tfidf)
    print("train acc: {0}".format(accuracy_score(train_label, y_pred)))
    print("val mean accuracy: {0}".format(model.score(val, val_label)))
    joblib.dump(model, config.save_path)

    config.get_time_diff()


def test(config, test_corpus, test_label):
    TEST_SIZE = len(test_label)
    print("length of corpus is: " + str(TEST_SIZE))
    tfidf = calTFIDF(config, test_corpus, is_train=False)

    print('current model: ', config.model_name)
    model = joblib.load(config.save_path)
    y_pred = model.predict(tfidf)
    print("test accuracy: {0}".format(accuracy_score(test_label, y_pred)))
    print(classification_report(test_label, y_pred))
    compare_result(test_corpus, y_pred, test_label, show_err=True, out=config.log_path)

    config.get_time_diff()


def main():
    config = Config(args.model)

    # 出现-p则进入在线预测模式
    # 否则出现-t运行模式测试
    # 否则训练模型
    if not args.test and not args.predict:
        # 获取数据集
        train_label, train_corpus = constructDataset(config.train_token)
        test_label, test_corpus = constructDataset(config.test_token)
        train(config, train_corpus, train_label, test_corpus, test_label)
    elif not args.predict:
        test_label, test_corpus = constructDataset(config.test_token)
        test(config, test_corpus, test_label)
    else:
        print('loading ...')
        try:
            vectorizer = joblib.load(config.feature_path)
            model = joblib.load(config.save_path)
            word_divider = WordCut()
        except FileNotFoundError as e:
            print('[error] no pretrained model, try: python3 --model ' + config.model_name)
            exit(0)


        print('type exit for exit')
        while True:
            query = input('[in]: ')
            if query == 'exit':
                break
            else:
                tfidf = vectorizer.transform([word_divider.seg_sentence(query)])
                # print(tfidf)
                y_pred = model.predict(tfidf)
                print('[out]: type id is [%d], type name is [%s]' % (y_pred[0], id2type[y_pred[0]]))



if __name__ == '__main__':
    main()
