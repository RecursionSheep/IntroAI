# 情感分类

models.py 为模型文件，可使用

```
python models.py
```

运行。

preprocess.py 为预处理文件，把训练集与测试集转换为词向量编号的形式。

## 模型

请至 [词向量](https://pan.baidu.com/s/1svFOwFBKnnlsqrF1t99Lnw) 下载，并将 sgns.sogounews.bigram-char 解压至 vec 文件夹下。

models.py 中 MLP_Model, CNN_Model, RNN_Model 分别定义了全连接网络、卷积网络与循环网络的模型，可以修改 model 调用的函数切换模型。

## 环境

```
python==3.6.8
keras==2.2.4
tensorflow==1.12.0
numpy==1.16.0
scipy==1.2.0
sklearn==0.0
```
