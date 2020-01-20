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
   - 成功log，如果是失败的，请带上失败的log给我，我尽力帮你调，如果刷量网站有变的话，也许会引起异常
     ```
		阅读量2127
		<function CsdnSeo.main at 0x0000000003CE3158>函数运行时间0.582s
		已完成刷量1次
		距离下一次运行时间还有180秒
		——————————————————————————————————
	 ```
