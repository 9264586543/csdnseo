"""
异常类信息,main调用
"""

class PythonVersionErroor(Exception):
    """版本异常信息,仅支持python版本>3"""

class ProxyException(Exception):
    """代理ip异常类"""

class ProxySettingsError(ProxyException):
    """代理配置范围错误"""

class ProxyCheckSettingsError(ProxyException):
    """代理配置范围错误"""

class ProxyAuthSettingsError(ProxyException):
    """代理验证配置错误"""

class HeadersException(Exception):
    """headers异常类"""

class HeadersSettingsError(HeadersException):
    """header头配置范围错误"""

class UrlsException(Exception):
    """urls配置异常类"""

class UrlsSettingsError(UrlsException):
    """urls不能为空"""

class ReadCountException(Exception):
    """每天刷量配置异常类"""

class TimeSleepSettingsError(ReadCountException):
    """readcount配置错误"""
