import click
import imgaug
import numpy as np
import glob
import augment
import cv2 as cv
import random
import os
import time


'''
example: python augwatch.py -r "aug_settings.cfg" -t "../data/road_disease"
        python augwatch.py -r "aug_settings.cfg" -t "../data/road_disease" --resize 0.3 --limit 5
'''


@click.command()
@click.option('-r', '--cfg-path', type=str, required=True,
              help='存储cfg配置文件的路径')
@click.option('-t', '--test-img-root', type=str, required=True,
              help='存储测试图片的root路径')
@click.option('--resize', type=float, default=None,
              help='测试图片缩放大小')
@click.option('--limit', type=int, default=None,
              help='限制图片加载数量')
@click.option('--interval', type=int, default=1000,
              help='加速时间间隔毫秒')
def main(cfg_path, test_img_root, resize, limit, interval):
    '''查看cfg增强设置文件的效果，按【d】下一张，按【e】加速播放和取消，按【ESC】关闭页面，更改cfg文件无需关闭页面，会自动重载cfg文件'''

    # 读取测试图片
    images = []
    for img_path in glob.glob(test_img_root+'/*.jpg'):
        # print(img_path)
        img = imread(img_path)

        # 图片缩放
        if resize:
            img = cv.resize(img, (0, 0), fx=resize, fy=resize)

        # 图片格式转换, (h, w, c) -> (1, h, w, c)
        img = np.reshape(img, (1, *img.shape))

        images.append(img)
        if limit:
            if len(images) >= limit:
                break

    # 读取增强函数
    aug = augment.aug_cfg_load(cfg_path=cfg_path)

    wait_key_time = 0
    cfg_last_change_time = os.stat(cfg_path).st_mtime

    # 循环展示
    while True:
        # 检查cfg变动，更新aug函数
        if os.stat(cfg_path).st_mtime != cfg_last_change_time:
            current_time=time.strftime("%H:%M:%S")
            #print(f"\rupdate cfg {current_time}",end='')
            cfg_last_change_time = os.stat(cfg_path).st_mtime
            aug = augment.aug_cfg_load(cfg_path=cfg_path)

        # 随机选择图片
        img = random.choice(images)

        # 图像增强
        augimg = aug(images=img)

        augimg = augimg[0]

        # 图片显示
        cv.imshow('augshow', augimg)

        key = cv.waitKey(wait_key_time)

        # 按【ESC】退出
        if key == ord('\033'):
            break

        # 按【d】下一张
        if key == ord('d'):
            continue

        # 按【e】自动播放和恢复
        if key == ord('e'):
            wait_key_time = interval if wait_key_time == 0 else 0


def imread(path):
    '''opencv的imread方法对中文路径的支持不好，用这个函数代替'''
    img = cv.imdecode(np.fromfile(path, dtype=np.uint8), -1)
    return img


if __name__ == "__main__":
    main()
