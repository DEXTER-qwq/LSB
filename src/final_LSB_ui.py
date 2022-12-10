from PySide2.QtWidgets import QApplication, QMessageBox, QFileDialog
from PySide2.QtUiTools import QUiLoader
import final_LSB


class ChaosLsb:
    e, d, n, C = "", "", "", ""

    def __init__(self):
        # 从文件中加载UI定义
        self.ui = QUiLoader().load('ui/test01.ui')
        self.ui.pushButton_img.clicked.connect(self.read_bmp)  # 选择加密文件
        self.ui.pushButton_msg.clicked.connect(self.read_txt)  # 选择密文
        self.ui.pushButton_en.clicked.connect(self.encode_show)  # 加密并展示按钮绑定点击事件
        self.ui.pushButton_import.clicked.connect(self.rsa_import)  # 快速导入按钮绑定点击事件
        self.ui.pushButton_rsa.clicked.connect(self.rsa_de)  # RSA解密按钮绑定点击事件
        self.ui.pushButton_img2.clicked.connect(self.read_bmp2)  # 选择解密文件
        self.ui.pushButton_de.clicked.connect(self.decode_show)  # 解密按钮绑定点击事件

    def read_bmp(self):
        FileDialog = QFileDialog(self.ui.pushButton_img)
        # 设置可以打开任何文件
        FileDialog.setFileMode(QFileDialog.AnyFile)
        # 文件过滤
        image_file, _ = FileDialog.getOpenFileName(self.ui.pushButton_img, 'open file', './',
                                                   'Image files (*.png *.bmp)')  # 选择目录，返回选中的路径 'Image files (*.png *.bmp)'
        # 判断是否正确打开文件
        if not image_file:
            QMessageBox.warning(self.ui.pushButton_img, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
            return
        self.ui.label_img.setText(image_file)
        # print(self.ui.label_img.text)
        print("读入文件成功")
        print(image_file)  # 默认打开当前路径   输出文件路径

    def read_txt(self):
        FileDialog = QFileDialog(self.ui.pushButton_msg)
        # 设置可以打开任何文件
        FileDialog.setFileMode(QFileDialog.AnyFile)
        # 文件过滤
        txt_file, _ = FileDialog.getOpenFileName(self.ui.pushButton_msg, 'open file', './',
                                                 '*.txt')  # 选择目录，返回选中的路径 '*.txt'
        # 判断是否正确打开文件
        if not txt_file:
            QMessageBox.warning(self.ui.pushButton_msg, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
            return
        self.ui.label_msg.setText(txt_file)
        print("读入文件成功")
        print(txt_file)  # 默认打开当前路径   输出文件路径

    def encode_show(self):
        # print(self.ui.label_img.text(), self.ui.label_msg.text())
        self.e, self.d, self.n, self.C = final_LSB.show_lsb(self.ui.label_img.text(), self.ui.label_msg.text(),
                                                            float(self.ui.lineEdit_key_en.text()))
        print(f'e= {self.e}\nd= {self.d}\nn= {self.n}\nC= {self.C}')

        self.ui.label_showe.setText(f'e={str(self.e)[:20]}')
        self.ui.label_showd.setText(f'd={str(self.d)[:20]}...')
        self.ui.label_shown.setText(f'n={str(self.n)[:20]}...')
        self.ui.label_showC.setText(f'C={str(self.C)[:20]}...')

    def read_bmp2(self):
        FileDialog = QFileDialog(self.ui.pushButton_img)
        # 设置可以打开任何文件
        FileDialog.setFileMode(QFileDialog.AnyFile)
        # 文件过滤
        image_file, _ = FileDialog.getOpenFileName(self.ui.pushButton_img, 'open file', './',
                                                   'Image files (*.png *.bmp)')  # 选择目录，返回选中的路径 'Image files (*.png *.bmp)'
        # 判断是否正确打开文件
        if not image_file:
            QMessageBox.warning(self.ui.pushButton_img, "警告", "文件错误或打开文件失败！", QMessageBox.Yes)
            return
        self.ui.label_img2.setText(image_file)
        # print(self.ui.label_img.text)
        print("读入文件成功")
        print(image_file)  # 默认打开当前路径   输出文件路径

    def decode_show(self):
        line = final_LSB.decode_show(self.ui.label_img2.text(), float(self.ui.lineEdit_key_de.text()))
        self.ui.label_lsb.setText(f'提取到的lsb:{line[:20]}...')

    def rsa_import(self):
        self.ui.lineEdit_d.setText(str(self.d))
        self.ui.lineEdit_n.setText(str(self.n))
        self.ui.lineEdit_C.setText(str(self.C))

    def rsa_de(self):
        d = self.ui.lineEdit_d.text()
        n = self.ui.lineEdit_n.text()
        self.ui.label_M.setText(f'明文:{final_LSB.decrypt(int(d), int(n), self.C)}')


app = QApplication([])
chaosLsb = ChaosLsb()
chaosLsb.ui.show()
app.exec_()
