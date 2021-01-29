# 意图识别方法汇总

```
.
├── dictpred.py
├── dl
│   ├── intent
│   │   ├── data
│   │   │   ├── class.txt                   # 类别ID
│   │   │   ├── dev.txt                     # 验证集
│   │   │   ├── read_pkl.py                 # 辅助读取pkl文件
│   │   │   ├── test.txt                    # 测试集
│   │   │   ├── train.txt                   # 训练集
│   │   │   └── vocab.pkl                   # 词表
│   │   └── saved_dict                      
│   │       └── TextRCNN.ckpt               # 训练保存的模型
│   ├── models                              # 各种神经网络模型
│   │   ├── DPCNN.py
│   │   ├── FastText.py
│   │   ├── TextCNN.py
│   │   ├── TextRCNN.py
│   │   ├── TextRNN_Att.py
│   │   ├── TextRNN.py
│   │   └── Transformer.py
│   ├── README.md
│   ├── run.py
│   ├── stopwords.txt                       # 停用词
│   ├── train_eval.py                       # 训练与验证
│   ├── utils_fasttext.py                   # 辅助代码
│   ├── utils.py                            # 辅助代码
│   └── wordCut.py                          # 辅助代码
├── intents.py
├── intents_util.py
├── README.md
└── regpred.py
```

## 数据处理

数据来源：

>  http://211.83.111.189:10086/chenc/ner/blob/master/txt_gen/gen_result.txt 

数据处理方式：

0. 对数据进行同音同义词替换预处理。方法见`./同音同义词/README.md`
1. 将原始数据与同音同义预处理之后的数据拼接，扩充数据集
2. 根据指令数据与其模式的对应关系手动生成标签数据
3. 同规则随机打乱指令数据及其模式标签
4. 根据8:2的方式将数据集切分成训练集与测试集
5. 分词

## 意图识别方法

### 基于词典的意图识别方法

针对六种意图，各提取了一些关键词，对输入的句子进行匹配，取关键词最符合的一项作为结果。

### 基于正则匹配的意图识别方法

制定正则表达式匹配输入语句，取第一个成功匹配的规则对应的意图作为结果。

### 基于机器学习的意图识别方法

1. 读取数据
2. 利用训练数据，使用tf-idf生成特征向量
3. 使用机器学习算法进行分类预测
   * 逻辑回归
   
     ```python
     # 进入 /tfidf 目录
     # 训练
     python tfidf.py --model logistic
     # 测试
     python tfidf.py --model logistic -t
     # 预测
     python tfidf.py --model logistic -p
     ```
     
   * 随机森林
   
     ```python
     # 进入 /tfidf 目录
     # 训练
     python tfidf.py --model randomforest
     # 测试
     python tfidf.py --model randomforest -t
     # 预测
     python tfidf.py --model randomforest -p
     ```
4. 利用测试数据，使用tf-idf生成特征向量，进行模型测试

### 基于深度学习的意图识别方法

#### TextCNN

**模型**

1. 随机embedding，数据padding，length=32
2. 一维卷积，relu激活，最大池化，拼接
3. dropout
4. 全连接映射

**运行**

```python
# 进入 /Chinese-Text-Classification-Pytorch 目录
# 训练
python run.py --model TextCNN
# 测试
python run.py --model TextCNN -t
# 预测
python run.py --model TextCNN -p
```

#### TextRNN

**模型**

1. 随机embedding，数据padding，length=32
2. 双向LSTM
3. 全连接

**运行**

```python
# 进入 /Chinese-Text-Classification-Pytorch 目录
# 训练
python run.py --model TextRNN
# 测试
python run.py --model TextRNN -t
# 预测
python run.py --model TextRNN -p
```

#### TextRNN_Att

**模型**

1. 随机embedding，数据padding，length=32
2. 双向LSTM
3. Tanh+softmax = α
4. 对RNN隐状态使用α加权
5. 连续两个全连接

**运行**

```python
# 进入 /Chinese-Text-Classification-Pytorch 目录
# 训练
python run.py --model TextRNN_Att
# 测试
python run.py --model TextCNN_Att -t
# 预测
python run.py --model TextCNN_Att -p
```

#### TextRCNN

**模型**

1. 随机embedding，数据padding，length=32

2. 双向LSTM

3. concat(input，隐状态)，relu激活

   >  双向LSTM每一时刻的隐层值(前向+后向)都可以表示当前词的前向和后向语义信息，将隐藏值与embedding值拼接来表示一个词 

4. reduceMax(axis=1)，相当于maxpool

5. 全连接

> 代码实现与原文略有不同。原文双向RNN每个状态由**前(后)一个状态和前(后)一个输入**共同生成。而传统RNN则是**前(后)一个状态和当前输入**共同生成。故在原文中存在第三步，将输入与RNN的隐状态进行拼接的操作。

**运行**

```python
# 进入 /Chinese-Text-Classification-Pytorch 目录
# 训练
python run.py --model TextRCNN
# 测试
python run.py --model TextRCNN -t
# 预测
python run.py --model TextRCNN -p
```

#### DPCNN

**模型**

1. 随机embedding，数据padding，length=32
2. 多层卷积池化
3. 全连接

**运行**

```python
# 进入 /Chinese-Text-Classification-Pytorch 目录
# 训练
python run.py --model DPCNN
# 测试
python run.py --model DPCNN -t
# 预测
python run.py --model DPCNN -p
```

## 结果

### 模型效果

