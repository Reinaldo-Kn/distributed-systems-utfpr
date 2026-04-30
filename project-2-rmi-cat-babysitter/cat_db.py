import sqlite3
import threading
from booking import Booking

class CatBookingCRUD:

    def __init__(self):
        self.conn = sqlite3.connect("cats.db", check_same_thread=False)
        self.lock = threading.Lock()
        cursor = self.conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY,
            owner_name TEXT,
            cat_name TEXT,
            days INTEGER,
            price_per_day REAL,
            city TEXT
        )
        """)

        self.conn.commit()
        cursor.close()

    def create_booking(self, booking: Booking):
        with self.lock:
            cursor = self.conn.cursor()

            cursor.execute(
                "INSERT INTO bookings(owner_name, cat_name, days, price_per_day, city) VALUES (?,?,?,?,?)",
                (
                    booking.owner_name,
                    booking.cat_name,
                    booking.days,
                    booking.price_per_day,
                    booking.city,
                )
            )

            self.conn.commit()
            id = cursor.lastrowid
            cursor.close()
        return Booking(
            id=id,
            owner_name=booking.owner_name,
            cat_name=booking.cat_name,
            days=booking.days,
            price_per_day=booking.price_per_day,
            city=booking.city,
        )

    def read_booking(self, id):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bookings WHERE id=?", (id,))
            result = cursor.fetchone()
            cursor.close()
        if result is None:
            return None
        return Booking(
            id=result[0],
            owner_name=result[1],
            cat_name=result[2],
            days=result[3],
            price_per_day=result[4],
            city=result[5],
        )

    def update_booking(self, id, booking: Booking):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute(
                "UPDATE bookings SET owner_name=?, cat_name=?, days=?, price_per_day=?, city=? WHERE id=?",
                (
                    booking.owner_name,
                    booking.cat_name,
                    booking.days,
                    booking.price_per_day,
                    booking.city,
                    id,
                )
            )
            updated = cursor.rowcount > 0
            self.conn.commit()
            cursor.close()
        return updated

    def delete_booking(self, id):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM bookings WHERE id=?", (id,))
            deleted = cursor.rowcount > 0
            self.conn.commit()
            cursor.close()
        return deleted

    def list_bookings(self):
        with self.lock:
            cursor = self.conn.cursor()
            cursor.execute("SELECT * FROM bookings")
            result = cursor.fetchall()
            cursor.close()
        return [
            Booking(
                id=row[0],
                owner_name=row[1],
                cat_name=row[2],
                days=row[3],
                price_per_day=row[4],
                city=row[5],
            )
            for row in result
        ]


# Backward compatibility alias
BD = CatBookingCRUD
