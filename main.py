from request import login, followMember, saleMember, submit
import datetime
import sys
import asyncio
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

typeMap = {
    "电话跟进": 1,
    "短信跟进": 2,
    "见面跟进": 3,
    "email跟进": 4
}

statusMap = {
    "无人接听": 0,
    "接通": 1,
    "电话忙": 2,
    "空号": 3,
    "关机": 4,
    "挂断": 5,
    "停机": 6
}


resultMap = {
    "未预约成功": 0,
    "预约成功": 1
}

paramterMap = {
    "潜在客户": "sale_premember",
    "会员跟进": "sale_member"
}

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
        self.contact_result = 0
        self.paramter = "sale_premember"

    def initGUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle("三体云动会员跟进辅助程序v1.0 (CHCC主页:githun.com/xcclovebaby)")
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

        # 账号
        self.usernameInput = QLineEdit(readOnly=True)
        self.usernameInput.setPlaceholderText("请输入用户名")

        # 密码输入框
        self.paswwordInput = QLineEdit(readOnly=True)
        self.paswwordInput.setEchoMode(QLineEdit.Password)
        self.paswwordInput.setPlaceholderText("请输入密码")

        # 页码
        self.start = QLineEdit()
        self.end = QLineEdit()

        # 内容输入框
        self.content = QTextEdit()
        self.content.ensureCursorVisible()
        self.content.setPlaceholderText("请输入跟进内容")
        self.content.setFixedSize(490, 100)

        # 服务方式下拉框
        typeBox = QComboBox(self)
        typeBox.addItems(list(typeMap.keys()))
        typeBox.currentIndexChanged[str].connect(self.onTypeClicked)

        # 服务状态下拉框
        statusBox = QComboBox(self)
        statusBox.addItems(list(statusMap.keys()))
        statusBox.currentIndexChanged[str].connect(self.onStatusClicked)

        # 服务结果下拉框
        resultBox = QComboBox(self)
        resultBox.addItems(list(resultMap.keys()))
        resultBox.currentIndexChanged[str].connect(self.onResultClicked)

        # 跟进客户类型下拉框
        paramterBox = QComboBox(self)
        paramterBox.addItems(list(paramterMap.keys()))
        paramterBox.currentIndexChanged[str].connect(self.onParamterClicked)

        formLayout.addRow("账号：", self.usernameInput)
        formLayout.addRow("密码：", self.paswwordInput)
        formLayout.addRow("开始页码：", self.start)
        formLayout.addRow("结束页码：", self.end)
        formLayout.addRow("跟进内容：", self.content)
        formLayout.addRow('跟进类型：', paramterBox)
        formLayout.addRow('服务方式：', typeBox)
        formLayout.addRow('通讯状态：', statusBox)
        formLayout.addRow('通讯结果：', resultBox)

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

    def onResultClicked(self,value):
        self.contact_result = resultMap.get(value)

    def OnBtnClicked(self):
        content = self.content.text()
        username = self.usernameInput.text()
        password = self.paswwordInput.text()
        end = int(self.end.text())
        start = int(self.start.text())
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        cookie = login(username, password)
        list = followMember(cookie, start)
        staff_id = None
        while len(list) > 0 and start < end:
            for memberId in list:
                if staff_id is None:
                    staff_id = saleMember(cookie, memberId)
                submit(cookie=cookie,
                 staff_id=staff_id, 
                 time=time, 
                 content=content, 
                 memberId=memberId,
                 concat_type=self.concat_type,
                 contact_status=self.contact_status,
                 contact_result=self.contact_result,
                 type = self.paramter)
            print("当前页码 %d" % start)
            start += 1
            list = followMember(cookie, start)

async def main():
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    ui.usernameInput.setText("lxy15020712608")
    ui.paswwordInput.setText("910216")
    ui.start.setText("1")
    ui.end.setText("9999")
    sys.exit(app.exec_())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [main()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()
