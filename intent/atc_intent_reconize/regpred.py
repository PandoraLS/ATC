# coding=utf-8
"""
针对需求创建示例，使用正则表达式提取槽位字符串。

语料示例：“需求创建，事件：应急任务-20190827，名称：目标测试，（时间：今天）。”

需求创建示例分析：
“需求创建，事件”，“名称”，“时间”是关键字符串，且有一定顺序。
“创建”是重点关键词，是其他指令没有的。
"""



import re

# 遥感影像数据查询类  √
# 查询 四川省 2019年10月份 高分1号 全色 分辨率优于1米 1级产品 的数据
# TODO:地域,时间,卫星,载荷,分辨率,级别
mode1_1 = r'请?查询(.+)(二.+(?:月份?|日))?(.+号|.+星)?(全色|多光谱|高光谱|红外)?(分辨率.+米)?(.+级产品)?的数据'
test1_1 = ['查询长江流域二零一九年十月三十日高分一号A星全色分辨率优于一米一级产品的数据',
           '查询内蒙古自治呼和浩特市二零一一年第四季ZY三全色分辨率为四米四级产品的数据',
           '查询左上角三十度五十七分五秒一十度五十三分二十秒右下角九十四度五十五分二十一秒二十三度一十二分八秒二零零八年上半年高分五号高光谱分辨率为八米五级产品的数据',
           '']

# (请)查询 [地点] [时间] 的 [条件] 的数据
# TODO:地点,时间,条件
mode1_2 = r'请?查询(.+)(二.+)的(.+)的.*数据'
test1_2 = '请查询朝鲜半岛二零一九年十月份的分辨率优于一米的数据'

# 航天运控查询类 √
# 查询[设备代号]设备状态
# TODO：设备代号
mode2_1 = r'.*查询(.+)设备.*状.*态'
# 发布设备代号为[设备代号]窗口
mode2_2 = r'.*发布.*设备.*代号.*为(.+)窗口'
# 下发设备代号为[设备代号]任务
mode2_3 = r'.*下发.*设备.*代号.*为(.+)任务'
# 申请[站点]的资源
mode2_4 = r'.*申请(.+)的.*资源'
test2 = ['查询ZY一二三一设备状态', '发布机器设备的代号为ZY一二三一窗口',
         '下发设备代号为ZY一二三一任务', '申请北京站的资源']

# 需求创建和录入 √
# 1.需求创建
# 需求创建，事件：应急任务-20190827，名称：目标测试。
# 需求创建，事件：应急任务-20190827，名称：目标测试，时间：今天。
# TODO：事件,名称,时间
mode3_1 = r'.*需求.*创建.*事件(.+)名称(.+)时间(.*)'
# TODO：事件,名称
mode3_2 = r'.*需求.*创建.*事件(.+)名称(.+)'
test3_12 = ['需求创建事件应急任务-二零一九零八二七名称目标测试',
         '需求创建事件应急任务-二零一九零八二七名称目标测试时间今天']

# 2.需求录入
# (1)点需求
# TODO:名称,经纬度1
# 点录入，名称：点目标1，经纬度：东经120.25度，北纬5.38度。
# 点需求录入，名称：点目标1，经纬度：东经120.25，北纬5.38。
mode3_3 = r'.*点(?:需求)?.*录入.*名称(.+)经纬度(.+)'
test3_3 = ['点录入名称点目标一经纬度东经一百二十点二五度北纬五点三八度',
           '点需求录入名称点目标一经纬度东经一百二十点二五度北纬五点三八度']

# (2)区域需求
# TODO:名称,经纬度1,经纬度2
# 区域需求录入，名称：区域目标1，左上角经纬度：东经120.25度，北纬5.38度，右下角经纬度：东经135.45度，南纬10.56度。
# 区域录入，名称：区域目标1，左上角经纬度：东经120.25度，北纬5.38度，右下角经纬度：东经135.45度，南纬10.56度。
# 区域需求录入，名称：区域目标1，左上角：东经120.25度，北纬5.38度，右下角：东经135.45度，南纬10.56度。
mode3_4 = r'.*区域.*(?:需求)?.*录入.*名称(.+)左.*上角(?:经纬度)?(.+)右.*下角(?:经纬度)?(.+)'
test3_4 = ['区域需求录入名称区域目标一左上角经纬度东经一百二十点二五度北纬五点三八度右下角经纬度东经一百三十五点四五度南纬十点五六度',
           '区域录入名称区域目标一左上角经纬度东经一百二十点二五度北纬五点三八度右下角经纬度东经一百三十五点四五度南纬十点五六度',
           '区域需求录入名称区域目标一左上角东经一百二十点二五度北纬五点三八度右下角东经一百三十五点四五度南纬十点五六度']
