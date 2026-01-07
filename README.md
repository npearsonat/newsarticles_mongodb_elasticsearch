# newsarticles_mongodb_elasticsearch

# News Search Engine with MongoDB and Elasticsearch

A full-text search engine for news articles using MongoDB for data storage and Elasticsearch for fast, relevance-ranked searching.

## Project Overview

This project demonstrates a modern data architecture pattern combining NoSQL document storage with specialized search capabilities:

- **MongoDB Atlas**: Stores 50,000+ news articles from various publications
- **Elasticsearch**: Provides fast full-text search with relevance scoring across ~12,000 indexed articles
- **Python**: ETL pipeline and search interface

## Architecture
```
CSV Data → MongoDB (document storage) → Elasticsearch (search index) → Search Results
```

**MongoDB** serves as the primary data store while **Elasticsearch** indexes the data for optimized search queries, demonstrating how complementary database technologies work together in production systems.

## Features

- Full-text search across article titles and content
- Relevance scoring using Elasticsearch's BM25 algorithm
- Search across 12,000+ news articles from publications like NY Times, Breitbart, etc.
- Filter by publication, author, date, and year
- Fast query performance (searches complete in milliseconds)

## Dataset

The project uses a news articles dataset containing:
- 50,000+ articles from major publications
- Fields: title, content, author, publication, date, year, month, url
- Source: [Kaggle - All the News dataset or similar]

## Technologies Used

- **Python 3.x**
- **MongoDB Atlas** - Cloud NoSQL database
- **Elasticsearch 8.11** - Search and analytics engine
- **Docker** - Containerization for Elasticsearch
- **pymongo** - MongoDB Python driver
- **elasticsearch** - Elasticsearch Python client
- **pandas** - Data manipulation

## Setup Instructions

### Prerequisites

- Python 3.x installed
- Docker Desktop installed and running
- MongoDB Atlas account (free tier)

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/news-search-engine.git
cd news-search-engine
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up MongoDB Atlas

1. Create a free MongoDB Atlas account
2. Create a cluster and database named `news_db`
3. Create a collection named `articles`
4. Whitelist your IP address or use 0.0.0.0/0 for testing
5. Create a database user with read/write permissions
6. Copy your connection string

### 4. Set up Elasticsearch with Docker
```bash
docker run -d --name elasticsearch -p 9200:9200 -p 9300:9300 \
  -e "discovery.type=single-node" \
  -e "xpack.security.enabled=false" \
  docker.elastic.co/elasticsearch/elasticsearch:8.11.0
```

Verify Elasticsearch is running:
```bash
curl http://localhost:9200
```

### 5. Configure connection strings

Update the MongoDB connection string in the scripts with your credentials:
```python
mongo_connection = "mongodb+srv://username:password@cluster.mongodb.net/"
```

### 6. Load data into MongoDB
```bash
python scripts/load_to_mongodb.py
```

This will load your CSV file into MongoDB (takes ~1-2 minutes for 50k articles).

### 7. Index data into Elasticsearch
```bash
python scripts/index_to_elasticsearch.py
```

This indexes articles from MongoDB into Elasticsearch (takes ~10 minutes per 10k articles).

### 8. Run search demo
```bash
python scripts/search_demo.py
```

## Usage Examples

### Basic search:
```python
from elasticsearch import Elasticsearch

es = Elasticsearch(['http://localhost:9200'])

search_query = {
    "query": {
        "multi_match": {
            "query": "climate change",
            "fields": ["title", "content"]
        }
    }
}

results = es.search(index='news_articles', body=search_query)
```

### Search with filters:
```python
search_query = {
    "query": {
        "bool": {
            "must": {
                "multi_match": {
                    "query": "election",
                    "fields": ["title", "content"]
                }
            },
            "filter": [
                {"term": {"publication": "New York Times"}},
                {"range": {"year": {"gte": 2016}}}
            ]
        }
    }
}
```

## Sample Search Results

**Query: "climate change"**
- Found 2,645 relevant articles
- Top result: "In America's Heartland, Discussing Climate Change Without Saying 'Climate Change'" (Score: 13.55)
- Search completed in < 100ms

**Query: "healthcare policy"**
- Demonstrates relevance ranking across political and policy articles

## Project Structure
```
news-search-engine/
├── scripts/
│   ├── load_to_mongodb.py          # Load CSV into MongoDB
│   ├── index_to_elasticsearch.py   # Index MongoDB data to Elasticsearch
│   └── search_demo.py              # Demo search functionality
├── screenshots/                     # Project screenshots
├── README.md                        # This file
├── requirements.txt                 # Python dependencies
└── .gitignore                      # Git ignore file
```

## Key Learnings

- **When to use MongoDB vs SQL**: Document databases excel with semi-structured data and flexible schemas
- **Elasticsearch architecture**: Understanding inverted indexes and relevance scoring (BM25)
- **ETL pipelines**: Extracting data from one system, transforming it, and loading into another
- **Docker containerization**: Deploying services in isolated, reproducible environments
- **Data cleaning**: Handling NaN values and data quality issues during ETL

## Future Enhancements

- [ ] Build web interface with Flask/Streamlit
- [ ] Add autocomplete functionality
- [ ] Implement faceted search (filter by multiple criteria)
- [ ] Add data visualization dashboard
- [ ] Implement pagination for large result sets
- [ ] Add fuzzy matching for typo tolerance

## Challenges Overcome

1. **MongoDB Atlas connection timeouts** - Resolved by properly configuring Network Access IP whitelist
2. **Elasticsearch version compatibility** - Matched Python client version with server version
3. **NaN handling in data** - Implemented data cleaning to convert NaN to empty strings before indexing
4. **Performance optimization** - Batching could further improve indexing speed
