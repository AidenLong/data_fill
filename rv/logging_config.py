# -*- coding utf-8 -*- #

import logging


class Logger:

    def __init__(self, path='./logger/debug.log', clevel=logging.DEBUG, Flevel=logging.DEBUG):
        self.logger = logging.getLogger(path)
        self.logger.setLevel(logging.DEBUG)
        # fmt = logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%Y-%m-%d %H:%M:%S')
        fmt = logging.Formatter("%(asctime)s %(filename)s %(funcName)s %(lineno)s \
              %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S")
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(path)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

logger = Logger().logger
# if __name__ == '__main__':
#     logyyx = Logger().logger
#     logyyx.debug('一个debug信息')
#     logyyx.info('一个info信息')
#     logyyx.warning('一个warning信息')
#     logyyx.error('一个error信息')
#     logyyx.critical('一个致命critical信息')
