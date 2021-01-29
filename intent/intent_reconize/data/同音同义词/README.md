# 对指令语料进行同音同义词替换

使用同音词同义词等对模拟指令语料进行替换，以模拟指令识别结果误差。

## 数据

`txt_gen_gen_result.txt`：航空语音指令模拟语料库

`/ChineseHomophones/chinese_homophone_char.txt`：同音字

`/ChineseHomophones/chinese_homophone_word.txt.txt`：同音词

`/DIAC/cilin.txt`：同义词

`/DIAC/same_pinyin.txt`：同音字

## 思路

1. 同义词替换

   * 获取同义词典

     ``` python
     # 获取cilin.txt中的同义词列表
     # TODO: 根据语料库的词汇过滤不相关的list
     def gen_synonyms_dict(filename):
         synonyms = open_file(filename)
         synonyms_dict = []
         for s in synonyms:
             synonyms_dict.append(s.strip().split(' ')[1:])
         return synonyms_dict
     ```

   * 查询相关字词的同义词列表

     ```python
     # 获取word的同义词列表
     def get_synonyms(word, synonyms_dict):
         for synonyms in synonyms_dict:
             if word in synonyms:
                 return synonyms
     
         return []
     ```

   * 随机替换

     ```python
     # 随机替换同义词
     def random_replace_synonyms(n_sent, synonyms_dict):
         ret = []
         tokens = jieba.cut(n_sent)
         for w in tokens:
             # 以一定的概率 替换为一个同义词
             set_random_seed()
             pb = random.random()
             if pb < 0.5:
                 synonyms = get_synonyms(w, synonyms_dict)
                 set_random_seed()
                 nw = random.choice(synonyms) if synonyms!=[] else w
             else:
                 nw = w
     
             ret.append(nw)
     
         return "".join(ret)
     ```

2. 同音词替换

   * 获取同音词典

     ```python
     # 获取chinese_homophone_word.txt中的同音词列表
     # 由于词汇表过大 只截取前2w行 设置shorter=-1可读取整个文件
     def gen_homophone_dict(filename, shorter=20000):
         homophone = open_file(filename)
         homophone_dict = []
         count = 0
         for h in homophone:
             homophone_dict.append(h.strip().split('\t')[1:])
             count += 1
             if count >= shorter:
                 break
         return homophone_dict
     ```

   * 查询相关词的同音词列表

     ```python
     # 获取word的同音词列表
     def get_homophone(word, homophone_dict):
         for homophone in homophone_dict:
             if word in homophone:
                 return homophone
     
         return []
     ```

   * 随机替换

     ```python
     # 随机替换同音词
     def random_replace_homophone(n_sent, homophone_dict):
         ret = []
         tokens = jieba.cut(n_sent)
         for w in tokens:
             # 以一定的概率 替换为一个同音词
             set_random_seed()
             pb = random.random()
             if pb < 0.5:
                 homophone = get_homophone(w, homophone_dict)
                 set_random_seed()
                 nw = random.choice(homophone) if homophone!=[] else w
             else:
                 nw = w
     
             ret.append(nw)
     
         return "".join(ret)
     ```

3. 随机插入同音字词

   * 获取同音字词典

     ```python
     # 获取同音字词典
     def gen_same_pin(filename):
         samepin = open_file(filename)
         samepin_dict = []
         for sp in samepin:
             samepin_dict.append(reduce(lambda x,y:x+y, sp.strip().split('\t')))
         return samepin_dict
     ```

   * 查询相关词的同音字列表

     ```python
     # 获取与word同音的字列表
     def get_samepin(word, samepin_dict):
         for samepin in samepin_dict:
             if word in samepin:
                 return samepin
     
         return []
     ```

   * 随机重复一些字

     ```python
     # 随机增加同音字(代表该字被重复识别(如回音))
     def random_add_word(n_sent, samepin_dict):
         ret = []
         for w in n_sent:
             set_random_seed()
             pb = random.random()
             if pb < 0.2:
                 samepin = get_samepin(w, samepin_dict)
                 # 20%概率重复两次
                 set_random_seed()
                 nw = random.choice(samepin)*random.choice([1,1,1,1,2]) if samepin!=[] else w
             else:
                 nw = w
     
             ret.append(nw)
     
         return "".join(ret)
     ```

4. 随机删除字词

   * 随机删除一些字

     ```python
     # 随机删减一些字(代表没有识别到该字(如发音较弱))
     def random_remove_word(n_sent):
         ret = []
         for w in n_sent:
             set_random_seed()
             pb = random.random()
             # 以80%的概率保留这个字
             if pb > 0.8:
                 ret.append(w)
     
         return "".join(ret)
     ```

     