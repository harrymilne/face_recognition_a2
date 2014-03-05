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
        new_user = self.menu_new.addAction("User")
        #new_user.setDisabled(True)
        log_file = self.menu_new.addAction("Log File")
        log_file.setDisabled(True)

        self.file_menu.addMenu(self.menu_new)

        #add about option to menu 
        if sys.platform != "darwin":
            self.help_menu = self.menu_bar.addMenu("Help")
            self.about = self.help_menu.addAction("About SQLite Inspector")
        else:
            self.about = self.file_menu.addAction("About SQLite Inspector")

        self.load_database = self.file_menu.addAction("Load Database")
        self.load_database.setShortcut(QKeySequence("Ctrl+o"))

        self.refresh_database = self.file_menu.addAction("Refresh Database")
        self.refresh_database.setDisabled(True)
        self.refresh_database.setShortcut(QKeySequence("F5"))

        self.tab_data = BrowseDataWidget()

        self.tool_bar = QToolBar("Manage Databases")
        self.tool_bar.setMovable(False)
        self.tool_bar.setIconSize(QSize(20,20))

        self.tool_bar.addAction(self.load_database)
        self.tool_bar.addAction(self.refresh_database)

        self.addToolBar(self.tool_bar)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tab_data)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)
        self.setMenuWidget(self.menu_bar)
        self.setUnifiedTitleAndToolBarOnMac(True)
        self.setWindowTitle("SQLite Inspector")

        #connections
        new_user.triggered.connect(self.get_name)
        self.load_database.triggered.connect(self.load_database_file)
        self.about.triggered.connect(self.about_application)
        self.refresh_database.triggered.connect(self.refresh)

    def load_database_file(self):
        """asks the user for the database file to load and ensures any previous database
            connections are closed before opening a new connection to the given file
        """
        #ensure that model is removed so that connection to database can be closed
        self.tab_data.table_view.setModel(None)

        #print(os.path.dirname(sys.executable)+"/sqldrivers/libqsqlite.dylib")
        #test = QPluginLoader(os.path.dirname(sys.executable)+"/sqldrivers/libqsqlite.dylib")
        #print(test.errorString())
        #print(test.isLoaded())

        path = QFileDialog.getOpenFileName(caption="Open Database",filter="Database file (*.db *.dat);; All Files (*.*)")
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
            self.refresh_database.setDisabled(False)
            self.tab_data.update_layout(self.db_connection)

    def about_application(self):
        dialog = QDialog()
        dialog.setWindowTitle("About SQLite Inspector")

        layout = QVBoxLayout()
        logo_layout = QHBoxLayout()
        copyright_layout = QVBoxLayout()

        logo = QLabel()
        logo.setPixmap(self.logo.scaledToWidth(200))
        logo.setMinimumWidth(400)
        app_name = QLabel("<b>SQLite Inspector</b>")
        app_name.setSizePolicy(QSizePolicy(QSizePolicy.Fixed))
        copyright = QLabel("Copyright 2013 Adam McNicol")
        copyright.setSizePolicy(QSizePolicy(QSizePolicy.Fixed))
        twitter = QLabel("@AdamMcNicol")
        twitter.setSizePolicy(QSizePolicy(QSizePolicy.Fixed))
        app_version = QLabel("Version 0.3.1")
        app_version.setSizePolicy(QSizePolicy(QSizePolicy.Fixed))
        license = QTextEdit("""This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or any later version.
<br/><br/>
This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
<br/><br/>
You should have received a copy of the GNU General Public License along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>""")

        license.setMinimumWidth(400)
        license.setMaximumHeight(100)
        license.setReadOnly(True)

        logo_layout.addWidget(logo)
        copyright_layout.addWidget(app_name)
        copyright_layout.addWidget(app_version)
        copyright_layout.addWidget(copyright)
        copyright_layout.addWidget(twitter)
        logo_layout.addLayout(copyright_layout)
        layout.addLayout(logo_layout)
        layout.addWidget(license)

        dialog.setLayout(layout)
        dialog.setFixedWidth(500)
        dialog.setFixedHeight(400)
        dialog.exec_()

    def refresh(self):
        if self.tab_bar.currentIndex() == 1:
            self.tab_data.refresh()

    def get_name(self):
        self.name_dialog = UserCreation()
        self.name_dialog.name_signal.connect(self.recv_name)
        self.name_dialog.exec_()

    def recv_name(self, name):
        self.sq



def main():
    application = QApplication(sys.argv)
    application.addLibraryPath(os.path.dirname(sys.executable))
    window = BrowserWindow()
    window.show()
    window.raise_()
    application.exec_()


if __name__ == '__main__':
    main()