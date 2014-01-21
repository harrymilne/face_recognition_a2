##SQL Interface

import traceback
import time
import sqlite3 as sql

from io import open
from os import listdir, path, makedirs
from ConfigParser import ConfigParser

class SQLInterface:
    __str__ = """object interface for SQLite3 database"""
    def __init__(self, db_fname):
        self.db_name = db_fname
        self.db_connection = sql.connect(db_fname)
        self.db_cursor = self.db_connection.cursor()
        config = ConfigParser()
        config.read("server.cfg")
        self.log_path = config.get("access_logs","log_path")
        self.init_log()
        self.create_tables()
        
    def init_log(self):
        print(self.log_path)
        if path.exists(self.log_path):
            if len(listdir(self.log_path)) == 0:
                self.create_log_file()
        else:
            makedirs(self.log_path)
            self.create_log_file()

    def create_tables(self):

        table_queries = [("Users",
                        """create table Users(
                        user_id integer,
                        user_name text,
                        primary key(user_id))"""),

                        ("Access",
                        """create table Access(
                        access_id integer,
                        user_id integer,
                        log_id integer,
                        access_date text,
                        access_toggle integer,
                        primary key(access_id))"""),

                        ("Log",
                        """create table Log(
                        log_id integer,
                        log_filen string,
                        log_created string,
                        primary key(log_id))""")]


        for tbl_name, sql_q in table_queries:
            try:
                self.db_cursor.execute(sql_q)
            except sql.OperationalError as e:
                if e.args[0] == 'table {0} already exists'.format(tbl_name):
                    print("Table {0} exists.".format(tbl_name))
                else:
                    traceback.print_exc()
                    print("Table {0} not created.".format(tbl_name))
        self.db_connection.commit()

    def add_user(self, user_name):
        if type(user_name) != type(str()):
            raise Exception("user_name must be string.")
        sql = "insert into Users(user_name) values (?)"
        self.db_cursor.execute(sql, (user_name.lower(),))
        self.db_connection.commit()

    def rm_user(self, user_id):
        sql_q = "delete from Users where user_id = ?"
        self.db_cursor.execute(sql_q, (user_id,))
        self.db_connection.commit()

    def ls_users(self):
        sql_q = "select user_name from Users"
        self.db_cursor.execute(sql_q)
        user_list = [user[0] for user in self.db_cursor.fetchall()]
        return user_list

    def fetch_user_id(self, user_name):
        """takes user_name as string and returns a list of matches"""
        if type(user_name) != type(str()):
            raise Exception("user_name must be string.")

        sql_q = "select * from Users where user_name = ?"
        self.db_cursor.execute(sql_q, (user_name.lower(),))
        result = self.db_cursor.fetchone()[0]
        return result

    def fetch_username(self, user_id):
        """returns name of given user_id"""
        sql_q = "select user_name from Users where user_id = ?"
        self.db_cursor.execute(sql_q, (user_id,))
        return self.db_cursor.fetchone()[0]

    def create_log_file(self):
        datetime = time.strftime("%y-%m-%dT%H%M%S")
        log_filen = datetime.strip(":")+".log"
        with open(self.log_path+log_filen, mode="w", encoding="utf-8"):
            pass
        sql_q = "insert into Log(log_filen, log_created) values (?,?)"
        self.db_cursor.execute(sql_q, (log_filen, datetime))
        self.db_connection.commit()

    def get_latest_log(self):
        sql_q = "select * from Log where log_id=(SELECT MAX(log_id) FROM Log)"
        self.db_cursor.execute(sql_q)
        log_file = self.db_cursor.fetchone()
        return log_file

    def append_latest_log(self, msg):
        path = self.log_path + self.get_latest_log()[1]
        with open(path, mode="a", encoding="utf-8") as log_f:
            log_f.write(msg+"\n")

    def log_access(self, user_name, toggle):
        sql_q = "insert into Access(user_id, log_id, access_date, access_toggle) values (?,?,?,?)"
        user_id = self.fetch_user_id(user_name)
        date = time.strftime("%y-%m-%dT%H:%M:%S")
        access_toggle = int(toggle)
        on_off = ["OFF", "ON"]
        msg = "[{0}] {1} toggled the system to {2}".format(date, user_name, on_off[access_toggle])
        log_id, log_filen = self.get_latest_log()[:-1]
        path = self.config["logs"]["log_folder"] + self.get_latest_log()[1]
        with open(self.log_folder+log_filen, mode="a", encoding="utf-8") as log_f:
            log_f.write(msg+"\n")
        self.db_cursor.execute(sql_q, (user_id, log_id, date, access_toggle))

    def logs_by_user(self, user_id):
        sql_q = "select * from Access where user_id = ?"
        self.db_cursor.execute(sql_q, (user_id,))
        return self.db_cursor.fetchall()



if __name__ == "__main__":
    db = SQLInterface("access.sqlite3")
    db.add_user("harry")
    #db.create_tables()
    #print(cfg.prefs)
    #print(db.fetch_username(1))
    #print(db.get_latest_log())
    #db.create_log_file()

    
    

