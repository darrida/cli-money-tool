# Standard
import sqlite3
import os
import sys
from pathlib import Path

class transactions:
    def __init__(self, id, account, date, description, amount, misc):
        self.id = id
        self.account = account
        self.date = date
        self.description = description
        self.amount = amount
        self.misc = misc
    

# class tags(self):
#     id = self.id
#     tag = self.tag


# class tags_link(self):
#     id = self.id
#     id_tag = self.id_tag
#     id_transaction = self.id_transaction


class database(object):
    #__DB_LOCATION = Path.home() / 'Documents' / 'GitHub' / '_appdata' / 'cli_money_tool' / 'accounts.db'
    #print(__DB_LOCATION)

    def __init__(self):
        __DB_LOCATION = Path.home() / 'Documents' / 'GitHub' / '_appdata' / 'cli_money_tool' / 'accounts.db'
        if os.path.exists(__DB_LOCATION):
            self.__db_connection = sqlite3.connect(__DB_LOCATION)
            self.cur = self.__db_connection.cursor()
        else:
            Path(Path.home() / 'Documents' / 'GitHub' / '_appdata' / 'cli_money_tool').mkdir(parents=True, exist_ok=True)
            self.__db_connection = sqlite3.connect(__DB_LOCATION)
            self.cur = self.__db_connection.cursor()
    def __del__(self):
        self.__db_connection.close()
    
    def __enter__(self):
        return self

    def __exit__(self, ext_type, exc_value, traceback):
        self.cur.close()
        if isinstance(exc_value, Exception):
            self.__db_connection.rollback()
        else:
            self.__db_connection.commit()
        self.__db_connection.close()

    def execute(self, new_data):
        return self.cur.execute(new_data)

    def executemany(self, many_new_data):
        self.create_table()
        self.cur.executemany('REPLACE INTO jobs VALUES(?, ?, ?, ?)', many_new_data)

    def insert(self, record):
        record.id = self.cur.execute('''SELECT MAX(id) FROM transactions''').fetchone()[0]
        record.id = record.id + 1 if record.id else 1
        self.cur.execute(f'''INSERT INTO transactions
                             VALUES (
                                        "{record.id}",
                                        "{record.account}",
                                        "{record.date}",
                                        "{record.description}",
                                        "{record.amount}",
                                        "{record.misc}"
                        )''')

    def create_tables(self):
        if Path.home() / 'Documents' / 'GitHub' / '_appdata' / 'cli_money_tool' / 'accounts.db':
            pass
        else:
            Path(Path.cwd() / '..' / '_appdata' / 'cli_money_tool').mkdir(parents=True, exist_ok=True)

        
        """create a database table if it does not exist already"""
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
                                "transactions" (
                                    "id"            INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "account"    	TEXT NOT NULL,
                                    "date"	        TEXT NOT NULL,
                                    "description"	TEXT,
                                    "amount"	    INTEGER NOT NULL,
                                    "misc"          INTEGER    
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
                                "tags_link" (
                                    "id"	          INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "id_tag"	      INTEGER NOT NULL,
                                    "id_transaction"  INTEGER NOT NULL
                        )''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS 
                                "tags" (
                                    "id"	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                                    "tag"	TEXT NOT NULL
                        )''')

    def select_all_transactions(self):
        return self.cur.execute('''SELECT * FROM transactions''').fetchall()
        
    def sum_transactions_all(self, account):
        all_amounts = self.cur.execute(f'''SELECT amount FROM transactions
                                           WHERE account = '{account}'
                                        ''').fetchall()
        sum = 0
        for i in all_amounts:
            sum += float(i[0])
        return round(sum, 2)

    def commit(self):
        self.connection.commit()



# class Database(object):
#     """sqlite3 database class that holds testers jobs"""
#     DB_LOCATION = "/root/Documents/testerJobSearch/tester_db.sqlite"

#     def __init__(self):
#         """Initialize db class variables"""
#         self.connection = sqlite3.connect(Database.DB_LOCATION)
#         self.cur = self.connection.cursor()

#     def close(self):
#         """close sqlite3 connection"""
#         self.connection.close()

#     def execute(self, new_data):
#         """execute a row of data to current cursor"""
#         self.cur.execute(new_data)

#     def executemany(self, many_new_data):
#         """add many new data to database in one go"""
#         self.create_table()
#         self.cur.executemany('REPLACE INTO jobs VALUES(?, ?, ?, ?)', many_new_data)

#     def create_table(self):
#         """create a database table if it does not exist already"""
#         self.cur.execute('''CREATE TABLE IF NOT EXISTS jobs(title text, \
#                                                             job_id integer PRIMARY KEY, 
#                                                             company text,
#                                                             age integer)''')

#     def commit(self):
#         """commit changes to database"""
#         self.connection.commit()