import psycopg2
from datetime import datetime
import pytz
import pandas as pd
import lpr_const as lpr

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = psycopg2.connect(
            database=database,
            user=lpr.user,
            password=lpr.password,
            host=lpr.host,
            port=lpr.port
        )

        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_reg` WHERE `status` = ?", (status,)).fetchall()
        self.connection.close()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("select exists(select 1 from subscriptions_reg where user_id = %s)",
                                         (str(user_id),))
            return self.cursor.fetchone()[0]
        self.connection.close()

    def subscriber_times(self, times):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions_reg` WHERE `times` = ? ", (times,)).fetchall()

    def add_subscriber(self, user_id, username, first_name, last_name, status = True):
        a = datetime.now(pytz.timezone('Europe/Moscow')).strftime("%Y-%m-%d %H:%M:%S") # вызывается этот объект и фиксируется дата
        times = a
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO subscriptions_reg (user_id, status, times, username, first_name, last_name) VALUES(%s,%s,%s,%s,%s,%s)", (user_id,status, times, username, first_name, last_name))
        self.connection.close()

    def subscriber_exists_username(self, username):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute("select exists(select 1 from subscriptions_reg where username = %s)",
                                         (str(username),))

            return self.cursor.fetchone()[0]




    def send_base (self):
            self.cursor.execute("SELECT user_id, times, username, first_name, last_name, status from subscriptions_reg")
            res = pd.DataFrame()
            rows = self.cursor.fetchall()
            for row in rows:
                user_id = row[0]
                times = row[1]
                username = row[2]
                first_name = row[3]
                last_name = row[4]
                status = row[5]

                res = res.append(pd.DataFrame([[user_id, times, username, first_name, last_name, status]],
                                             columns=['user_id', 'times', 'username', 'first_name', 'last_name_id',
                                                      'status']), ignore_index=True)

            res.to_excel('result.xlsx')
            self.connection.close()



    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()

