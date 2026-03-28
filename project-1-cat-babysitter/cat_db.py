import sqlite3

class BD:

    def __init__(self):
        self.conn = sqlite3.connect("cats.db")
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

    def insert(self, owner, cat, days, price, city):
        cursor = self.conn.cursor()

        cursor.execute(
            "INSERT INTO bookings(owner_name, cat_name, days, price_per_day, city) VALUES (?,?,?,?,?)",
            (owner, cat, days, price, city)
        )

        self.conn.commit()
        id = cursor.lastrowid
        cursor.close()
        return id

    def get(self, id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bookings WHERE id=?", (id,))
        result = cursor.fetchone()
        cursor.close()
        return result

    def update(self, id, owner, cat, days, price, city):
        cursor = self.conn.cursor()
        cursor.execute(
            "UPDATE bookings SET owner_name=?, cat_name=?, days=?, price_per_day=?, city=? WHERE id=?",
            (owner, cat, days, price, city, id)
        )
        self.conn.commit()
        cursor.close()

    def delete(self, id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM bookings WHERE id=?", (id,))
        self.conn.commit()
        cursor.close()

    def list(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bookings")
        result = cursor.fetchall()
        cursor.close()
        return result