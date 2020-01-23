"""
测试文件,主要测试阅读量的算法。以及其他测试
"""

import time
import random
import datetime
import settings
import OpenSSL
import cryptography 
import certifi
from functools import reduce
from selenium import webdriver
from bs4 import BeautifulSoup
print(OpenSSL.__version__)
print(cryptography.__version__)
print(certifi.__version__)

class TimeSleepTest:
    """
    刷量的两种算法,计算该小时的请求频率间隔,一种获取平均值、一种获取随机值。
    此类是为了获得该小时刷量的运行间隔列表
    """
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
        # 经过测试
        # DayTime:白天时段,目前看来8分钟,也就是1-480s之间筛选20次的合计很接近3600s,重要的是不花费时间
        # Nigth:夜晚时段, 10分钟
        # BeforeDawn:凌晨时段,特殊处理一次,在3600内随机,剩下的一次用3600-之前的随机值
        # hourly_read_counts_tuple:获取元组数据;hourly:小时属于哪个时段,hourly_read_counts:每小时需要请求的次数
        hourly_read_counts_tuple = TimeSleepTest.time_sleep_hour()
        hourly = hourly_read_counts_tuple[0]
        hourly_read_counts = hourly_read_counts_tuple[1]
        # 造了两个假数据测试下
        #hourly = "DayTime"
        #hourly_read_counts = 20
        # get_random_choice_list:根据每小时需要请求的次数,连续随机,每次随机的数值加入列表;类型list
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

    def test_random_choice(self):
        """
        获取满足条件的随机数list,判断条件,小于3600s返回此次抽取的抓取的元组
        现在的计算比较符合一天刷300次的阅读量
        :return: 符合条件的随时数组("随机数列表", 随机数列表值之和)
        """
        s = 0
        while True:
            a = self.sum_random_choice_list()
            s += 1
            print("第{n}次运行,random 20次的数合计{m}".format(n=s, m=a[1]))
            if a[1] <= 3600:
                break
        return a


ua = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'
ua1 = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0'

def selenium_webdriver():
    """此方法可以不用代理，根据ua去刷阅读,不过刷的要慢一点。但是不花钱,找一个ua库即可"""
    # key值为ua
    chrome_options = webdriver.ChromeOptions()
    # 设置ua
    chrome_options.add_argument('user-agent=%s' % ua)
    # 无界面启动chrome
    chrome_options.add_argument('--headless')
    # 禁止图片加载,提高速度
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    chrome = webdriver.Chrome(options=chrome_options)
    chrome.get('https://blog.csdn.net/kdl_csdn/article/details/104023516')
    html = chrome.page_source
    chrome.quit()
    soup = BeautifulSoup(html, "html.parser")
    read_counts = soup.select('.read-count')[0].text
    print(read_counts)

if __name__ == '__main__':
    t = TimeSleepTest()
    print(t.test_random_choice())
