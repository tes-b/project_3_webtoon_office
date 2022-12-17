import psycopg2
from psycopg2.extras import execute_values
import crawler
from module.dbId import dbId 

TABLE_WEBTOONS = "webtoons"
TABLE_GENRES = "genres"
TABLE_ARTISTS = "artists"
TABLE_DAYS = "days"
TABLE_WT_GR = "webtoon_genre"
TABLE_WT_AT = "webtoon_artist"
TABLE_WT_DAY = "webtoon_day"

def db_init():
    db = dbId()
    connection = psycopg2.connect(
        host = db.get_host(),
        user = db.get_user(),
        password = db.get_password(),
        database = db.get_database()
    )
    # print(type(connection))
    if isinstance(connection,psycopg2.extensions.connection):
        print("db connected")
        cursor = connection.cursor()
    if isinstance(cursor,psycopg2.extensions.cursor):
        print("db initiation")

    return connection, cursor

def db_close(connection, cursor):
    if isinstance(cursor,psycopg2.extensions.cursor):
        cursor.close()
    if isinstance(connection,psycopg2.extensions.connection):
        connection.close()
        print("db closed")

def db_truncate(connection, cursor):
    # query_trun_wt_day   = f"TRUNCATE TABLE {TABLE_WT_DAY}"
    # query_trun_wt_artist= f"TRUNCATE TABLE {TABLE_WT_AT}"
    # query_trun_wt_genre = f"TRUNCATE TABLE {TABLE_WT_GR}"
    # query_trun_days     = f"TRUNCATE TABLE {TABLE_DAYS} CASCADE"
    # query_trun_artists  = f"TRUNCATE TABLE {TABLE_ARTISTS} CASCADE"
    # query_trun_genres   = f"TRUNCATE TABLE {TABLE_GENRES} CASCADE"
    query_trun_webtoons = f"TRUNCATE TABLE {TABLE_WEBTOONS} CASCADE"

    try:
        # cursor.execute(query_trun_wt_day)
        # cursor.execute(query_trun_wt_artist)
        # cursor.execute(query_trun_wt_genre)
        # cursor.execute(query_trun_days)
        # cursor.execute(query_trun_artists)
        # cursor.execute(query_trun_genres)
        cursor.execute(query_trun_webtoons)
    except Exception as e:
        print('EXCEPTION : ', e)
        db_close(connection, cursor)
        return False
    
    return True, "table truncated"

def update(connection, cursor, data):

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

    execute_values(cursor, qr_insert, values)
    connection.commit()


def create_tables(connection, cursor):
    
    query_drop_wt_day = f"DROP TABLE IF EXISTS {TABLE_WT_DAY}"
    query_drop_wt_genre = f"DROP TABLE IF EXISTS {TABLE_WT_GR}"
    query_drop_wt_artist = f"DROP TABLE IF EXISTS {TABLE_WT_AT}"
    query_drop_genres = f"DROP TABLE IF EXISTS {TABLE_GENRES}"
    query_drop_artists = f"DROP TABLE IF EXISTS {TABLE_ARTISTS}"
    query_drop_days = f"DROP TABLE IF EXISTS {TABLE_DAYS}"
    query_drop_webtoons = f"DROP TABLE IF EXISTS {TABLE_WEBTOONS}"

    try:
        # cursor.execute(query_drop_wt_day)
        # cursor.execute(query_drop_wt_genre)
        # cursor.execute(query_drop_wt_artist)
        # cursor.execute(query_drop_days)
        # cursor.execute(query_drop_artists)
        # cursor.execute(query_drop_genres)
        cursor.execute(query_drop_webtoons)

    except Exception as e:
        print('EXCEPTION : ', e)
        db_close(connection, cursor)
        return "create table fail"
    
    connection.commit()
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

    # qr_create_table_genre = f"""
    #     CREATE TABLE {TABLE_GENRES} (
    #         id SERIAL PRIMARY KEY,
    #         genre   VARCHAR(32) UNIQUE
    #     )
    # """
    # qr_create_table_artist = f"""
    #     CREATE TABLE {TABLE_ARTISTS} (
    #         id      SERIAL PRIMARY KEY,
    #         artist  VARCHAR(32) UNIQUE
    #     )
    # """

    # qr_create_table_days = f"""
    #     CREATE TABLE {TABLE_DAYS} (
    #         id       SERIAL PRIMARY KEY,
    #         day      VARCHAR(8) UNIQUE
    #     )
    # """

    # qr_create_table_webtoon_genre = f"""
    #     CREATE TABLE {TABLE_WT_GR} (
    #         webtoon_id  INTEGER REFERENCES {TABLE_WEBTOONS} (id) CASCADE,
    #         genre_id    INTEGER REFERENCES {TABLE_GENRES} (id) CASCADE
    #     )
    # """

    # qr_create_table_webtoon_artist = f"""
    #     CREATE TABLE {TABLE_WT_AT} (
    #         webtoon_id  INTEGER REFERENCES {TABLE_WEBTOONS} (id) CASCADE,
    #         artist_id   INTEGER REFERENCES {TABLE_ARTISTS} (id) CASCADE
    #     )
    # """
    
    # qr_create_table_webtoon_day = f"""
    #     CREATE TABLE {TABLE_WT_DAY} (
    #         webtoon_id  INTEGER REFERENCES {TABLE_WEBTOONS} (id) CASCADE,
    #         day_id      INTEGER REFERENCES {TABLE_DAYS} (id) CASCADE
    #     )
    # """
    try:
        cursor.execute(qr_create_table_webtoon)
        # cursor.execute(qr_create_table_genre)
        # cursor.execute(qr_create_table_artist)
        # cursor.execute(qr_create_table_days)
        # cursor.execute(qr_create_table_webtoon_genre)
        # cursor.execute(qr_create_table_webtoon_artist)
        # cursor.execute(qr_create_table_webtoon_day)

        connection.commit()
    except Exception as e:
        db_close(connection, cursor)
        return print("EXCEPTION : ", e)

    return print("table created")


def process():
    connection, cursor = db_init()
    
    webtoons = crawler.collect_naver_data()
    create_tables(connection,cursor)
    # db_truncate(connection, cursor)
    update(connection,cursor,data=webtoons)

    db_close(connection,cursor)

process()
