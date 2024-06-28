import asyncio
from graph import Graph
from bs4 import BeautifulSoup

def clean_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text(separator='\n', strip=True)

async def main():
    graph = Graph()

    token = await graph.get_user_token()
    print("User token:", token[:10] + "..." + token[-10:])

    messages = await graph.get_inbox()

    if messages and messages.value:
        for message in messages.value:
            print(f"Subject: {message.subject}")
            print(f"From: {message.from_.email_address.address if message.from_ and message.from_.email_address else 'NONE'}")
            print(f"Read: {'Yes' if message.is_read else 'No'}")
            print(f"Received: {message.received_date_time}")
            print("Body:")
            if message.body and message.body.content:
                if message.body.content_type == 'html':
                    print(clean_html(message.body.content))
                else:
                    print(message.body.content)
            else:
                print("No body content")
            print("---" * 30)
    else:
        print("No messages found.")

if __name__ == "__main__":
    asyncio.run(main())