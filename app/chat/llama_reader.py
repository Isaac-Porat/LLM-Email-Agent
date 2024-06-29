import os
import sqlite3
from datetime import date
from typing import List
from dotenv import load_dotenv
from llama_index.core import Document, VectorStoreIndex
from llama_index.llms.openai import OpenAI
from llama_index.core.readers.base import BaseReader
from llama_index.core import Settings
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.vector_stores import SimpleVectorStore

load_dotenv()

class SQLiteReader(BaseReader):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def load_data(self) -> List[Document]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Get today's date in the format stored in the database
        today = date.today().isoformat()

        cursor.execute("SELECT sender, body, sent_date FROM emails WHERE sent_date LIKE ? ORDER BY sent_date DESC", (f"{today}%",))
        rows = cursor.fetchall()
        conn.close()
        documents = []
        for row in rows:
            sender, body, sent_date = row
            metadata = {
                "sender": sender,
                "sent_date": sent_date
            }
            doc = Document(text=body, metadata=metadata)
            documents.append(doc)

        return documents

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(current_dir, '..', 'database', 'emails.db')

    reader = SQLiteReader(db_path)
    documents = reader.load_data()

    print(f"Loaded {len(documents)} documents from today's date.")
    for i, doc in enumerate(documents, 1):
        print(f"\nDocument {i}:")
        print(f"Sender: {doc.metadata['sender']}")
        print(f"Sent Date: {doc.metadata['sent_date']}")
        print(f"Content Preview: {doc.text[:100]}...")

    if documents:
        Settings.llm = OpenAI(temperature=0.1, model="gpt-3.5-turbo")

        storage_context = StorageContext.from_defaults(vector_store=SimpleVectorStore())
        index = VectorStoreIndex.from_documents(
            documents,
            storage_context=storage_context,
        )

        # index.storage_context.persist(persist_dir="./email_index")

        print("\nCreated and saved VectorStoreIndex with today's documents.")

        query_engine = index.as_query_engine()
        response = query_engine.query("Summarize the main points from today's emails in a bulleted list.")
        print("\nSample query result:")
        print(response)
    else:
        print("\nNo documents found for today's date. VectorStoreIndex was not created.")

if __name__ == "__main__":
    main()