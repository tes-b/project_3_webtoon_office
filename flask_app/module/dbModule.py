import psycopg2
from psycopg2.extras import execute_values
from flask_app.module.dbId import dbId 
# from dbId import dbId 

TABLE_WEBTOONS = "webtoons"

class Database:

    def __init__(self):
        dbid = dbId()
        self.connection = psycopg2.connect(
            host = dbid.get_host(),
            user = dbid.get_user(),
            password = dbid.get_password(),
            database = dbid.get_database()
        )
        
        if isinstance(self.connection,psycopg2.extensions.connection):
            print("db connected")
            self.cursor = self.connection.cursor()
        if isinstance(self.cursor,psycopg2.extensions.cursor):
            print("db initiation")

    def db_close(self):
        if isinstance(self.cursor,psycopg2.extensions.cursor):
            self.cursor.close()
        if isinstance(self.connection,psycopg2.extensions.connection):
            self.connection.close()
            print("db closed")

    def truncate(self):
        query_trun_webtoons = f"TRUNCATE TABLE {TABLE_WEBTOONS} CASCADE"

        try:
            self.cursor.execute(query_trun_webtoons)
        except Exception as e:
            print('EXCEPTION : ', e)
            self.db_close()
            return False
        
        return True, "table truncated"

    def process_data(self, data):

        values = []
        # print(data["title"])
        for val in data:
            genre = ""
            for a in val["genre"]:
                genre += a + ", "

            artist = ""
            for a in val["artist"]:
                artist += a + ", "            
            
            wt = (
                val["title"],
                val["platform"],
                val["link"],
                artist[:-2],
                genre[:-2],
                val["day"],
                val["rate"],
                val["for_adult"],
                val["views_rank"],
                val["synopsis"],
                val["thumbnail_link"]
                )
            values.append(wt)
        return values

    def insert_data(self, values):
        
        qr_insert = f"""
            INSERT INTO {TABLE_WEBTOONS} (
                title,
                platform,
                link,   
                artist,
                genre,
                day,
                rate,
                for_adult,
                views_rank,
                synopsis,
                thumbnail_link
                )
                VALUES %s
        """
        try:
            execute_values(self.cursor, qr_insert, values)
            self.connection.commit()
            return True, print("data insert done")            
        except Exception as e:
            self.db_close()
            return False, print("EXCEPTION : ", e)            


    def create_tables(self):
        
        query_drop_webtoons = f"DROP TABLE IF EXISTS {TABLE_WEBTOONS}"

        try:
            self.cursor.execute(query_drop_webtoons)
            self.connection.commit()

        except Exception as e:
            print('EXCEPTION : ', e)
            self.db_close()
            return False, print("EXCEPTION : ", e)
        
        print("table dropped")

        qr_create_table_webtoon = f"""
            CREATE TABLE {TABLE_WEBTOONS} (
                id          SERIAL PRIMARY KEY,
                title       VARCHAR(128),
                platform    VARCHAR(64),
                link        VARCHAR(256),
                artist      VARCHAR(64),
                genre       VARCHAR(64),
                day         VARCHAR(4),
                rate        FLOAT,
                for_adult   BOOLEAN,
                views_rank  INTEGER,
                synopsis    VARCHAR(512),
                thumbnail_link VARCHAR(256)
            )
        """

        try:
            self.cursor.execute(qr_create_table_webtoon)
            self.commit()
        except Exception as e:
            self.db_close()
            return False, print("EXCEPTION : ", e)

        return True, print("table created")

    def execute_all(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchall()
        return row

    def execute(self, query, args={}):
        self.cursor.execute(query,args)

    def execute_one(self, query, args={}):
        self.cursor.execute(query, args)
        row = self.cursor.fetchone()
        return row

    def commit(self):
        self.connection.commit()

    def update(self, data):
        values = self.process_data(data)
        result, _ = self.create_tables()
        if result:
            result, _ = self.insert_data(values)
            if result: 
                return True, print("data update done.")
        







