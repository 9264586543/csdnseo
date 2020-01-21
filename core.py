"""
对于csdn刚发布的博文刷量,目前研究过代理ip与header值;代理IP为key是没问题的。
header值里cookie变化也是可以完成一次阅读;经研究,存在登录与非登录状态;两种状态都都有固定的数据;
"""

import sys
import time
import queue
import random
import urllib3
import datetime
import requests
import api
import settings
from functools import reduce
from bs4 import BeautifulSoup
from api import csdnseologger as log
from exception import ProxySettingsError, HeadersSettingsError, UrlsSettingsError, ProxyCheckSettingsError, ProxyAuthSettingsError, TimeSleepSettingsError
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
__version__ = "1.0.1"

class CsdnSeo:
    """csdn刷阅读,代理IP或header值为key"""
    
    @staticmethod
    def urls_queue():
        """
        url队列
        :return: urls的queue队列
        """
        if settings.URLS:
            que = queue.Queue()
            for url in settings.URLS:
                que.put(url)
            return que
        else:
            raise UrlsSettingsError("settings URLS can't be empty")

    @staticmethod
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

    def check_proxy(self, **kwargs):
        """
        对代理IP进行验证
        :return: bool
        """
        if settings.IS_CHECK_PROXY not in [0 ,1]:
            raise ProxyCheckSettingsError("settings IS_CHECK_PROXY={} range exception".format(settings.IS_CHECK_PROXY))

        if settings.IS_CHECK_PROXY == 1:
            proxies = CsdnSeo.proxies_format()
            try:
                r = requests.get(url=settings.CHECK_PROXY_URL, headers=settings.HEADERS_DEFAULT, proxies=proxies, verify=False)
                if r.status_code not in [200, 301, 302,]:
                    print("代理异常")
                    return False
                print("代理正常")
                return True
            except Exception as e:
                #self.logger.debug(e)
                raise e
        if settings.IS_CHECK_PROXY == 0:
            pass
        return None

    @api.spend_time
    def main(self, url):
        """
        查询配置文件,进行刷量
        :param url:
        :return: response body
        """
        # 配置文件的规则查询
        if settings.IS_HEADERS_DEFAULT not in [0, 1]:
            raise HeadersSettingsError(
                        "settings IS_HEADERS_DEFAULT={} range exception".format(settings.IS_HEADERS_DEFAULT)
                )

        if settings.IS_USE_PROXY not in [0, 1]:
            raise ProxySettingsError(
                        "settings IS_USE_PROXY={} range exception".format(settings.IS_USE_PROXY)
                )

        if settings.IS_HEADERS_DEFAULT == 0 and settings.IS_USE_PROXY == 0:
            r = requests.get(url=url, headers=settings.HEADERS_DEFAULT)
        elif settings.IS_HEADERS_DEFAULT == 0 and settings.IS_USE_PROXY == 1:
            proxies = CsdnSeo.proxies_format()
            self.check_proxy()
            r = requests.get(url=url, headers=settings.HEADERS_DEFAULT, proxies=proxies, verify=False)
        elif settings.IS_HEADERS_DEFAULT == 1 and settings.IS_USE_PROXY == 0:
            r = requests.get(url=url, headers=headers)
        else: # settings.IS_HEADERS_DEFAULT == 1 and settings.IS_USE_PROXY == 1
            proxies = CsdnSeo.proxies_format()
            self.check_proxy()
            r = requests.get(url=url, headers=headers, proxies=proxies, verify=False)

        # 读取页面内容的目前阅读量,如果网站改版,这里也容易出错
        soup = BeautifulSoup(r.text, "html.parser")
        read_counts = soup.select('.read-count')[0].text
        nums = read_counts.split(" ")[1]
        log.logger.info("博文{url}的阅读量{nums}".format(url=url, nums=nums))
        return r.text

