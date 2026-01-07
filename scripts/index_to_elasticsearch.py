from elasticsearch import Elasticsearch
from pymongo import MongoClient
import math

# Configuration - UPDATE WITH YOUR CREDENTIALS
MONGO_CONNECTION = "mongodb+srv://username:password@cluster.mongodb.net/"
ELASTICSEARCH_HOST = "http://localhost:9200"
DATABASE_NAME = "news_db"
COLLECTION_NAME = "articles"
INDEX_NAME = "news_articles"
LIMIT = None  # Set to a number like 5000 to index fewer articles, or None for all

def clean_value(value):
    """Clean NaN values for Elasticsearch compatibility"""
    if isinstance(value, float) and math.isnan(value):
        return ''
    return value if value is not None else ''

def index_articles():
    """Index articles from MongoDB into Elasticsearch"""
    
    # Connect to MongoDB
    print("Connecting to MongoDB...")
    mongo_client = MongoClient(MONGO_CONNECTION)
    db = mongo_client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Connect to Elasticsearch
    print("Connecting to Elasticsearch...")
    es = Elasticsearch([ELASTICSEARCH_HOST])
    
    # Create index
    print(f"Creating Elasticsearch index: {INDEX_NAME}")
    try:
        es.indices.create(
            index=INDEX_NAME,
            body={
                "settings": {
                    "number_of_shards": 1,
                    "number_of_replicas": 0
                }
            }
        )
        print(f"✓ Created index: {INDEX_NAME}")
    except Exception as e:
        print(f"Index might already exist: {e}")
    
    # Fetch and index articles
    print("Starting to index articles...")
    query = collection.find()
    if LIMIT:
        query = query.limit(LIMIT)
        print(f"Limiting to {LIMIT} articles")
    
    count = 0
    errors = 0
    
    for article in query:
        try:
            # Prepare document with cleaned values
            doc = {
                'title': clean_value(article.get('title', '')),
                'content': clean_value(article.get('content', '')),
                'author': clean_value(article.get('author', '')),
                'publication': clean_value(article.get('publication', '')),
                'date': clean_value(article.get('date', '')),
                'year': clean_value(article.get('year', '')),
                'month': clean_value(article.get('month', '')),
                'url': clean_value(article.get('url', ''))
            }
            
            # Index into Elasticsearch
            es.index(index=INDEX_NAME, id=str(article['_id']), document=doc)
            
            count += 1
            if count % 1000 == 0:
                print(f"Indexed {count} articles...")
                
        except Exception as e:
            errors += 1
            if errors < 5:
                print(f"Error indexing article: {e}")
    
    print(f"✓ Done! Indexed: {count} articles, Errors: {errors}")
    
    # Verify count
    result = es.count(index=INDEX_NAME)
    print(f"✓ Total articles in Elasticsearch: {result['count']}")
    
    # Close connections
    mongo_client.close()

if __name__ == "__main__":
    index_articles()