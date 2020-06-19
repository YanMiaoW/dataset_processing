import json
import easydict


class AugCNN:
    '''分类任务图片数据增强类'''

    def __init__(self, json_file):
        
        #读取配置文件
        with open(json_file) as f:
            cfg_json = json.load(f)

            cfg = easydict.EasyDict(cfg_json)
            self.cfg = cfg



    def augment(self, images):
        print(self.cfg)