> 此处准确率仅代表测试集上的准确率。
>
> 对于准确率均值、准确率方差、训练用时、预测用时均采用5次训练的结果计算得出。完整记录见[附录1](#附录1)
>
> 平均准确率反映模型的效能。准确率方差反映模型稳定性。
>
> 对模型名后[A]，A表示同模型使用不同特征、噪音配置，具体配置见[模型说明](#模型说明)
>
> 测试环境：CPU：六核 i5-8400 2.80GHz，内存：，GPU：GTX 1060，显存：6GB，编程语言：Pytorch。

| 模型                    | 准确率均值 | 准确率方差 | 平均训练用时 | 平均预测用时 |
| ----------------------- | ---------- | ---------- | ------------ | ------------ |
| logistic regression [1] | 96.41%     | -          | 0            | 0            |
| Random Forest [1]       | 95.77%     | 0.1633     | 1            | 0            |
| TextCNN [1]             | 97.83%     | 0.1010     | 6.4          | 1            |
| TextRNN [1]             | 94.40%     | 0.9184     | 17.4         | 1.6          |
| TextRNN_Att [1]         | 97.26%     | 0.1902     | 17           | 1.8          |
| TextRCNN [1]            | 97.64%     | 0.1143     | 10.8         | 2            |
| DPCNN [1]               | 97.55%     | 0.0394     | 9            | 1.6          |



## 附录1 训练结果记录表

模型多次训练结果完整记录表：

> 对模型名后[A]，A表示同模型使用不同特征、噪音配置，具体配置见[模型说明](#模型说明)
>
> 由于逻辑斯蒂回顾模型无随机参数，所以多次训练结果固定，只记录一次训练结果

| 模型名称                | 训练准确率 | 测试准确率 | 训练用时 | 测试用时 |
| ----------------------- | ---------- | ---------- | -------- | -------- |
| logistic regression [1] | 98.41%     | 96.41%     | 0        | 0        |
| random forest [1]       | 99.95%     | 95.63%     | 1        | 0        |
|                         | 99.96%     | 96.25%     | 1        | 0        |
|                         | 99.95%     | 96.25%     | 0        | 0        |
|                         | 99.90%     | 95.36%     | 0        | 0        |
|                         | 99.91%     | 95.36%     | 0        | 0        |
| Text CNN [1]            | 100%       | 97.76%     | 7        | 1        |
|                         | 100%       | 97.50%     | 6        | 1        |
|                         | 100%       | 97.50%     | 6        | 1        |
|                         | 100%       | 98.18%     | 7        | 1        |
|                         | 100%       | 98.23%     | 7        | 1        |
| Text RNN [1]            | 100%       | 95.31%     | 17       | 2        |
|                         | 99.22%     | 94.74%     | 17       | 1        |
|                         | 100%       | 94.84%     | 18       | 2        |
|                         | 98.44%     | 92.55%     | 18       | 2        |
|                         | 100%       | 94.58%     | 17       | 1        |
| Text RNN_Att [1]        | 100%       | 96.46%     | 17       | 2        |
|                         | 100%       | 97.55%     | 17       | 2        |
|                         | 100%       | 97.71%     | 17       | 2        |
|                         | 100%       | 97.40%     | 17       | 1        |
|                         | 100%       | 97.19%     | 17       | 2        |
| Text RCNN [1]           | 100%       | 97.71%     | 10       | 2        |
|                         | 100%       | 97.08%     | 11       | 2        |
|                         | 100%       | 98.07%     | 11       | 2        |
|                         | 100%       | 97.50%     | 10       | 2        |
|                         | 100%       | 97.86%     | 12       | 2        |
| DPCNN [1]               | 100%       | 97.55%     | 9        | 2        |
|                         | 100%       | 97.60%     | 9        | 2        |
|                         | 100%       | 97.50%     | 9        | 2        |
|                         | 100%       | 97.86%     | 9        | 1        |
|                         | 100%       | 97.24%     | 9        | 1        |

## 附录2 模型说明

> 噪音(a,b,c,d)：对于分词后的语料，对每个词：以a的概率替换为一个同义词（模拟不同方式下达同义指令，如查询/查看/查问），以b的概率替换为一个同音词（模拟语音识别出错）；对每个字：以c的概率重复1/2次（其中重复1次占80%的概率，重复2次占20%的概率，模拟持续发音），以d的概率删除（模拟发音较弱）。噪音越大，则处理后的文本与原始文本差别越大。
>
> 基本模型结构见[意图识别方法](#意图识别方法)，此处仅说明模型相关参数，如Epoch，rnn类型等

| 模型                    | 特征          | 模型噪音          | Epoch | 其它说明       |
| ----------------------- | ------------- | ----------------- | ----- | -------------- |
| logistic regression [1] | tf-idf特征    | (0.3,0.3,0.1,0.1) | -     | 逻辑斯蒂二分类 |
| random forest [1]       | tf-idf特征    | (0.3,0.3,0.1,0.1) | -     | 集成算法       |
| Text CNN [1]            | 随机embedding | (0.3,0.3,0.1,0.1) | 3     |                |
| Text RNN [1]            | 随机embedding | (0.3,0.3,0.1,0.1) | 10    | 双向LSTM       |
| Text RNN_Att [1]        | 随机embedding | (0.3,0.3,0.1,0.1) | 10    | 双向LSTM       |
| Text RCNN [1]           | 随机embedding | (0.3,0.3,0.1,0.1) | 5     | 双向LSTM       |
| DPCNN [1]               | 随机embedding | (0.3,0.3,0.1,0.1) | 5     | 多层CNN        |

