"""
配置文件
URLS 类型list,要刷的网页url。
READ_COUNTS 每天要刷的阅读总量。
HEADERS 模拟用户请求,每次请求带上的header参数。
PROXY 代理IP参数,csdn经研究可以使用代理IP来刷阅读量。很有效,但要节制,新的博文控制好量
"""
from functools import reduce


# urls类型list,要刷阅读的url,支持列表推导式
URLS = ['https://blog.csdn.net/kdl_csdn/article/details/103962098',]
#URLS = []

# DAYS_SECONDS 每天要刷的阅读总量
# PS:csdn新用户发布新博文,建议用默认配置1天刷300次阅读即可。
# BeforeDawn表示凌晨时段,0-9点;DayTime白天时段,10-18点;Nigth夜晚时段,19-23点
# READ_COUNTS每天要刷的阅读总量,Days每天的3个时段阅读量占比。Total_Days占比之和
# TIME_SLEEP_DEFAULT 算法模式,取值[0,1].默认为0。用平均算法,取平均值。1用随机算法,用随机值的list
TIME_SLEEP_DEFAULT = 0
READ_COUNTS = 300
DAYS_SECONDS = 86400
HOURS_SECONDS = 3600
BeforeDawn = [i for i in range(0, 10)]
DayTime = [i for i in range(10, 19)]
Nigth = [i for i in range(19, 24)]
Days = {
    "BeforeDawn": 3, #凌晨,0点-9点,阅读量占当天的3/33
    "DayTime": 20, #白天,10点-18点,阅读量占当天的20/33
    "Nigth": 10, #夜晚,19点-23点,阅读量占当天的10/33
}
Total_Days = reduce(lambda x, y: x+y, list(Days.values()))

# 先算出3个时段需要的总量,每个时段的总量//当前时段的粒度(小时),得出每个粒度需要的量。
# BeforeDawn_Counts凌晨需要刷的阅读总量,DayTime_Counts白天需要刷的阅读总量,Nigth_Counts夜晚需要刷的阅读总量
# BeforeDawn_Every_Hours凌晨每小时的阅读量,DayTime_Every_Hours白天每小时的阅读量,Nigth_Every_Hours夜晚每小时的阅读量
BeforeDawn_Counts = READ_COUNTS * Days["BeforeDawn"] // Total_Days
DayTime_Counts = READ_COUNTS * Days["DayTime"] // Total_Days
Nigth_Counts = READ_COUNTS * Days["Nigth"] // Total_Days
BeforeDawn_Every_Hours = BeforeDawn_Counts // len(BeforeDawn)
DayTime_Every_Hours = DayTime_Counts // len(DayTime)
Nigth_Every_Hours = Nigth_Counts // len(Nigth)

# IS_HEADERS_DEFAULT:header值取值[0,1]。0默认;1用户自定义, 支持调用第三方的UA库
IS_HEADERS_DEFAULT = 0
HEADERS_DEFAULT = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36",
            #"Referer": "https://blog.csdn.net/kdl_csdn",
        }
#HEADERS_DEFAULT = {}

# IS_USE_PROXY:代理配置取值[0,1];0不开启代理,1开启代理
# IS_CHECK_PROXY:验证代理可用性取值[0,1],当启用代理时,支持此选项,0不验证。默认1则验证,默认使用csdn首页进行验证
# PROXY 代理的信息,不启用代理可以不填写。
# IS_PROXY_AUTH:代理IP的身份信息取值[0,1];默认0不需要;1需要,并且填写代理的用户名与密码。
# 此处代理由快代理www.kuaidaili.com赞助,建议使用隧道代理。
IS_USE_PROXY = 1
IS_CHECK_PROXY = 1
CHECK_PROXY_URL = 'https://www.csdn.net/'
PROXY = 'tps136.kdlapi.com:15818'
IS_PROXY_AUTH = 1
PROXY_USER = 't16878530245319'
PROXY_PWD = 'jason1234'