# (3)移动目标需求
# TODO:时长,目标
# 移动目标需求录入，跟踪时长：8，目标：CVN76里根号。
# 移动目标录入，跟踪时长：8，目标：CVN76里根号。
mode3_5 = r'.*移动目标.*(?:需求)?.*录入.*跟踪.*时长*(.+点?.*).*目标(.+)'
test3_5 = ['移动目标需求录入跟踪时长八目标CVN七六里根号',
         '移动目标录入跟踪时长十五点八目标CVN七六里根号']

# (4)目标需求
# TODO:目标
# 目标需求录入，目标：中国-北京首都机场。
# 目标库录入，目标：中国-北京首都机场。
# 目标库需求录入，中国-北京首都机场。
mode3_6 = r'目标.*(?:需求|库|库需求)?.*录入(?:目标)?(.+)'
test3_6 = ['目标需求录入目标中国-北京首都机场',
         '目标库录入目标中国-北京首都机场',
         '目标库需求录入中国-北京首都机场']
# 搜索
# (1)需求搜索
# TODO:名称
# 需求搜索，名称：区域153。
# 需求搜索，区域153。
# (2)侦查目标
# 侦察目标搜索，名称：目标1。
# 侦察目标搜索，目标1。
# (3)资源搜索
# 资源搜索，名称：卫星001。
# 资源名称搜索，卫星001。
# 资源名称搜索，名称：卫星001。
mode4 = r'.*(?:需求|侦察?查?.*目标|资源(?:名称)*).*搜索(?:名称)?(.+)'
test4 = ['需求搜索名称区域一五三', '需求搜索区域一五三',
           '侦察目标搜索名称目标零零一', '侦察目标搜索目标一',
           '资源搜索名称卫星零零一', '资源名称搜索卫星零零一',
           '资源名称搜索名称卫星零零一', '侦察目标搜索名称目标四一九']

# 弹窗
# TODO:动作,名称
# 弹出 资源状态监视窗口。
mode5 = r'(查询|弹出|关闭|打开)(资源.*状态.*监视|需求.*汇集.*管理|应急.*任务.*规划|计划.*审核.*分析|任务.*进程.*监控|任务.*时效.*分析|.*综合.*显示.*管理|服务.*日志.*管理)窗口'
test5 = ['查询需求汇集管理窗口', '弹出应急任务规划窗口', '关闭计划审核分析窗口']


# 指令下达
# TODO:动作,指令编号(三位数字)  ??编号是中文还是数字
# 下达212编号的应急快响计划
# 下达编号为212的应急快响计划
mode6_1 = r'(下达|执行)(.+)编号的应急快响计划'
mode6_2 = r'(下达|执行)编号为?(.+)的应急快响计划'
test6 = ['下达二一二编号的应急快响计划', '下达编号为二一二的应急快响计划']


str_commands = ['mode1_1', 'mode1_2', 'mode2_1', 'mode2_2', 'mode2_3', 'mode2_4',
                'mode3_1', 'mode3_2', 'mode3_3', 'mode3_4', 'mode3_5', 'mode3_6',
                'mode4', 'mode5', 'mode6_1', 'mode6_2']
index2type = {
    "1":"遥感影像数据查询类","2":"航天运控查询类","3":"需求创建和录入","4":"需求搜索","5":"弹窗","6":"指令下达"
}
commands = [mode1_1, mode1_2, mode2_1, mode2_2, mode2_3, mode2_4, mode3_1, mode3_2, mode3_3, mode3_4, mode3_5, mode3_6,
            mode4, mode5, mode6_1, mode6_2]


# modex_x对应哪种情况(一共七种)
def sort_dict(str_commands):
    s_dict = {}
    for i in range(len(str_commands)):
        n = str_commands[i][4]
        s_dict[str_commands[i]] = n
    return s_dict


# modex_x的具体值
def value_dict(commands, str_commands):
    v_dict = {}
    for i in range(len(str_commands)):
        v_dict[str_commands[i]] = commands[i]
    return v_dict


