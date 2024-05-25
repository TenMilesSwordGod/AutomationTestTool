import sqlite3

class SQLiteDB:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def create_table(self, table_name, columns):
        """
        创建表格
        :param table_name: 表名
        :param columns: 列定义，格式如 "id INT PRIMARY KEY, name TEXT"
        """
        create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns})"
        self.cursor.execute(create_table_sql)
        self.conn.commit()

    def drop_table(self, table_name):
        """
        删除表格
        :param table_name: 表名
        """
        drop_table_sql = f"DROP TABLE IF EXISTS {table_name}"
        self.cursor.execute(drop_table_sql)
        self.conn.commit()

    def truncate_table(self, table_name):
        """
        清空表格
        :param table_name: 表名
        """
        truncate_table_sql = f"DELETE FROM {table_name}"
        self.cursor.execute(truncate_table_sql)
        self.conn.commit()


    def insert_record(self, table_name, values):
        """
        插入记录
        :param table_name: 表名
        :param values: 要插入的数据，格式为元组，如 (value1, value2, ...)
        """
        placeholders = ', '.join(['?' for _ in range(len(values))])
        insert_sql = f"INSERT INTO {table_name} VALUES ({placeholders})"
        self.cursor.execute(insert_sql, values)
        self.conn.commit()

    def delete_record(self, table_name, condition):
        """
        删除记录
        :param table_name: 表名
        :param condition: 删除条件，如 "id = 1"
        """
        delete_sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(delete_sql)
        self.conn.commit()

    def update_record(self, table_name, set_values, condition):
        """
        更新记录
        :param table_name: 表名
        :param set_values: 要更新的值，如 "name = 'New Name'"
        :param condition: 更新条件，如 "id = 1"
        """
        update_sql = f"UPDATE {table_name} SET {set_values} WHERE {condition}"
        self.cursor.execute(update_sql)
        self.conn.commit()

    def select_records(self, table_name, columns="*", condition=None):
        """
        查询记录
        :param table_name: 表名
        :param columns: 要查询的列，默认为所有列
        :param condition: 查询条件，默认为空
        :return: 查询结果
        """
        if condition:
            select_sql = f"SELECT {columns} FROM {table_name} WHERE {condition}"
        else:
            select_sql = f"SELECT {columns} FROM {table_name}"
        self.cursor.execute(select_sql)
        return self.cursor.fetchall()

    def table_exists(self, table_name):
        return self.conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?",
                                 (table_name,)).fetchone() is not None

    def close(self):
        """
        关闭数据库连接
        """
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
        # 创建数据库对象
    db = SQLiteDB('example.db')

    # db.drop_table('users')

    # 创建表格
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

    db.truncate_table(table_name="users")
    print(db.select_records('users'))
    db.insert_record('users', (1, 'Alice', 30))
    db.insert_record('users', (2, 'Bob', 25))

    # 查询记录
    print(db.select_records('users'))

    # 更新记录
    db.update_record('users', "age = 40", "id = 1")

    # 删除记录
    # db.delete_record('users', "id = 2")
    print("==============================")
    print(db.table_exists('users'))

    # 删除表格
    # db.drop_table('users')

    # 关闭数据库连接
    db.close()
