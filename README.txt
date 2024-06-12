一、概述
这是一个根据抖音视频id保存视频至本地的爬虫项目，可以批量爬取抖音视频，项目依托scrapy框架及selenium自动化技术，不熟悉可以先看:
scrapy:https://www.bilibili.com/video/BV1QY411F7Vt
selenium:https://www.bilibili.com/video/BV1Z4411o7TA

二、依赖
详见requirements.txt
终端安装:pip install -r requirements.txt

三、模块介绍
1、video_spider为程序的主要逻辑，包含访问及提取步骤
2、items中修改保存的数据字段
3、middlewares中包含抖音验证中间件，可设置无浏览器或有浏览器模式
4、pipelines设置保存模式
5、run为调用函数
6、config_get_logcookie为设置获取函数，主要获取登录cookie

四、使用方法
1、在网址目录目录中设置好要爬取的excel列表
2、在video_spider中设置好目标excel路径及网址列
3、运行config_get_logcookie，扫码登陆，自动保存cookie
4、运行run程序
5、视频结果保存至“爬取视频”
