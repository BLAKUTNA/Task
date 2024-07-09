# -*- coding: utf-8 -*-
import sqlite3
import os

def create_connection(db_file):
    # Створюємо директорію, якщо вона не існує
    if not os.path.exists(os.path.dirname(db_file)):
        try:
            os.makedirs(os.path.dirname(db_file))
        except OSError as e:
            print(f"Error creating directory: {e}")
    conn = sqlite3.connect(db_file)
    return conn

def create_tables(conn):
    sql_create_trips_table = """
    CREATE TABLE IF NOT EXISTS Trips (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        country TEXT NOT NULL,
        price REAL,
        day_start TEXT,
        day_finish TEXT
    );"""

    sql_create_people_table = """
    CREATE TABLE IF NOT EXISTS People (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        age INTEGER,
        phone_number TEXT
    );"""

    sql_create_peopletrips_table = """
    CREATE TABLE IF NOT EXISTS PeopleTrips (
        person_id INTEGER,
        trip_id INTEGER,
        PRIMARY KEY (person_id, trip_id),
        FOREIGN KEY (person_id) REFERENCES People (id),
        FOREIGN KEY (trip_id) REFERENCES Trips (id)
    );"""

    try:
        c = conn.cursor()
        c.execute(sql_create_trips_table)
        c.execute(sql_create_people_table)
        c.execute(sql_create_peopletrips_table)
    except sqlite3.Error as e:
        print(f"Error creating tables: {e}")

def add_trip(conn, trip):
    sql = ''' INSERT INTO Trips(name, country, price, day_start, day_finish)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, trip)
    conn.commit()
    return cur.lastrowid

def add_person(conn, person):
    sql = ''' INSERT INTO People(name, age, phone_number)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, person)
    conn.commit()
    return cur.lastrowid

def add_person_to_trip(conn, person_id, trip_id):
    sql = ''' INSERT INTO PeopleTrips(person_id, trip_id)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, (person_id, trip_id))
    conn.commit()

def add_trip_details(conn, tripdetails):
    sql = ''' INSERT INTO TripDetails(tripid, description, guide_name)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, tripdetails)
    conn.commit()
    return cur.lastrowid

def delete_trip(conn, id):
    sql = 'DELETE FROM Trips WHERE id=?'
    cur = conn.cursor()
    cur.execute(sql, (id,))
    conn.commit()

def get_trips(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Trips")

    rows = cur.fetchall()

    return rows  # Повертаємо всі рядки з таблиці Trips

if __name__ == '__main__':
    conn = create_connection("data/app.db")  # Шлях до файлу бази даних SQLite
    if conn is not None:
        create_tables(conn)
        conn.close()
    else:
        print("Error! Cannot create the database connection.")





