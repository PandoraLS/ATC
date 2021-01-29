import json
import re
import random
import math
lists = {
    1: "时间点", 2: "时间段", 3: "行政区域", 4: "国家区域", 5: "地理范围", 6: "卫星", 7: "载荷", 8: "分辨率", 9: "级别",
    10: "设备代号", 11: "站点",
    12: "事件", 13: "事件名称", 14: "目标名称", 15: "经纬度", 16: "目标库名称", 17: "跟踪时长", 18: "跟踪目标",
    19: "弹窗指令", 20: "窗口名称", 21: "指令", 22: "指令编号"
}
tag_lists = {
    1:"TIME",2:"TIMED",3:"ADMIN_AREA",4:"COUNTRY_AREA",5:"GEOGRAPHY_AREA",6:"SATELLITE",7:"LOAD",
    8:"RESOLUTION",9:"LEVEL",10:"CODE",11:"SITE",12:"EVENT",13:"EVENT_NAME",14:"TARGET_NAME",15:"LATITUDE",
    16:"TARGET_RESPO",17:"TRACE_TIME",18:"TRACE_TARGET",19:"WINDOWS_COMMAND",20:"WINDOWS_NAME",
    21:"INSTRACT",22:"INSTRACT_NUM"
}
base_sentences = json.load(open("sentence.json", mode="r", encoding="utf-8"))
short_sentences = json.load(open("short_sentence.json",mode='r',encoding='utf-8'))

print()
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
            if 0< start and start < 1:
                value = float(random.randint(math.ceil(start),end*10))/10
            else:
                value = random.randint(start,end)
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
    lists = {
        "0":"零",
        "1":"一",
        "2":"二",
        "3":"三",
        "4":"四",
        "5":"五",
        "6":"六",
        "7":"七",
        "8":"八",
        "9":"九",
        "10":"十"
    }
    hanzi = ""
    if num - math.ceil(num) != 0: # 小数
        integer = math.floor(num)
        hanzi_integer = num2hanzi(integer)
        re_str = r"[\d]+\.([\d]+)"
        hanzi_decimal = ""
        for match in re.finditer(re_str,str(num)):
            for char in match.group(1):
                hanzi_decimal += lists[char]
        hanzi_decimal = "点" + hanzi_decimal
        hanzi = hanzi_integer+hanzi_decimal
    else:
        if num<=10 and num >=0:
            hanzi = lists[str(num)[0]]
        elif num > 10 and num < 100:
            shiwei = lists[str(num)[0]]
            if str(num)[0]=='1':
                shiwei = ""
            if str(num)[1] == '0':
                gewei = ''
            else:
                gewei = lists[str(num)[1]]
            hanzi = shiwei+"十"+gewei
        elif num<1000 and num>=100:
            gewei = ''
            baiwei = lists[str(num)[0]] + "百"
            if str(num)[2] == '0':
                if str(num)[1] == '0':
                    shiwei = ""
                else:
                    shiwei = lists[str(num)[1]] + "十"
            else:
                gewei = lists[str(num)[2]]
                if str(num)[1] == '0':
                    shiwei = lists[str(num)[1]]
                else:
                    shiwei = lists[str(num)[1]] + "十"
            hanzi = baiwei + shiwei + gewei
        else:
            for char in str(num):
                hanzi +=lists[char]
    return hanzi

def num2hanzi_simple(sentence):
    '''
    简单的处理数字转汉字
    :param sentence:
    :return:
    '''
    lists = {
        "0":"零",
        "1":"一",
        "2":"二",
        "3":"三",
        "4":"四",
        "5":"五",
        "6":"六",
        "7":"七",
        "8":"八",
        "9":"九",
        "10":"十"
    }
    for c in sentence:
        if c in lists.keys():
            sentence = re.sub(c,lists[c],sentence,count=1)
    return sentence

sentences = []
train_sentences = []
for key,value in base_sentences.items():
    moban = key
    moban_count = value['count'] * 5
    short_type = value['index']
    moban_position = list(short_type.keys())
    moban_position.sort()
    for i in range(moban_count):
        temp_dict = dict()
        sentence =moban
        init_end_index = sentence.index('#')
        temp_dict['word'] = []
        temp_dict['tag'] = []
        # for j in range(init_end_index):
        #     temp_dict['word'].append(sentence[j])
        #     temp_dict['tag'].append('O')
        prev_idx = 0
        for index in moban_position:
            re_str = '#'+index+'#'
            start_index = sentence.index('#')
            # 当前槽前面的非槽字符
            for j in range(prev_idx, start_index):
                temp_dict['word'].append(sentence[j])
                temp_dict['tag'].append('O')
            short_value_lists = short_type[index]
            short_sentence,type = get_rand_short(short_value_lists) # type表示短语类别
            short_sentence = num2hanzi_simple(short_sentence) # 将所有数字转成汉字
            sentence = re.sub(re_str,short_sentence,string=sentence,count=1)
            end_index = len(short_sentence)+start_index-1
            prev_idx = end_index+1
            temp_dict['word'].append(sentence[start_index])
            temp_dict['tag'].append('B-' + tag_lists[type])
            for j in range(start_index+1,end_index):
                temp_dict['word'].append(sentence[j])
                temp_dict['tag'].append('I-'+tag_lists[type])
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
train_datasets = train_sentences[:int(8*len(train_sentences)/10)]
test_datasets = train_sentences[int(8*len(train_sentences)/10):int(9*len(train_sentences)/10)]
dev_datasets = train_sentences[int(9*len(train_sentences)/10):]
train_file = "train.char.bmes"
test_file = "test.char.bmes"
dev_file = "dev.char.bmes"
f_train = open(train_file,mode='w',encoding='utf-8')
f_test = open(test_file,mode='w',encoding='utf-8')
f_dev = open(dev_file,mode='w',encoding='utf-8')
for f, d in zip([f_dev,f_test,f_train], [dev_datasets, test_datasets, train_datasets]):
    for item in d:
        words = item['word']
        entitys = item['tag']
        for word,entity in zip(words,entitys):
            f.write(word+' '+entity+'\n')
        f.write('\n')

with open("gen_result.txt",'w',encoding='utf-8') as f:
    for s in sentences:
        f.write(s+'\n')
