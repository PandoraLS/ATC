import numpy as np

index2type = {
    "0":"遥感影像数据查询类",
    "1":"航天运控查询类",
    "2":"需求创建和录入",
    "3":"需求搜索",
    "4":"弹窗",
    "5":"指令下达"
}

# 1
dict_control = [ "编号", "快响", "下达"]

# 0
dict_query = ["查询", " 光谱", "分辨率", " 米", " 级", " 产品", " 光学"," 红外", " 全色", " 经度"," 维度"]

# 2
dict_create = ["创建", "事件",  "录入", "点目标", "经纬度", "东经", "北纬",  "西经", "南纬", "移动", "跟踪", "时长", "点录入"]

# 3
dict_search = [ "搜索",  "侦查" ]

# 4
dict_window = ["弹出", " 监视", " 窗口", " 汇集", " 管理", " 任务", " 规划", " 审核", " 分析", " 进程", " 监控", " 时效", " 综合", " 显示", "关闭", "打开"]

# 5
dict_cmd = [ "发布", "代号", "下发", "申请"]


dicts = [dict_query, dict_control, dict_create, dict_search, dict_window, dict_cmd]

def intent_classify(s):
    res = []
    for i in range(6):
        c = 0 
        for w in dicts[i]:
            if s.find(w)!=-1:
                c+=1
        res.append(c)
    n = np.argmax(res)+1
    return index2type(str(n))


TEST_FILE = 'tfidf/test_token.txt'


def load_test():
    pass



def main():
    pass
    


if __name__ == '__main__':
    main()
