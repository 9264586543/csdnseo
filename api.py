"""
api功能
函数运行时间;代理格式化处理;检测代理可用性;
多线程运行;随机筛选headers值;日志记录
"""
import csv
import time
import random
import pymysql
import logging
import threading
import requests
import settings
from logging import handlers
from fake_useragent import UserAgent


def spend_time(func):
    """
    计算函数运行时间
    :param func:
    :return: 函数运行时间
    """
    def newFunc(*args, **args2):
        t0 = time.time()
        start_time = "%s" % (time.strftime("%X", time.localtime()))
        back = func(*args, **args2)
        end_time = "%s" % (time.strftime("%X", time.localtime()))
        spend_time = "%.3fs" % (time.time() - t0)
        print("{func}函数运行时间{time}".format(time=spend_time, func=func))
        return back
    return newFunc

def proxies_format(**kwargs):
    """
    代理IP格式化处理
    :return: proxies
    """
    if settings.IS_PROXY_AUTH not in [0, 1]:
        raise ProxyAuthSettingsError("settings IS_PROXY_AUTH={} range exception".format(settings.IS_PROXY_AUTH))
    if settings.IS_PROXY_AUTH == 0:
        proxies = {"http": "http://%s" % settings.PROXY, "https": "https://%s" % settings.PROXY}
    if settings.IS_PROXY_AUTH == 1:
        proxies = {
            "http": "https://%(user)s:%(pwd)s@%(ip)s/" % {'user': settings.PROXY_USER, 'pwd': settings.PROXY_PWD, "ip": settings.PROXY,},
            "https": "http://%(user)s:%(pwd)s@%(ip)s/" % {'user': settings.PROXY_USER, 'pwd': settings.PROXY_PWD, "ip": settings.PROXY,}
        }
    return proxies

def check_proxy(settings_argv, **kwargs):
    """
    对代理IP进行验证
    :param settings_argv 设置文件的参数settings.IS_CHECK_PROXY
    :return: bool
    """
    if settings_argv not in [0 ,1]:
        raise ProxyCheckSettingsError("settings IS_CHECK_PROXY={} range exception".format(settings_argv))

    if settings_argv == 1:
        proxies = proxies_format()
        try:
            r = requests.get(url=settings.CHECK_PROXY_URL, headers=settings.HEADERS_DEFAULT, proxies=proxies)
            if r.status_code not in [200, 301, 302,]:
                print("代理异常")
                return False
            print("代理正常")
            return True
        except Exception as e:
            raise e
    if settings_argv == 0:
        pass
    return None

def thread_run(func, *args):
    '''
    将函数打包进线程
    :param func
    :return:
    '''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    #t.join()

def random_headers():
    """
    使用fake_useragent的库,默认提取chrome的ua
    暂时先用着,后面出一个api功能
    :return: headers
    """
    ua = UserAgent().chrome
    if "ipad" or "iPad" in us:
        random_headers()
    else:
        headers = {"User-Agent": ua}
        return headers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    } # 日志级别关系映射

    def __init__(self, filename, level='info', when='D', backCount=3, fmt='%(asctime)s - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger(filename)
        format_str = logging.Formatter(fmt) # 设置日志格式
        self.logger.setLevel(self.level_relations.get(level)) # 设置日志级别
        sh = logging.StreamHandler() # 往屏幕上输出
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式
        th = handlers.TimedRotatingFileHandler(filename=filename, when=when, backupCount=backCount, encoding='utf-8') # 往文件里写入#指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        # interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        # S 秒
        # M 分
        # H 小时、
        # D 天、
        # W 每星期（interval==0时代表星期一）
        # midnight 每天凌晨
        th.setFormatter(format_str)# 设置文件里写入的格式
        self.logger.addHandler(sh) # 把对象加到logger里
        self.logger.addHandler(th)

# 这是我的日志记录,注意这里需要在创建/data/logs/csdnseo/目录
csdnseologger = Logger('/data/logs/csdnseo/csdnseo.log', level='debug')

def test_check_proxy():
    return check_proxy(1)

def csdn_mysqldb(sql):
    """
    操作csdnseo数据库,插入csdnseo表数据
    :parma sql;
    :return:
    """
    db = pymysql.connect("localhost","root","123456","csdnseo")
    cur = db.cursor()
    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    db.close()
    return None

