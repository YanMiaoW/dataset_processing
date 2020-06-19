import imgaug
import imgaug.augmenters as iaa
import configparser
import re


def aug_cfg_load(cfg_path):
    '''读取cfg增强设置文件，返回一个imgaug增强函数'''

    # cfg文件解析
    cp = configparser.ConfigParser()
    cp.read(cfg_path, encoding="utf-8")

    # 获取增强的函数数组
    fs = []
    for fc_name in cp.keys():

        # 跳过默认值
        if fc_name == 'DEFAULT':
            continue

        isopen = get_value(cp[fc_name]['open'])
        p = get_value(cp[fc_name]['p'])

        # open属性为1或True时，加载函数进数组
        if isopen in [1, True]:

            # 获取函数参数
            argv = {}
            for k, v in cp[fc_name].items():

                # 不记录open和p参数
                if k not in ['open', 'p']:
                    argv[k] = get_value(v)

            # print(f'\n【{fc_name}】')
            # print(argv)

            # 类另命名
            C = eval(f'iaa.{fc_name}')

            # 类初始化函数是否包含概率p属性
            if 'p' in C.__init__.__code__.co_varnames:

                # 实例化类
                c = C(p=p, **argv)

            else:

                # 实例化类
                c = C(**argv)

                # 添加概率函数
                c = iaa.Sometimes(p, c)

            # 添加函数到fs
            fs.append(c)


    # 函数整合
    seq = iaa.Sequential(fs, random_order=True)

    return seq


def get_value(v):

    # 去除每行后面的注释
    v = v.split('#')[0]

    # 转化成值
    v = eval(v)

    return v
