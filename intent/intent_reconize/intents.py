import pickle
import torch

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
            0:"遥感影像数据查询类",
            1:"航天运控查询类",
            2:"需求创建和录入",
            3:"需求搜索",
            4:"弹窗",
            5:"指令下达"
        }
        

    def intent_analyse(self, sentence):

        token = self.word_divider.seg_sentence(sentence).split(' ')
        query = get_pred_query(token, self.config, self.vocab)

        # call model's static method to get predict
        return self.model.predict(self.model, query, self.id2type)

