##SQL Interface

import sqlite3 as sql
import traceback
import time
from os import path


class SQLInterface:
    __str__ = """object interface for SQLite3 database"""
    def __init__(self, db_fname):
        self.db_name = db_fname
        self.db_connection = sql.connect(db_fname)
        self.db_cursor = self.db_connection.cursor()
    
    def init_log(self):
    	if path.exists("logs/"):
    		pass
        

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
                    print("Table exists.")
                else:
                    traceback.print_exc()
                    print("Table {0} not created.".format(tbl_name))
        self.db_connection.commit()

    def add_user(self, user_name):
        if type(user_name) != type(str()):
            raise Exception("user_name must be string.")
        sql = "insert into Users(user_name) values (?)"
        self.db_cursor.execute(sql, (user_name,))
        self.db_connection.commit()

    def rm_user(self, user_id):
        sql_q = "delete from Users where user_id = ?"
        self.db_cursor.execute(sql_q, (user_id,))
        self.db_connection.commit()

    def ls_users(self):
        sql_q = "select * from Users"
        self.db_cursor.execute(sql_q)
        user_list = self.db_cursor.fetchall()
        return user_list

    def fetch_user_id(self, user_name):
        """takes user_name as string and returns a list of matches"""
        if type(user_name) != type(str()):
            raise Exception("user_name must be string.")

        sql_q = "select * from Users where user_name = ?"
        self.db_cursor.execute(sql_q, (user_name,))
        result = self.db_cursor.fetchall()
        return result

    def fetch_username(self, user_id):
    	"""returns name of given user_id"""
    	sql_q = "select user_name from Users where user_id = ?"
    	self.db_cursor.execute(sql_q, (user_id,))
    	return self.db_cursor.fetchone()[0]


    def log_access(self, user_id, toggle):
        sql_q = "insert into Access(user_id, log_id, access_date, access_toggle) values (?,?,?,?)"
        date = time.strftime("%y-%m-%dT%H:%M:%S")
        access_toggle = int(toggle)
        on_off = ["OFF", "ON"]
        msg = "[{0}] {1} toggled the system to {2}".format(date, self.fetch, on_off[access_toggle])
        self.db_cursor.execute(sql_q, (user_id, "", date, access_toggle))

    def logs_by_user(self, user_id):
    	sql_q = "select * from Access where user_id = ?"
    	self.db_cursor.execute(sql_q, (user_id,))
    	return self.db_cursor.fetchall()

class Config:
	pass



if __name__ == "__main__":
    db = SQLInterface("main.db")
    db.create_tables()
    #db.add_user("Harry")
    print(db.ls_users())
    print(db.fetch_username(1))

    
    

