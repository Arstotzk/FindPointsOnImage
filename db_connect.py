import psycopg2
from config_read import Settings

class DBConnect:
    def __init__(self):
        settings = Settings()
        self.connect = psycopg2.connect(dbname=settings.dbName, user=settings.dbUser, password=settings.dbPassword,
                                        host=settings.dbHost, port=str(settings.dbPort))
        self.cursor = self.connect.cursor()

    def Close(self):
        self.cursor.close()
        self.connect.close()

    def ExecuteQuery(self, query):
        self.cursor.execute(query)
        result = self.cursor.fetchall()
        return result

    def ExecuteInsertQuery(self, query):
        self.cursor.execute(query)
        self.connect.commit()
        result = self.cursor.fetchone()[0]
        return result
