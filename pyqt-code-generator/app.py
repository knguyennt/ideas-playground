import sys

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QMenu,
    QPushButton,
)
from PyQt6.QtGui import QAction

from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("gacha auto clicker")

        page_layout = QVBoxLayout()
        self.button_layout = QHBoxLayout()
        command_block_layout = QHBoxLayout()

        btn = QPushButton("red")
        btn2 = QPushButton("red")
        btn3 = QPushButton("red")
        self.button_layout.addWidget(btn)
        self.button_layout.addWidget(btn2)
        self.button_layout.addWidget(btn3)

        btn.pressed.connect(self.addLayoutCommand)

        page_layout.addLayout(self.button_layout)
        page_layout.addLayout(command_block_layout)
        widget = QWidget()
        widget.setLayout(page_layout)
        self.setCentralWidget(widget)

    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("Delete", self))
        context.addAction(QAction("If", self))
        context.addAction(QAction("Loop", self))
        context.exec(e.globalPos())

    def addLayoutCommand(self):
        new_btn = QPushButton("blue")
        self.button_layout.addWidget(new_btn)


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
