"""
三体云动Pro会员跟进程序
--------------------------------------
v.10 2023年2月13日
--------------------------------------
GitHub: https://github.com/xcclovebaby
"""
from api.request_pro import shop, switchShop, followMember, submit
import datetime
import sys
import os
import asyncio
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

HEAD = {"Content-Type": "application/json; charset=UTF-8",
        "Connection": "keep-alive",
        "Host": "pro.styd.cn",
        "Origin": "https://pro.styd.cn",
        "app-version": "c25265b",
        "app-id": "10000",
        "app-shop-id": "",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome",
        "token": "",
        "Cookie": ""
        }

typeMap = {
    "电话": 1,
    "微信": 2,
    "会员到访": 3,
    "上门拜访": 4
}

statusMap = {
    "已电话": 1,
    "已邀约": 2,
    "邀约成功": 3,
    "实际到访": 4,
    "已签约": 5,
    "已购卡": 6
}

paramterMap = {
    "潜在客户": 1,
    "正式会员": 2,
    "流失会员": 3
}

shopMap = {}

class Stream(QObject):
    """Redirects console output to text widget."""
    newText = pyqtSignal(str)

    def write(self, text):
        self.newText.emit(str(text))
        QApplication.processEvents()


class MainUi(QWidget):
    def __init__(self):
        super(MainUi, self).__init__()
        # 注掉这句就可以打印到控制台，方便调试
        sys.stdout = Stream(newText=self.onUpdateText)
        self.initGUI()
        self.concat_type = 1
        self.contact_status = 1
        self.shopId = 0
        self.paramter = 1

    def initGUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle("三体云动Pro会员跟进辅助程序v1.0 (CHCC主页:githun.com/xcclovebaby)")
        self.setFixedSize(600, 800)

        # 外层容器
        container = QVBoxLayout()

        # 表单容器
        formLayout = QFormLayout()

        rightLayout = QStackedLayout()
        self.process = QTextEdit(self, readOnly=True)
        self.process.ensureCursorVisible()
        self.process.setLineWrapColumnOrWidth(500)
        self.process.setLineWrapMode(QTextEdit.FixedPixelWidth)
        rightLayout.addWidget(self.process)

        # Token
        self.usernameInput = QTextEdit()
        self.usernameInput.setPlaceholderText("请输入Token")
        self.usernameInput.setFixedSize(490, 100)

        # Cookie
        self.paswwordInput = QTextEdit()
        self.paswwordInput.setPlaceholderText("请输入Cookie")
        self.paswwordInput.setFixedSize(490, 100)

        # 页码
        self.start = QLineEdit()
        self.end = QLineEdit()

        # 内容输入框
        self.content = QTextEdit()
        self.content.setPlaceholderText("请输入跟进内容")
        self.content.setFixedSize(490, 50)

        # 服务方式下拉框
        typeBox = QComboBox(self)
        typeBox.addItems(list(typeMap.keys()))
        typeBox.currentIndexChanged[str].connect(self.onTypeClicked)

        # 服务状态下拉框
        statusBox = QComboBox(self)
        statusBox.addItems(list(statusMap.keys()))
        statusBox.currentIndexChanged[str].connect(self.onStatusClicked)

        # 跟进客户类型下拉框
        paramterBox = QComboBox(self)
        paramterBox.addItems(list(paramterMap.keys()))
        paramterBox.currentIndexChanged[str].connect(self.onParamterClicked)

        # 门店下拉框
        self.shopBox = QComboBox(self)
        self.shopBox.currentIndexChanged[str].connect(self.onShopClicked)

        shopbtn = QPushButton("获取门店")
        shopbtn.clicked.connect(self.shopClicked)

        shopQVBoxLayout = QVBoxLayout();
        shopQVBoxLayout.addWidget(self.shopBox)
        shopQVBoxLayout.addWidget(shopbtn)
        shopQVBoxLayout.addStretch()

        formLayout.addRow("Token：", self.usernameInput)
        formLayout.addRow("Cookie：", self.paswwordInput)
        formLayout.addRow("开始页码：", self.start)
        formLayout.addRow("结束页码：", self.end)
        formLayout.addRow("跟进内容：", self.content)
        formLayout.addRow('会员分类：', paramterBox)
        formLayout.addRow('方式：', typeBox)
        formLayout.addRow('状态：', statusBox)
        formLayout.addRow('选择门店：', shopQVBoxLayout)

        btn = QPushButton("开始跟进")
        btn.setFixedSize(100, 50)
        btn.clicked.connect(self.OnBtnClicked)

        widgetRight = QWidget()
        widgetRight.setLayout(rightLayout)
        widgetRight.setStyleSheet("background-color:grey;")

        widgetLeft = QWidget()
        widgetLeft.setLayout(formLayout)

        container.addWidget(widgetLeft, alignment=Qt.AlignLeft)
        container.addWidget(widgetRight)
        container.addWidget(btn, alignment=Qt.AlignRight)

        self.setLayout(container)

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def closeEvent(self, event):
        """Shuts down application on close."""
        # Return stdout to defaults.
        sys.stdout = sys.__stdout__
        super().closeEvent(event)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def onTypeClicked(self,value):
        self.concat_type = typeMap.get(value)

    def onParamterClicked(self,value):
        self.paramter = paramterMap.get(value)

    def onStatusClicked(self,value):
        self.contact_status = statusMap.get(value)

    def onShopClicked(self,value):
        self.shopId = shopMap.get(value)

    def shopClicked(self):
        username = self.usernameInput.toPlainText()
        password = self.paswwordInput.toPlainText()
        HEAD['token'] = username
        HEAD['Cookie'] = password
        shopMap = shop(HEAD)
        self.shopBox.addItems(list(shopMap.keys()))
        self.shopId = list(shopMap.values())[0]
        HEAD['app-shop-id'] = str(self.shopId)


    def OnBtnClicked(self):
        content = self.content.toPlainText()
        end = int(self.end.text())
        start = int(self.start.text())
        cookie = switchShop(HEAD, self.shopId)

        styd_cookie = open('files\\styd_cookie.txt', 'w+')
        styd_token = open('files\\styd_token.txt', 'w+')
        password = self.paswwordInput.toPlainText()
        styd_cookie.write(password)
        styd_token.write(HEAD['token'])
        styd_cookie.close()
        styd_token.close()

        list = followMember(HEAD, cookie, self.shopId, self.paramter)
        try:
            while len(list) > 0 and start < end:
                for memberId in list:
                    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                    submit(HEAD=HEAD,
                            cookie=cookie,
                            time=time,
                            content=content,
                            memberId=memberId,
                            concat_type=self.concat_type,
                            contact_status=self.contact_status)
                print("当前页码 %d" % start)
                start += 1
                list = followMember(HEAD, cookie, self.shopId, self.paramter, start)
        except:
            err_box = QMessageBox(QMessageBox.Information, '错误！！', '程序执行异常！！！')
            err_box.exec_()

        msg_box = QMessageBox(QMessageBox.Information, '成功！', '已运行完成！')
        msg_box.exec_()

async def main():
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    styd_cookie = open('files\\styd_cookie.txt', 'r')
    cookie = styd_cookie.read()
    styd_token = open('files\\styd_token.txt', 'r')
    token = styd_token.read()
    ui.usernameInput.setText(token)
    ui.paswwordInput.setText(cookie)
    ui.start.setText("1")
    ui.end.setText("9999")
    sys.exit(app.exec_())
    styd_cookie.close()
    styd_token.close()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [main()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
