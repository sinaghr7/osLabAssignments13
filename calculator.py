from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtUiTools import QUiLoader


import operator

# Calculator state.
READY = 0
INPUT = 1


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        loader = QUiLoader()
        self.myUi = loader.load('mainwindow.ui')

        # Setup numbers.
        for n in range(0, 10):
            getattr(self.myUi, 'pushButton_n%s' % n).pressed.connect(lambda v=n: self.input_number(v))

        # Setup operations.
        self.myUi.pushButton_add.pressed.connect(lambda: self.operation(operator.add))
        self.myUi.pushButton_sub.pressed.connect(lambda: self.operation(operator.sub))
        self.myUi.pushButton_mul.pressed.connect(lambda: self.operation(operator.mul))
        self.myUi.pushButton_div.pressed.connect(lambda: self.operation(operator.truediv)) 

        self.myUi.pushButton_pc.pressed.connect(self.operation_pc)
        self.myUi.pushButton_eq.pressed.connect(self.equals)

        # Setup actions
        self.myUi.actionReset.triggered.connect(self.reset)
        self.myUi.pushButton_ac.pressed.connect(self.reset)

        self.reset()

        self.myUi.show()

    def display(self):
        self.myUi.lcdNumber.display(self.stack[-1])

    def reset(self):
        self.state = READY
        self.stack = [0]
        self.last_operation = None
        self.current_op = None
        self.display()


    def input_number(self, v):
        if self.state == READY:
            self.state = INPUT
            self.stack[-1] = v
        else:
            self.stack[-1] = self.stack[-1] * 10 + v

        self.display()

    def operation(self, op):
        if self.current_op:  # Complete the current operation
            self.equals()

        self.stack.append(0)
        self.state = INPUT
        self.current_op = op

    def operation_pc(self):
        self.state = INPUT
        self.stack[-1] *= 0.01
        self.display()

    def equals(self):
        if self.state == READY and self.last_operation:
            s, self.current_op = self.last_operation
            self.stack.append(s)

        if self.current_op:
            self.last_operation = self.stack[-1], self.current_op

            try:
                self.stack = [self.current_op(*self.stack)]
            except Exception:
                self.myUi.lcdNumber.display('Err')
                self.stack = [0]
            else:
                self.current_op = None
                self.state = READY
                self.display()


if __name__ == '__main__':
    app = QApplication([])
    app.setApplicationName("Calculator")

    window = MainWindow()
    app.exec_()