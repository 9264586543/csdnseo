"""
api功能
函数运行时间;代理格式化处理;检测代理可用性;
多线程运行;随机筛选headers值;日志记录
"""
import time
import threading
import requests
import settings

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

def random_headers(headers):
    """
    对于ua库随机选择。
    :return: headers
    """
    pass

def test_check_proxy():
    return check_proxy(1)
