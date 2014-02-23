import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import *

class UserCreation(QDialog):
    name_signal = pyqtSignal(str)

    def __init__(self):
        super(QDialog, self).__init__()

        #Elements
        self.name_label = QLabel("Name:")
        self.name_field = QLineEdit()
        self.name_button = QPushButton("Create")
        self.name_button.setDefault(True)
        self.cancel_button = QPushButton("Cancel")

        #Layout setup (QWidget, row, column)
        self.layout = QGridLayout()
        self.layout.addWidget(self.name_label, 1, 0)
        self.layout.addWidget(self.name_field, 1, 1, 1, 2)
        self.layout.addWidget(self.cancel_button, 2, 1)
        self.layout.addWidget(self.name_button, 2, 2)

        #Dialog setup
        self.setLayout(self.layout)

        #connections
        self.name_button.clicked.connect(self.submit)
        self.cancel_button.clicked.connect(self.close)

    def submit(self):
        name = str(self.name_field.text())
        print(name)
        if name.isalpha():
            self.name_signal.emit(name)
            self.done(1)

    def close(self):
        self.done(1)



if __name__ == '__main__':
    application = QApplication(sys.argv)
    window = UserCreation()
    window.show()
    window.raise_()
    application.exec_()


