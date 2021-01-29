import pickle
import torch
import re

from .dl.models.TextRCNN import Config, Model
from .dl.wordCut import WordCut
from .dl.utils import get_pred_query


class IntentTextRCNN():

    def __init__(self, params):
        dataset = params['IntentTextRCNN']['data_path']
        self.config = Config(dataset, 'random')

        # load vocab dict
        vocab_file = self.config.vocab_path
        self.vocab = pickle.load(open(vocab_file, 'rb'))
        self.config.n_vocab = len(self.vocab)

        # load textRCNN model
        self.model = Model(self.config).to(self.config.device)
        self.model.load_state_dict(torch.load(self.config.save_path))
        self.model.eval()

        # word cut tool
        self.word_divider = WordCut()

        self.id2type = {
            0: "高度的描述",
            1: "高度的改变、报告和升降率及TCAS指令",
            2: "管制移交及转换频率",
            3: "呼号的改变",
            4: "飞行活动通报",
            5: "气象情报",
            6: "位置报告",
            7: "附加报告",
            8: "机场情报",
            9: "助航设备工作状况"
        }

    def delete_punctuation(self, text):
        """
        去掉句子中任意地方的英文标点符号
        :param text: 句子
        :return: 
        """
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def replace_time(self, text):
        """
        正则表达式匹配所有的时间,并将其替换为<TIME>
        如果没有时间, 则不进行替换
        :param text: 
        :return: 替换后的文本
        """
        # date_all = re.findall(r"(\d{1,2}:\d{1,2})", text)
        return re.sub(r'(\d{1,2}:\d{1,2})', '<TIME>', text)

    def replace_num(self, text):
        """
        正则表达式匹配所有的数字并替换掉
        该程序在replace_time()之后运行
        # TODO 暂时不考虑小数
        :param text: 
        :return: 
        """
        return re.sub(r'(\d+)', '<NUM>', text)

    def intent_analyse(self, sentence):
        sentence = self.delete_punctuation(sentence)
        sentence = self.replace_time(sentence)
        sentence = self.replace_num(sentence)
        token = self.word_divider.seg_sentence(sentence).split(' ')
        query = get_pred_query(token, self.config, self.vocab)

        # call model's static method to get predict
        return self.model.predict(self.model, query, self.id2type)

