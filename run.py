import argparse
import sys
from exception import PythonVersionErroor

if sys.version_info.major < 3:
    raise PythonVersionErroor("python verison gt python3")

def parser_arguments(argv):
    """
    :param argv:
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("operate", type=str, help="r: 运行刷量程序, t: 测试代理ip,需要填写上代理IP的地址")
    return parser.parse_args(argv)

if __name__ == '__main__':
    args = parser_arguments(sys.argv[1:])
    if args.operate == "r":
        from core import main
        main()
    elif args.operate == "t":
        from api import test_check_proxy
        test_check_proxy()