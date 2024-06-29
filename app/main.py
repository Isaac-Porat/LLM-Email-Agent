import asyncio
from graph import Graph
from database import EmailDatabase, clean_html

async def main():
    graph = Graph()
    db = EmailDatabase()

    token = await graph.get_user_token()
    print("User token acquired")

    messages = await graph.get_inbox()

    if messages and messages.value:
        for message in messages.value:
            sender = message.from_.email_address.address if message.from_ and message.from_.email_address else 'NONE'
            body = clean_html(message.body.content) if message.body and message.body.content else 'No body content'
            sent_date = message.sent_date_time.isoformat() if message.sent_date_time else 'NONE'

            db.insert_email(sender, body, sent_date)
            print(f"Inserted email from {sender} sent on {sent_date}")

        print("\nAll emails inserted into the database. Here's what we have:")
        for email in db.get_all_emails():
            print(f"ID: {email[0]}, From: {email[1]}, Date: {email[3]}, Body preview: {email[2][:50]}...")
    else:
        print("No messages found.")

    db.close()

if __name__ == "__main__":
    asyncio.run(main())