from tokenize import Double
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys
import asyncio

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

    def onUpdateText(self, text):
        """Write console output to text widget."""
        cursor = self.process.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.process.setTextCursor(cursor)
        self.process.ensureCursorVisible()

    def initGUI(self):
        QToolTip.setFont(QFont('SansSerif', 10))
        self.setWindowTitle("碳水循环计算器v1.0 (CHCC主页:githun.com/xcclovebaby)")
        self.setFixedSize(500, 500)
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

        btn = QPushButton("计算")
        btn.setFixedSize(100, 50)
        btn.clicked.connect(self.OnBtnClicked)

        # 体重
        self.width = QLineEdit()

        # 蛋白质
        self.p1 = QLineEdit()

         # 碳水
        self.p2 = QLineEdit()

         # 脂肪
        self.p3 = QLineEdit()

        formLayout.addRow("体重(kg):", self.width)
        formLayout.addRow("蛋白质(g):", self.p1)
        formLayout.addRow("碳水(g):", self.p2)
        formLayout.addRow("脂肪(g):", self.p3)

        widgetRight = QWidget()
        widgetRight.setLayout(rightLayout)
        # widgetRight.setStyleSheet("background-color:grey;")

        widgetLeft = QWidget()
        widgetLeft.setLayout(formLayout)
        container.addWidget(widgetLeft, alignment=Qt.AlignLeft)
        container.addWidget(widgetRight)
        container.addWidget(btn, alignment=Qt.AlignRight)

        self.setLayout(container)

    def OnBtnClicked(self):
        width = int(self.width.text())
        p1 = float(self.p1.text())
        p2 = float(self.p2.text())
        p3 = float(self.p3.text())
        print("\n\n=================================计算结果==================================")
        print("\n高碳日：%.2fg碳水、%.2fg脂肪、%.2fg蛋白质" % (p1 * width * 7 * 0.5 / 2, p3 * width * 7 * 0.15 / 2, p2 * width * 7 * 0.35 / 2))
        print("\n中碳日：%.2fg碳水、%.2fg脂肪、%.2fg蛋白质" % (p1 * width * 7 * 0.35 / 3, p3 * width * 7 * 0.35 / 3, p2 * width * 7 * 0.3 / 3))
        print("\n低碳日：%.2fg碳水、%.2fg脂肪、%.2fg蛋白质" % (p1 * width * 7 * 0.15 / 2, p3 * width * 7 * 0.5 / 2, p2 * width * 7 * 0.35 / 2))
        print("\n===========================================================================")


async def main():
    app = QApplication(sys.argv)
    ui = MainUi()
    ui.show()
    ui.width.setText('70')
    ui.p1.setText('2')
    ui.p2.setText('1.2')
    ui.p3.setText('0.8')
    ui.process.setText("\n碳水循环计划，1周1个循环，分别为：高碳2天、中碳3天、低碳2天。\n\n可以自由安排低中高碳日，请减肥的朋友一定要好好吃饭，好好休息，加油！！！")
    sys.exit(app.exec_())

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    tasks = [main()]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()

