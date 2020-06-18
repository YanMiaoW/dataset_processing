import sys

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5 import QtGui


def main():
    '''可视化数据增加脚本，输出一个数据增强配置文件'''

    app = QApplication(sys.argv)

    # 设置主界面
    w = QWidget()
    w.resize(250, 150)
    w.move(300, 300)
    w.setWindowTitle('数据增强')
    w.setWindowIcon(QtGui.QIcon('window.png'))

    # 启动页面
    w.show()

    # 关闭页面
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
