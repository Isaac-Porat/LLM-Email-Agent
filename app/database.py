import sqlite3
from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator=' ', strip=True)

class EmailDatabase:
    def __init__(self, db_name='emails.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS emails (
            id INTEGER PRIMARY KEY,
            sender TEXT,
            body TEXT,
            sent_date TEXT
        )
        ''')
        self.conn.commit()

    def insert_email(self, sender, body, sent_date):
        cursor = self.conn.cursor()
        cursor.execute('''
        INSERT INTO emails (sender, body, sent_date)
        VALUES (?, ?, ?)
        ''', (sender, body, sent_date))
        self.conn.commit()

    def get_all_emails(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM emails')
        return cursor.fetchall()

    def close(self):
        self.conn.close()