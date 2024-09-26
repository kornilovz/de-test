
import pymysql.cursors
import pandas as pd
from sqlalchemy import create_engine

def change_date(df, column):
    df[column] = pd.to_datetime(df[column])

def change_time(df, column):
    df[column] = pd.to_datetime(df[column], format='%H:%M:%S').dt.time

def create_query(sql_query, connect):
    with connect.cursor() as cursor:
        with cursor:
            cursor.execute(sql_query)

def load_data(df, str_table_sql, str_user, str_pass, str_database, chunk_size, name_table):
    engine = create_engine(f"mysql+pymysql://{str_user}:{str_pass}@mydb:3306/{str_database}")
    len_df = len(df)
    count_chunks = (len_df // chunk_size) + 1
    for i in range(0, len(df), chunk_size):
        df_chunk = df[i:i + chunk_size]
        df_chunk.to_sql(str_table_sql, con=engine, if_exists='append', index=False)
        print(f"Часть {i // chunk_size + 1} из {count_chunks} загружено в таблицу {name_table}")


def return_query(sql_query, connect):
    with connect.cursor() as cursor:
        cursor.execute(sql_query)
        result = cursor.fetchall() # Прочитать все результаты
    return result


def main():
    user = 'admin'
    database = 'sber_db'
    password = 'admin'
    ga_session_name = 'ga_session'
    ga_hits_name = 'ga_hits'

    conn = pymysql.connect(
        host='mydb',
        port=3306,
        user=user,
        password=password,
        database=database,
        cursorclass=pymysql.cursors.DictCursor)

    sql_session = ("create table ga_session(session_id varchar(60) not null primary key,"
                   "client_id varchar(50),"
                   #"visit_date datetime,"
                   #"visit_time TIME,"
                   "visit_date varchar(20),"
                   "visit_time varchar(8),"
                   "visit_number int,"
                   "utm_source varchar(30),"
                   "utm_medium varchar(30),"
                   "utm_campaign varchar(30),"
                   "utm_adcontent varchar(30),"
                   "utm_keyword varchar(30),"
                   "device_category varchar(10),"
                   "device_os varchar(20),"
                   "device_brand varchar(20),"
                   "device_model varchar(30),"
                   "device_screen_resolution varchar(20),"
                   "device_browser varchar(40),"
                   "geo_country varchar(30),"
                   "geo_city varchar(40));")

    sql_hits = ("create table ga_hits(id INT AUTO_INCREMENT not null primary key,"
                "session_id varchar(60),"
                #"hit_date datetime,"
                "hit_date varchar(20),"
                "hit_time float,"
                "hit_number int,"
                "hit_type varchar(10),"
                "hit_referer varchar(30),"
                "hit_page_path varchar(2000),"
                "event_category varchar(40),"
                "event_action varchar(50),"
                "event_label varchar(30),"
                "event_value varchar(10));")

    def create_df_session():

        df_sessions = pd.read_parquet('data/ga_sessions.parquet.gz')
        change_date(df_sessions, 'visit_date')
        change_time(df_sessions, 'visit_time')
        create_query(sql_session, conn)
        load_data(df_sessions, ga_session_name, user, password, database, 60000, 'ga_session')

    def create_df_hits():
        df_hits = pd.read_parquet('data/ga_hits.parquet.gz')
        change_date(df_hits, 'hit_date')
        create_query(sql_hits, conn)
        load_data(df_hits, ga_hits_name, user, password, database, 30000, 'ga_hits')

    tables = [x['Tables_in_sber_db'] for x in return_query("show tables;", conn)]

    if 'ga_session' in tables:
        print('Таблица ga_session уже присутствует в базе')
    else:
        create_df_session()

    if 'ga_session' in tables:
        print('Таблица ga_hits уже присутствует в базе')
    else:
        create_df_hits()

    print('Изначальные данные загружены')

if __name__ == '__main__':
    main()
