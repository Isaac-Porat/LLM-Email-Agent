import asyncio
import sqlite3
from app.email.graph import Graph
from app.database.database import EmailDatabase, clean_html

def create_emails_table(db):
    cursor = db.conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS emails (
        id INTEGER PRIMARY KEY,
        sender TEXT,
        body TEXT,
        sent_date TEXT,
        UNIQUE(sender, sent_date)
    )
    ''')
    db.conn.commit()

async def main():
    graph = Graph()
    db = EmailDatabase()

    if not db.table_exists():
        print("The 'emails' table does not exist. Creating it now.")
        create_emails_table(db)

    token = await graph.get_user_token()
    print("User token acquired")

    messages = await graph.get_inbox()

    if messages and messages.value:
        for message in messages.value:
            sender = message.from_.email_address.address if message.from_ and message.from_.email_address else 'NONE'
            body = clean_html(message.body.content) if message.body and message.body.content else 'No body content'
            sent_date = message.sent_date_time.isoformat() if message.sent_date_time else 'NONE'

            try:
                db.upsert_email(sender, body, sent_date)
                print(f"Upserted email from {sender} sent on {sent_date}")
            except sqlite3.Error as e:
                print(f"An error occurred while upserting the email: {e}")

        print("\nAll emails processed. Here's what we have in the database:")
        for email in db.get_all_emails():
            print(f"ID: {email[0]}, From: {email[1]}, Date: {email[3]}, Body preview: {email[2][:50]}...")
    else:
        print("No messages found.")

    db.close()

if __name__ == "__main__":
    asyncio.run(main())