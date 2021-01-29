# coding: UTF-8
import time
import pickle as pkl
import torch
import numpy as np
from train_eval import train, test, init_network
from importlib import import_module
from utils import get_pred_query
import argparse

from wordCut import WordCut

parser = argparse.ArgumentParser(description='Chinese Text Classification')
parser.add_argument('--model', default='TextRCNN', type=str, help='choose a model: TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer')
# parser.add_argument('--embedding', default='pre_trained', type=str, help='random or pre_trained')
parser.add_argument('--embedding', default='random', type=str, help='random or pre_trained')
parser.add_argument('--word', default=True, type=bool, help='True for word, False for char')
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


if __name__ == '__main__':
    dataset = 'intent'  # 数据集

    # 搜狗新闻:embedding_SougouNews.npz, 腾讯:embedding_Tencent.npz, 随机初始化:random
    embedding = 'embedding_SougouNews.npz'
    if args.embedding == 'random':
        embedding = 'random'
    model_name = args.model  # 'TextRCNN'  # TextCNN, TextRNN, FastText, TextRCNN, TextRNN_Att, DPCNN, Transformer
    if model_name == 'FastText':
        from utils_fasttext import build_dataset, build_iterator, get_time_dif
        embedding = 'random'
    else:
        from utils import build_dataset, build_iterator, get_time_dif

    x = import_module('models.' + model_name)
    # 构建一个x.Config对象
    config = x.Config(dataset, embedding)
    # np.random.seed(1)
    # torch.manual_seed(1)
    # torch.cuda.manual_seed_all(1)
    # torch.backends.cudnn.deterministic = True  # 保证每次结果一样

    start_time = time.time()
    print("Loading data...")
    vocab, train_data, dev_data, test_data = build_dataset(config, args.word)
    train_iter = build_iterator(train_data, config)
    dev_iter = build_iterator(dev_data, config)
    test_iter = build_iterator(test_data, config)
    time_dif = get_time_dif(start_time)
    print("Time usage:", time_dif)

    # train
    config.n_vocab = len(vocab)
    model = x.Model(config).to(config.device)
    if model_name != 'Transformer':
        init_network(model)
    print(model.parameters)
    if not args.test and not args.predict:
        # print("Loading data...")
        # vocab, train_data, dev_data, test_data = build_dataset(config, args.word)
        # train_iter = build_iterator(train_data, config)
        # dev_iter = build_iterator(dev_data, config)
        # time_dif = get_time_dif(start_time)
        # print("Time usage:", time_dif)

        # config.n_vocab = len(vocab)
        # model = x.Model(config).to(config.device)
        # if model_name != 'Transformer':
        #     init_network(model)
        # print(model.parameters)

        train(config, model, train_iter, dev_iter, test_iter)
        time_dif = get_time_dif(start_time)
        print('total time cost: ', time_dif)
    elif not args.predict:
        # print("Loading data...")
        # vocab, train_data, dev_data, test_data = build_dataset(config, args.word)
        # test_iter = build_iterator(test_data, config)
        # time_dif = get_time_dif(start_time)
        # print("Time usage:", time_dif)

        # config.n_vocab = len(vocab)
        # model = x.Model(config).to(config.device)
        # if model_name != 'Transformer':
        #     init_network(model)
        # print(model.parameters)

        test(config, model, test_iter)
        time_dif = get_time_dif(start_time)
        print('total time cost: ', time_dif)
    else:
        print('loading ...')
        word_divider = WordCut()

        vocab = pkl.load(open(config.vocab_path, 'rb'))
        config.n_vocab = len(vocab)
        model = x.Model(config).to(config.device)
        model.load_state_dict(torch.load(config.save_path))
        model.eval()

        print('type exit for exit')
        while True:
            query = input('[in]: ')
            if query == 'exit':
                break
            else:
                token = word_divider.seg_sentence(query).split(' ')
                query = get_pred_query(token, config, vocab)
                outputs = model(query)
                predic = torch.max(outputs.data, 1)[1].cpu().numpy()
                print('[out]: type id is [%d], type name is [%s]' % (predic[0], id2type[predic[0]]))

    print('exit...')
