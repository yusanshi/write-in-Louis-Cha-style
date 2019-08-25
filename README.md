# 金庸风格补写

## 简介

输入开头、要生成的字数及温度，点击提交即可按金庸风格补写开头。

演示站：https://yusanshi.com/Louis_Cha/ ，参考了 [TensorFlow 官方教程](https://www.tensorflow.org/beta/tutorials/text/text_generation) 和 [LeeMeng 博客](https://leemeng.tw/how-to-generate-interesting-text-with-tensorflow2-and-tensorflow-js.html)。

![1566730015119](README.assets/1566730015119.png)

## 基本原理

### Python 版
运行`main.py`即为 Python 版。

### 网页版

#### 模型保存

若`apply.py`中`apply`函数的`save_to_JS`参数为`True`，则保存下`data.json`（是字段和序号间对应关系的一个字典）和可在 Tensorflow.js 中加载的模型。

#### 前端

在`website`文件夹中，分为前端`front-end`和`back-end`后端。前端包含主站 https://yusanshi.com/Louis_Cha/ 的源码，亦包括使用 Tensorflow.js 来生成字符序列的 Javascript 代码。

#### 后端

后端是使用 Node.js 搭建的用于提供中文分词服务的 API（这个分词服务用于对用户输入的开头分词）。核心的分词服务用的是 [NodeJieba](https://www.npmjs.com/package/nodejieba)，HTTPS 服务器用的是 [express](https://www.npmjs.com/package/express)，跨域访问问题用 [cors package](https://www.npmjs.com/package/cors) 解决，免费 HTTPS 证书由 [Let's Encrypt](https://letsencrypt.org/) 签发（之所以要给 API 添加对 HTTPS 的支持，是因为我的主站也是 HTTPS 的，不允许向 HTTP 地址发送 Ajax 请求）。 API 请求地址为 https://jieba.yusanshi.com:8000/ （POST 方法），同时也提供对 GET 请求的处理，直接访问这个地址即可在线体验（或检查该 API 有没有挂掉233），如下图。

![1566731287948](README.assets/1566731287948.png)

## 其他

### 数据集

从网上搜集到金庸老师的作品之后（txt格式），我对每部作品进行了处理（去掉“注”部分和“按”部分、多行空行转成一行），并打包放在了 https://yun.yusanshi.com/TF_datasets/Louis_Cha_novels.zip 。

> 依照《中华人民共和国著作权法》第二十二条“可以不经著作权人许可”的几种情况，请仅基于研究深度学习的目的使用本数据。

