# -*- coding: utf-8 -*-
# @Time : 2020/12/23 下午1:03

import os
import sys
sys.path.append(os.path.join('..'))
from atc_intent_reconize.intents import IntentTextRCNN



class IntentModel:
    def __init__(self):
        param = {}
        param['IntentTextRCNN'] = {}
        param['IntentTextRCNN']['data_path'] = "atc_intent_reconize/dl/intent"
        self.model = IntentTextRCNN(param)

    def run(self, s: str) -> str:
        """
        意图识别
        :param s: 输入的语句
        :return:
        """
        result = self.model.intent_analyse(s)
        res_id, res_type = result           # res_id： 类别id,  res_type: 类别type描述
        return "类别ID: " + str(res_id) + "\n类别描述: " + str(res_type)



if __name__ == '__main__':
    model = IntentModel()
    output = model.run("IF NOT CONTACT REQUEST DEPARTURE INFORMATION")
    print(output)

