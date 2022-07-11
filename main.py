from request import login, followMember, saleMember, submit
import datetime
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


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
        # sys.stdout = Stream(newText=self.onUpdateText)
        self.initGUI()

    def initGUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle("三体云动会员跟进辅助程序")
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
        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("请输入用户名")

        # 密码输入框
        self.paswwordInput = QLineEdit()
        self.paswwordInput.setPlaceholderText("请输入密码")

        # 页码
        self.start = QLineEdit()
        self.end = QLineEdit()

        # 内容输入框
        self.content = QLineEdit()
        self.content.setPlaceholderText("请输入跟进内容")
        self.content.setFixedSize(500, 100)

        formLayout.addRow("账号:", self.usernameInput)
        formLayout.addRow("密码", self.paswwordInput)
        formLayout.addRow("开始", self.start)
        formLayout.addRow("结束", self.end)
        formLayout.addRow("内容", self.content)


        btn = QPushButton("开始")
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
                submit(cookie, staff_id, time, content, memberId)
            print("当前页码 %d" % start)
            start += 1
            list = followMember(cookie, start)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    ui.usernameInput.setText("lxy15020712608")
    ui.paswwordInput.setText("910216")
    ui.start.setText("1")
    ui.end.setText("9999")
    sys.exit(app.exec_())
