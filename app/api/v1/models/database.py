import os

import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    """Initialization."""

    def __init__(self):
        self.db_name = os.getenv('DB_NAME')
        self.db_host = os.getenv('DB_HOST')
        self.db_user = os.getenv('DB_USER')
        self.db_password = os.getenv('DB_PASSWORD')
        self.conn = psycopg2.connect(
            database=self.db_name, host=self.db_host, user=self.db_user, password=self.db_password)
        self.curr = self.conn.cursor(cursor_factory=RealDictCursor)

    def create_table(self):
        """Create tables."""
        queries = [
            """
            CREATE TABLE IF NOT EXISTS users(
                user_id serial PRIMARY KEY,
                firstname varchar NOT NULL,
                lastname varchar NOT NULL,
                phone varchar NOT NULL,
                username varchar NOT NULL,
                email varchar NOT NULL,
                password varchar NOT NULL,
                date TIMESTAMP
            )"""
        ]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return e

    def create_admin(self):
        """Create a deafult admin user."""
        query = "INSERT INTO users(firstname,lastname,phone,username,email, password)\
        VALUES('Harun','Gachanja','0711371265','Arrotech','admin@admin.com','pbkdf2:sha256:50000$aNlgJU9E$bf5d2dc9783e38f905618aacd50eb55b098f282dc6b03834aee7c4f80a9100e8')"
        self.curr.execute(query)
        self.conn.commit()
        self.curr.close()

    def destroy_table(self):
        """Destroy tables"""
        users = "DROP TABLE IF EXISTS  users CASCADE"
        queries = [users]
        try:
            for query in queries:
                self.curr.execute(query)
            self.conn.commit()
            self.curr.close()
        except Exception as e:
            return e

    def fetch(self, query):
        """Fetch all query."""
        self.curr.execute(query)
        fetch_all = self.curr.fetchall()
        self.conn.commit()
        self.curr.close()
        return fetch_all

    def fetch_one(self, query):
        """Fetch one query."""
        self.curr.execute(query)
        fetch_one = self.curr.fetchone()
        self.conn.commit()
        self.curr.close()
        return fetch_one

if __name__ == '__main__':
    Database().destroy_table()
    Database().create_table()
