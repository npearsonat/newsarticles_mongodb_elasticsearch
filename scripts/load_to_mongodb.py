import pandas as pd
from pymongo import MongoClient

# Configuration - UPDATE WITH YOUR CREDENTIALS
MONGO_CONNECTION = "mongodb+srv://username:password@cluster.mongodb.net/"
CSV_FILE = "articles.csv"  # Update with your CSV filename
DATABASE_NAME = "news_db"
COLLECTION_NAME = "articles"

def load_articles_to_mongodb():
    """Load articles from CSV into MongoDB"""
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    client = MongoClient(MONGO_CONNECTION)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Read CSV
    print(f"Reading CSV file: {CSV_FILE}")
    df = pd.read_csv(CSV_FILE)
    print(f"Found {len(df)} articles in CSV")
    
    # Convert DataFrame to list of dictionaries
    articles = df.to_dict('records')
    
    # Insert into MongoDB
    print("Inserting articles into MongoDB...")
    result = collection.insert_many(articles)
    
    print(f"✓ Successfully inserted {len(result.inserted_ids)} articles!")
    
    # Verify
    count = collection.count_documents({})
    print(f"✓ Total documents in collection: {count}")
    
    # Close connection
    client.close()
    print("✓ Done!")

if __name__ == "__main__":
    load_articles_to_mongodb()