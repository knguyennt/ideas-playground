import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QMenu
from PyQt6.QtGui import QAction

from layout_colorwidget import Color


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Widget adder")
        self.context_menu = QMenu(self)
        action1 = self.context_menu.addAction("Action 1")
        action2 = self.context_menu.addAction("Action 2")
        action3 = self.context_menu.addAction("Action 3")

        # action1.triggered.connect(self.action1_triggered)
        # action2.triggered.connect(self.action2_triggered)
        # action3.triggered.connect(self.action3_triggered)
        layout = QHBoxLayout()
        # layout.addWidget()
        widget = QWidget()
        widget.setLayout(layout)
    
    def contextMenuEvent(self, e):
        context = QMenu(self)
        context.addAction(QAction("test 1", self))
        context.addAction(QAction("test 2", self))
        context.addAction(QAction("test 3", self))
        context.exec(e.globalPos())


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec()
