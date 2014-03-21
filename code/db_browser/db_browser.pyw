import sys
import os
import sqlite3

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtSql import *

from sqlite_browse_data import *
from sqlite_connection import *
from dialogs import *

class BrowserWindow(QMainWindow):
    """Creates the main window for the application"""
    def __init__(self):
        super(QMainWindow, self).__init__()

        self.db_connection = None


        self.menu_bar = QMenuBar()
        self.file_menu = self.menu_bar.addMenu("File")

        self.menu_new = QMenu("New")
        self.menu_new.setDisabled(True)
        new_user = self.menu_new.addAction("User")
        log_file = self.menu_new.addAction("Log File")

        self.file_menu.addMenu(self.menu_new)


        self.load_database = self.file_menu.addAction("Load Database")
        self.load_database.setShortcut(QKeySequence("Ctrl+o"))

        self.refresh_database = self.file_menu.addAction("Refresh Database")
        self.refresh_database.setDisabled(True)
        self.refresh_database.setShortcut(QKeySequence("F5"))

        self.tab_data = BrowseDataWidget()
        self.tab_data.setDisabled(True)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_data)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setMenuWidget(self.menu_bar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowTitle("Database Browser")

        #connections
        new_user.triggered.connect(self.get_name)
        log_file.triggered.connect(self.create_log)
        self.load_database.triggered.connect(self.load_database_file)
        self.refresh_database.triggered.connect(self.refresh)

    def load_database_file(self):
        """asks the user for the database file to load and ensures any previous database
            connections are closed before opening a new connection to the given file
        """
        #ensure that model is removed so that connection to database can be closed
        self.tab_data.table_view.setModel(None)

        path = QFileDialog.getOpenFileName(caption="Open Database",filter="SQLite3 Files (*.sqlite3);; All Files (*)")
        if len(path) > 0:
            #already have a connection object
            if self.db_connection:
                self.db_connection.path = path
            else:
                self.db_connection = SQLConnection(path)
            
            ok = self.db_connection.open_database()
            self.set_up_elements()

    def set_up_elements(self):
        """updates the current tab by providing the current database connection to the update method of the
        appropriate main_widget"""
        
        if self.db_connection:
            self.tab_data.setDisabled(False)
            self.menu_new.setDisabled(False)
            self.refresh_database.setDisabled(False)
            self.tab_data.update_layout(self.db_connection)


    def refresh(self):
        self.tab_data.refresh()

    def get_name(self):
        self.name_dialog = UserCreation()
        self.name_dialog.name_signal.connect(self.recv_name)
        self.name_dialog.exec_()

    def recv_name(self, name):
        if self.db_connection.add_user(name):
            self.status_bar.showMessage("User {} sucessfully created...".format(name))
        else:
            self.status_bar.showMessage("An error occured while trying to create a user...".format(name))
        self.refresh()

    def create_log(self):
        if self.db_connection.add_log():
            self.status_bar.showMessage("A new log has sucessfully been created...")
        else:
            self.status_bar.showMessage("An error occured while trying to create a new log...")
        self.refresh()



def main():
    application = QApplication(sys.argv)
    application.addLibraryPath(os.path.dirname(sys.executable))
    window = BrowserWindow()
    window.show()
    window.raise_()
    application.exec_()


if __name__ == '__main__':
    main()