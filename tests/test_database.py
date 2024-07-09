# -*- coding: utf-8 -*-
import unittest
import sqlite3
from crate_tables import create_connection, create_tables, add_trip, add_person, add_person_to_trip, add_trip_details, delete_trip, get_trips

class TestDatabaseFunctions(unittest.TestCase):

    def setUp(self):
        self.conn = create_connection(":memory:")
        create_tables(self.conn)
        trip = ('Trip to Paris', 'France', 1200.00, '2023-06-01', '2023-06-10')
        add_trip(self.conn, trip)

    def tearDown(self):
        self.conn.close()

    def test_add_trip(self):
        trip = ('Trip to Paris', 'France', 1200.00, '2023-06-01', '2023-06-10')
        trip_id = add_trip(self.conn, trip)
        self.assertIsNotNone(trip_id)

    def test_add_person(self):
        person = ('John Doe', 30, '1234567890')
        person_id = add_person(self.conn, person)
        self.assertIsNotNone(person_id)

    def test_add_person_to_trip(self):
        trip = ('Trip to Paris', 'France', 1200.00, '2023-06-01', '2023-06-10')
        trip_id = add_trip(self.conn, trip)
        person = ('John Doe', 30, '1234567890')
        person_id = add_person(self.conn, person)
        add_person_to_trip(self.conn, person_id, trip_id)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM PeopleTrips WHERE person_id=? AND trip_id=?", (person_id, trip_id))
        self.assertIsNotNone(cur.fetchone())

    def test_add_trip_details(self):
        trip = ('Trip to Paris', 'France', 1200.00, '2023-06-01', '2023-06-10')
        trip_id = add_trip(self.conn, trip)
        tripdetails = (trip_id, 'Guided tour of Paris', 'Jane Doe')
        tripdetails_id = add_trip_details(self.conn, tripdetails)
        self.assertIsNotNone(tripdetails_id)

    def test_delete_trip(self):
        trip = ('Trip to Paris', 'France', 1200.00, '2023-06-01', '2023-06-10')
        trip_id = add_trip(self.conn, trip)
        delete_trip(self.conn, trip_id)
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM Trips WHERE id=?", (trip_id,))
        self.assertIsNone(cur.fetchone())

    def test_get_trips(self):
        trips = get_trips(self.conn)
        self.assertIsNotNone(trips)
        self.assertGreaterEqual(len(trips), 1, "Expected at least one trip in the database")

if __name__ == '__main__':
    unittest.main()


