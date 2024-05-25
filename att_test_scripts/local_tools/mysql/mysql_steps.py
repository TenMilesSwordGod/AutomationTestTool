import pymysql

from att_test_scripts.local_tools.basic_sql import BasicDB


class MySQLDB(BasicDB):
    def __init__(self, host, user, password, database, port=3306, charset='utf8mb4'):
        super().__init__()
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.charset = charset
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.create_database()
        try:
            self.conn = pymysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                charset=self.charset
            )
            self.cursor = self.conn.cursor()
            print("Successfully connected to MySQL")
        except pymysql.Error as e:
            print(f"Error while connecting to MySQL: {e}")

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        print("MySQL connection closed")

    def create_database(self):
        connection = pymysql.connect(host=self.host, user=self.user, password=self.password)
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES;")
            databases = [db[0] for db in cursor.fetchall()]
            if self.database in databases:
                print("db existed!!!")
                return
            sql = "CREATE DATABASE IF NOT EXISTS `{}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;".\
                format(self.database)
            cursor.execute(sql)
        connection.commit()
        print(f"Database {self.database} created successfully")

    def table_exists(self, table_name):
        self.cursor.execute("show tables")
        self.conn.commit()
        res_tuple: tuple = self.cursor.fetchall()
        for database in res_tuple:
            (db,) = database
            if table_name == db:
                return True
        else:
            return False


if __name__ == "__main__":
    db = MySQLDB(
        host='192.168.0.103',
        user='test',
        password='user@123',
        database='att_db'
    )

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
