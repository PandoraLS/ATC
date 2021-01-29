## 目录结构

```bash
├── dev.txt                                     # 验证集
├── module.py                                   # 用于生成模拟数据
├── prep_data.py                                # 用于生成 train.txt, dev.txt, test.txt, vocab.pkl
├── README.md
├── read_pkl.py                                 # 读取pkl文件
├── sentence.json                               # 用于生成数据的模板
├── short_sentence.json                         # 用于生成数据的模板
├── test.txt                                    # 测试集
├── train.txt                                   # 训练集
└── vocab.pkl                                   # 词表
```

## 生成数据的方法
- 修改`sentence.json`中所有的`"count": 20,`, 将count 的值 替换为其他数值，比如 200，也可保持不变；
- 修改`module.py`中的第253行的count，与`sentence.json`中的count保持一致，文件生成`id_sentence_order.txt`等过程文件
- 运行`prep_data.py`文件生成 `train.txt`、`dev.txt`、`test.txt`、`vocab.pkl`几个文件，前一步骤中的过程文件会被删除，`id_sentence_order.txt`文件会被保留

