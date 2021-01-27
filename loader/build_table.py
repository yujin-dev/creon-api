import pymysql
from config import *
class Table:

    def __init__(self):
        self.connect = pymysql.connect(
            user=USER,
            passwd=PWD,
            host=HOST,
            db=DB
        )
        self.cursor = self.connect.cursor(pymysql.cursors.DictCursor)
    def _build_minute_table(self):
        sql = """
         CREATE TABLE minute_data(
         date VARCHAR(20) NOT NULL, 
         time VARCHAR(20) NOT NULL,
         stock_code VARCHAR(10) NOT NULL,
         open INT NOT NULL,
         close INT NOT NULL,
         high INT NOT NULL,
         low INT NOT NULL,
         volume INT NOT NULL
         );
         """
        self.cursor.execute(sql)
        self.check_build('minute_data')

    def _build_transaction_table(self):
        sql = """
         CREATE TABLE minute_transaction(
         date VARCHAR(20) NOT NULL, 
         time VARCHAR(20) NOT NULL,
         stock_code VARCHAR(6) NOT NULL,
         transaction INT NOT NULL
         );
         """
        self.cursor.execute(sql)
        self.check_build('minute_transaction')

    def _build_tick_table(self):
        sql = """
         CREATE TABLE tick_data(
         date VARCHAR(20) NOT NULL, 
         time VARCHAR(20) NOT NULL,
         stock_code VARCHAR(6) NOT NULL,
         close INT NOT NULL
         );
         """
        self.cursor.execute(sql)
        self.check_build('minute_transaction')

    def check_build(self, table_name):
        sql = f"""
        SELECT * FROM {table_name}
        """
        try:
            self.cursor.execute(sql)
            print(f"{table_name} exists")
        except pymysql.err.ProgrammingError as e:
            raise e
        result = self.cursor.fetchall()
        print(result)

if __name__ == "__main__":

    make_table= Table()
    make_table.check_build('minute_data')