class RunTimesleep:
    """
    刷量的两种算法,计算该小时的请求频率间隔,一种获取平均值、一种获取随机值。
    此类是为了获得该小时刷量的运行间隔列表
    """
    # 查看配置文件TIME_SLEEP_DEFAULT范围是否正常
    if settings.TIME_SLEEP_DEFAULT not in [0 ,1]:
        raise TimeSleepSettingsError(
            "settings TIME_SLEEP_DEFAULT={} range exception".format(settings.TIME_SLEEP_DEFAULT)
            )
    log.logger.info('settings TIME_SLEEP_DEFAULT={}'.format(settings.TIME_SLEEP_DEFAULT))
    @staticmethod
    def time_sleep_hour():
        """
        判断目前的小时是属于哪个时段
        :return: 该时段的元组("时段", 该时段每小时的请求量)
        """
        now = datetime.datetime.now()
        if now.hour in settings.BeforeDawn:
            hourly_read_counts_tuple = ("BeforeDawn", settings.BeforeDawn_Every_Hours)
        elif now.hour in settings.DayTime:
            hourly_read_counts_tuple = ("DayTime", settings.DayTime_Every_Hours)
        else: # now.hour in Nigth
            hourly_read_counts_tuple = ("Nigth", settings.Nigth_Every_Hours)
        return hourly_read_counts_tuple

    def random_choice_list(self):
        """
        从hourly_read_counts_tuple拿到每小时要刷的次数,随机抽取此小时的时间间隔,生成list
        :return: 随机数的列表
        """
        # hourly_read_counts_tuple:获取元组数据;hourly:小时属于哪个时段,hourly_read_counts:每小时需要请求的次数
        hourly_read_counts_tuple = RunTimesleep.time_sleep_hour()
        hourly = hourly_read_counts_tuple[0]
        hourly_read_counts = hourly_read_counts_tuple[1]
        # get_random_choice_list:根据每小时需要请求的次数,连续随机,每次随机的数值加入列表。类型list
        get_random_choice_list = []
        if  hourly == "BeforeDawn":
            s = [i for i in range(1, 60*60)]
            if hourly_read_counts <= 2:
                a = random.choice(s)
                b = 3600 - a
                get_random_choice_list = [a,b]
                return get_random_choice_list
        if hourly  == "DayTime":
            s = [i for i in range(1, 8*60)]
        if hourly  == "Nigth":
            s = [i for i in range(1, 10*60)]
        while True:
            get_random_choice_list.append(random.choice(s))
            hourly_read_counts -= 1
            if hourly_read_counts == 0:
                break
        return get_random_choice_list

    def sum_random_choice_list(self):
        """
        计算随机抽取值get_random_choice_list之和
        :return: 该时段的随机数组之和的元组("随机数列表", 随机数列表值之和)
        """
        get_random_choice_list = self.random_choice_list()
        # get_random_choice_list_counts:对随机获取到的数值进行累加
        get_random_choice_list_counts = reduce(lambda x, y: x+y, get_random_choice_list)
        return get_random_choice_list, get_random_choice_list_counts

    def get_random_choice(self):
        """
        获取满足条件的随机数list,判断条件,小于3600s返回此次抽取的抓取的元组
        现在的计算比较符合一天刷300次的阅读量
        :return: 符合条件的随时数组("随机数列表", 随机数列表值之和)
        """
        #s = 0
        while True:
            a = self.sum_random_choice_list()
            #s += 1
            #print("第{n}次运行,random 20次的数合计{m}".format(n=s, m=a[1]))
            if a[1] <= 3600:
                break
        return a

    def main(self):
        """
        算法模式选择,返回time_sleep_list,类型list
        :return: 请求时间间隔列表
        """
        if settings.TIME_SLEEP_DEFAULT == 0:
            time_sleep_list = [settings.HOURS_SECONDS // RunTimesleep.time_sleep_hour()[1]]
        if settings.TIME_SLEEP_DEFAULT == 1:
            req = RunTimesleep().get_random_choice()
            time_sleep_list = req[0]
        log.logger.info("符合sleep条件的列表{}".format(time_sleep_list))
        return time_sleep_list

def get_time_sleep_list():
    """
    获取请求时间间隔列表
    :return: 请求时间时间列表
    """
    return RunTimesleep().main()

def run_seo_main():
    """
    启动刷量程序
    :return: True
    """
    csdn = CsdnSeo()
    que = CsdnSeo.urls_queue()
    while not que.empty():
        url = que.get()
        csdn.main(url)
        # 多url进行不同时间的刷量
        s = random.choice(range(1, 5))
        time.sleep(s)
    return True

def main():
    """
    启动程序
    :return:
    """
    s = 0
    while True:
        time_sleep_list = get_time_sleep_list()
        for t in time_sleep_list:
            run_seo_main()
            s += 1
            log.logger.info("已完成刷量累计%s次" % s)
            log.logger.info("距离下一次运行时间还有%s秒" % t)
            time.sleep(t)

if __name__ == '__main__':
    main()

