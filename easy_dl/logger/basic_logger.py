'''
自定义一个logger类
能够生成一个目录(可以指定目录名,也可以自动根据时间来生成目录), 保存日志信息，生成图片，模型参数等
能够在终端输出日志信息，同时保存到txt文件
'''

import os
import time
import logging


import torch
from torchvision.utils import save_image
from torchvision.transforms.functional import to_pil_image

def makedir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

def create_results_dir(base_root='.', runname=None, time_suffix=True):
    '''
    创建结果保存目录

    Examples:
        print(create_results_dir(base_root='.', runname='', time_suffix=False)) # 结果保存在当前目录
        print(create_results_dir(base_root='.', runname='', time_suffix=True)) # 结果保存在当前时间戳目录下

        print(create_results_dir(base_root='.', runname='results', time_suffix=False)) # 结果保存在results目录下
        print(create_results_dir(base_root='results', runname='test', time_suffix=False)) # 结果保存在results/test目录下
    '''
    res_dir = os.path.join(base_root, runname)

    # 添加时间后缀
    if time_suffix:
        time_stamp = time.strftime("%Y%m%d%H%M%S", time.localtime())
        if runname is None or runname == '':
            res_dir = f'{time_stamp}'
        else:
            res_dir = f'{res_dir}_{time_stamp}'

    # 创建目录
    makedir_if_not_exists(res_dir)
    print(f'The results is in:{os.path.abspath(res_dir)}.')
    return res_dir

def loadLogger(work_dir, save_name='log.txt'):
    if work_dir in logging.Logger.manager.loggerDict:
        return logging.getLogger(work_dir)
    # setup logger
    logger = logging.getLogger(work_dir) # 以工作目录区分多个logger对象
    # set level
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(fmt="[ %(asctime)s ] %(message)s", datefmt="%a %b %d %H:%M:%S %Y")
    # output to stdout
    sHandler = logging.StreamHandler()
    sHandler.setFormatter(formatter)
    logger.addHandler(sHandler)
    # output to file
    fHandler = logging.FileHandler(os.path.join(work_dir, save_name), mode='w')
    fHandler.setFormatter(formatter)
    logger.addHandler(fHandler)
    # sys.stdout = fHandler.stream # 设置 print 打印到logger 日志中。
    return logger


class Logger():
    def __init__(self, base_root='.', runname=None, time_suffix=True):
        '''
        base_root_timesuffix
        base_root/runname_timesuffix
        base_root/runname_timesuffix

        :param base_root: 存放多次实验结果的目录
        :param runname: 实验名，如果为None则以时间作为名称
        :param time_suffix: 为实验名加上时间后缀
        :param mode:

        example:
            logger = Logger('./results', 'test', time_suffix=False)
            logger.log('Hello world!')
        '''
        # create the dir of results
        self.base_root = base_root
        self.res_dir = create_results_dir(base_root, runname, time_suffix)
        # setup logger
        self.logger = None

    # log info
    def log(self, msg):
        if self.logger is None:
            self.logger = loadLogger(self.res_dir, save_name=f'log.txt')
        self.logger.info(msg)

    # log tensor image
    def log_image(self, tensor, f):
        save_path = os.path.join(self.res_dir, f)
        makedir_if_not_exists(os.path.dirname(save_path))
        image = to_pil_image(tensor)
        image.save(save_path)

    # log tensor images
    def log_images(self, tensor, f, nrow=4):
        save_path = os.path.join(self.res_dir, f)
        makedir_if_not_exists(os.path.dirname(save_path))
        save_image(tensor, save_path, nrow=nrow)

    def log_state_dict(self, state_dict, f):
        save_path = os.path.join(self.res_dir, f)
        makedir_if_not_exists(os.path.dirname(save_path))
        torch.save(state_dict, save_path)
        self.log(f'save weight successfully!')

    def log_figure(self, figure, save_path):
        pass