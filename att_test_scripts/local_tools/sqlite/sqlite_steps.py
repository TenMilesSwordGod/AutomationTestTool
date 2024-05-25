import sqlite3

from att_test_scripts.local_tools.basic_sql import BasicDB

class SQLiteDB(BasicDB):
    def __init__(self, db_name):
        super().__init__()
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def truncate_table(self, table_name):
        """
        清空表格
        :param table_name: 表名
        """
        truncate_table_sql = f"DELETE FROM {table_name}"
        self.cursor.execute(truncate_table_sql)
        self.conn.commit()


    def table_exists(self, table_name):
        return self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                                 (table_name,)).fetchone() is not None


if __name__ == "__main__":
    # python -m att_test_scripts.local_tools.sqlite.sqlite_steps
    db = SQLiteDB('example.db')
    db.drop_table('users')
    db.create_table('users', 'id INT PRIMARY KEY, name TEXT, age INT')
    print(db.select_records('users'))
    db.create_table('users', 'id INT PRIMARY KEY, name TEXT, age INT')
    print(db.select_records('users'))
    print(db.table_exists('users'))
    # 插入记录
    db.insert_record('users', (1, 'Alice', 30))
    db.insert_record('users', (2, 'Bob', 25))
    print(db.select_records('users'))
    print("***start to truncate table")
    db.truncate_table(table_name="users")
    print(db.select_records('users'))
    db.insert_record('users', (1, 'Alice', 30))
    db.insert_record('users', (2, 'Bob', 25))
    db.insert_record('users', (3, '3Alice', 30))
    db.insert_record('users', (4, '1Bob', 25))
    # 查询记录
    print(db.select_records('users'))
    # 更新记录
    db.update_record('users', "age = 40", "id = 1")
    print(db.select_records('users'))
    # 删除记录
    db.delete_record('users', "id = 2")
    print(db.select_records('users'))
    print("==============================")
    print(db.table_exists('users'))

    db.close()
