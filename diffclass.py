import pymysql

class ChoosingFilm:
    def __init__(self, janr, string_Janr):
        self.janr = janr
        self.string = string_Janr
    def check_film(self):
        connection = pymysql.connect(host='localhost',
                                     user='Kotit',
                                     password='141923vaniqwerty',
                                     db='pythonbot',
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)
        try:
            with connection.cursor() as cursor:
                # Выполняем SQL-запрос для выборки строки из БД
                sql_select = "SELECT * FROM film WHERE NumberFilm = %s"
                cursor.execute(sql_select, (self.janr,))

                # Получаем результат запроса
                result = cursor.fetchone()

                # Если строка найдена, читаем ее
                if result:


                    if result['Janr'] == self.string:
                        return result
                else:
                    return False
        finally:
            # Всегда закрываем соединение с БД после использования
            connection.close()

