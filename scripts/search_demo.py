from elasticsearch import Elasticsearch

# Configuration
ELASTICSEARCH_HOST = "http://localhost:9200"
INDEX_NAME = "news_articles"

def search_articles(query_text, num_results=5):
    """Search for articles"""
    
    # Connect to Elasticsearch
    es = Elasticsearch([ELASTICSEARCH_HOST])
    
    # Build search query
    search_query = {
        "query": {
            "multi_match": {
                "query": query_text,
                "fields": ["title^2", "content"]  # Title weighted 2x more
            }
        },
        "size": num_results
    }
    
    # Execute search
    results = es.search(index=INDEX_NAME, body=search_query)
    
    # Display results
    total = results['hits']['total']['value']
    print(f"\n{'='*80}")
    print(f"Search: '{query_text}'")
    print(f"Found {total} matching articles")
    print(f"{'='*80}\n")
    
    for i, hit in enumerate(results['hits']['hits'], 1):
        article = hit['_source']
        score = hit['_score']
        
        print(f"{i}. Score: {score:.2f}")
        print(f"   Title: {article['title']}")
        print(f"   Author: {article['author']}")
        print(f"   Publication: {article['publication']}")
        print(f"   Date: {article['date']}")
        print(f"   Preview: {article['content'][:150]}...")
        print()

def main():
    """Run demo searches"""
    
    # Example searches
    queries = [
        "climate change",
        "election results",
        "healthcare policy",
        "Trump administration"
    ]
    
    for query in queries:
        search_articles(query, num_results=3)
        input("Press Enter for next search...")

if __name__ == "__main__":
    main()