# modex_x对应的实体类型
def entity_dict():
    e_dict = {}
    e_dict['mode1_1'] = ['地域', '时间', '卫星', '载荷', '分辨率', '级别']
    e_dict['mode1_2'] = ['地域', '时间', '数据']
    e_dict['mode2_1'] = ['设备代号']
    e_dict['mode2_2'] = ['设备代号']
    e_dict['mode2_3'] = ['设备代号']
    e_dict['mode2_4'] = ['站点']
    e_dict['mode3_1'] = ['事件', '名称', '时间']
    e_dict['mode3_2'] = ['事件', '名称']
    e_dict['mode3_3'] = ['名称', '经纬度1']
    e_dict['mode3_4'] = ['名称', '经纬度1', '经纬度2']
    e_dict['mode3_5'] = ['时长', '目标']
    e_dict['mode3_6'] = ['目标']
    e_dict['mode4'] = ['名称']
    e_dict['mode5'] = ['动作', '名称']
    e_dict['mode6_1'] = ['动作', '指令编号']
    e_dict['mode6_2'] = ['动作', '指令编号']
    return e_dict


# 找到命令对应的具体值和分类
def find_sort_value(input_str, value_dict, sort_dict):
    res = []
    s = ''
    v = ''
    for v in value_dict.keys():
        # print(value_dict[v])
        res = re.findall(value_dict[v], input_str)
        if res != []:
            s = sort_dict[v]
            return res, s, v
    return res, s, v


# res：识别出的实体们
# value：'modex_x'
def gene_dic(res, value, entity_dict):
    dict = {}
    entity = entity_dict[value]
    l = len(entity)
    for i in range(len(entity)):
        # dict[entity[i]] = res[0][i]
        e_i = entity[i]
        if l>1:
            r_i = res[0][i]
        else:
            r_i = res[0]
        dict[e_i] = r_i
    return dict


test = [
    '查询长江流域二零一九年十月三十日高分一号A星全色分辨率优于一米一级产品的数据',
    '请查询朝鲜半岛二零一九年十月份的分辨率优于一米的数据',
    '查询ZY一二三一设备状态',
    '发布机器设备的代号为ZY一二三一窗口',
    '下发设备代号为ZY一二三一任务',
    '申请北京站的资源',
    '需求创建事件应急任务-二零一九零八二七名称目标测试',
    '需求创建事件应急任务-二零一九零八二七名称目标测试时间今天'
    '点录入名称点目标一经纬度东经一百二十点二五度北纬五点三八度',
    '点需求录入名称点目标一经纬度东经一百二十点二五度北纬五点三八度',
    '区域需求录入名称区域目标一左上角经纬度东经一百二十点二五度北纬五点三八度右下角经纬度东经一百三十五点四五度南纬十点五六度',
    '区域录入名称区域目标一左上角经纬度东经一百二十点二五度北纬五点三八度右下角经纬度东经一百三十五点四五度南纬十点五六度',
    '区域需求录入名称区域目标一左上角东经一百二十点二五度北纬五点三八度右下角东经一百三十五点四五度南纬十点五六度',
    '目标需求录入目标中国-北京首都机场',
    '目标库录入目标中国-北京首都机场',
    '目标库需求录入中国-北京首都机场',
    '移动目标需求录入跟踪时长八目标CVN七六里根号',
    '移动目标录入跟踪时长十五点八目标CVN七六里根号',
    '需求搜索名称区域一五三',
    '需求搜索区域一五三',
    '侦察目标搜索名称目标一',
    '侦察目标搜索目标一',
    '资源搜索名称卫星零零一',
    '资源名称搜索卫星零零一',
    '资源名称搜索名称卫星零零一',
    '查询需求汇集管理窗口',
    '弹出应急任务规划窗口',
    '关闭计划审核分析窗口',
    '下达二一二编号的应急快响计划',
    '下达编号为二一二的应急快响计划',
    '需求创建事件森林大火名称二一二'
]


def regular(sentence):
    s_dict = sort_dict(str_commands)
    v_dict = value_dict(commands, str_commands)
    e_dict = entity_dict()
    res, s, v = find_sort_value(sentence, v_dict, s_dict)
    dict = {}
    if res == []:
        print("no match", sentence)
    else:
        dict = gene_dic(res, v, e_dict)
    # s：str型,第几类命令
    # dict：实体字典
    if s == '':
        type = "未知"
    else:
        type = index2type[s]
    return type, dict

test_lists =[
    "申请北京站的资源"
]
for s in test:
    s, dict = regular(s)
    print(s, "th type of command", "dict", dict)

"""
暂时只考虑了可能多字的情况。
需要根据识别结果再进行调整
"""
