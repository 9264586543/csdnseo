## csdn博文刷量程序

#### python版本 
 - python3以上

#### 功能
 - 刷阅读量
 - 代理验证

#### 刷量算法
 - 平均值
 - 随机值

#### 依赖库
 - requests与bs4
 - 项目依赖 [requirements.txt](requirements.txt)
 - 安装方法:
      - root用户(避免多python环境产生问题): `pip3 install -r requirements.txt`
      - 非root用户（避免安装和运行时使用了不同环境）: `pip3 install -r requirements.txt`

#### 项目使用说明
  - 服务器启动:
      - 修改[配置](settings.py)文件
      - 设置上代理参数,本程序测试代理由[快代理](https://www.kuaidaili.com)赞助,建议使用隧道代理
        - 配置[配置](TickerConfig.py)文件的时候，需注意空格和遵循python语法格式
			```
            python3 run.py t
            ```
			# 用python3 还是python 完全取决于安装的时候配置的环境变量是否为python3,以下启动默认环境变量为python3
		
      - 启动前请先测试代理可用性，这点很`重要`
        ```
        python3 run.py t
        ```
      - 启动服务
        ```
        python3 run.py r
        ```
      - 如果你不知道如何操作，下面的命令可能会帮助你
        ```
        python3 run.py -h

        ——————————————————————————
        sage: run.py [-h] operate

        positional arguments:
          operate     r: 运行刷量程序, t: 测试代理可用性
        ```
#### 文件对应说明
  - core - 项目主运行
  - settings - 项目配置
  - api - 接口
  - exception - 异常
  - test  项目测试

#### 项目声明：
  - 本软件只供学习交流使用，勿作为商业用途

#### 日志列子
   - 成功log，如果是失败的，请带上失败的log给我，我尽力帮你调。
     ```
	2020-01-21 15:10:02,878 - INFO: settings TIME_SLEEP_DEFAULT=1
	2020-01-21 15:10:02,881 - INFO: 符合sleep条件的列表[88, 46, 144, 87, 119, 199, 17, 178, 160, 202, 327, 40, 122, 238, 21, 379, 187, 42, 211, 150]
	2020-01-21 15:10:03,694 - INFO: 博文https://blog.csdn.net/kdl_csdn/article/details/103962098的阅读量2270
	2020-01-21 15:10:06,362 - INFO: 博文https://blog.csdn.net/kdl_csdn/article/details/103985282的阅读量466
	2020-01-21 15:10:09,785 - INFO: 博文https://blog.csdn.net/kdl_csdn/article/details/103986221的阅读量396
	2020-01-21 15:10:14,205 - INFO: 博文https://blog.csdn.net/kdl_csdn/article/details/103989024的阅读量348
	2020-01-21 15:10:16,260 - INFO: 博文https://blog.csdn.net/kdl_csdn/article/details/103999779的阅读量395
	2020-01-21 15:10:19,843 - INFO: 博文https://blog.csdn.net/kdl_csdn/article/details/104023516的阅读量130
	2020-01-21 15:10:23,846 - INFO: 已完成刷量累计1次
	2020-01-21 15:10:23,846 - INFO: 距离下一次运行时间还有88秒

     ```
