# News Search Engine with MongoDB and Elasticsearch

## Overview

This project is a full-text search engine built for exploring news articles at scale. It demonstrates how modern data architectures combine different database technologies to handle storage and search operations efficiently. The system uses MongoDB Atlas as the primary document store for over 50,000 news articles, while Elasticsearch provides fast, relevance-ranked search capabilities across approximately 12,000 indexed articles. The entire pipeline is built in Python, showcasing practical data engineering skills including ETL processes, NoSQL databases, containerization with Docker, and search engine implementation.

## The Dataset

The foundation of this project is a comprehensive news articles dataset containing over 50,000 articles from major publications including The New York Times, Breitbart, and other prominent sources. Each article in the dataset includes structured fields: a unique identifier, title, full content text, author name, publication name, publication date (broken down into date, year, and month fields), and the original URL. This data structure provides both the rich text content needed for full-text search and the metadata necessary for filtering and organization. The dataset comes from publicly available news article collections, demonstrating real-world data with all its complexity—including missing values, inconsistent formatting, and varying content lengths.

## Building the MongoDB Foundation

![Detection Demo](screenshots/MongoDB_Compass.png)

The first step in the project was establishing a reliable data storage layer using MongoDB Atlas, MongoDB's cloud-hosted database service. MongoDB was chosen for this project because it handles semi-structured document data naturally, making it ideal for articles that might vary in their field completeness or structure. Setting up MongoDB Atlas involved creating a free-tier cluster, configuring network access to allow connections from my development environment, and establishing a database user with appropriate permissions.

Once the infrastructure was in place, I loaded the CSV dataset into MongoDB using Python's pandas library to read the file and pymongo to handle the database operations. The process converted each row of the CSV into a JSON-like document that MongoDB stores in BSON format. All 50,000 articles were inserted into a collection called "articles" within a database named "news_db". This took approximately one to two minutes to complete. The data is now accessible through MongoDB Compass, MongoDB's GUI tool, where you can browse through the documents, examine individual articles, and verify the data structure. Each document retains its original fields from the CSV, making it straightforward to query by author, publication, date, or any other metadata field.

## Integrating Elasticsearch for Search

![Detection Demo](screenshots/docker_desktop_screenshop.png)

With the data safely stored in MongoDB, the next phase involved setting up Elasticsearch to enable sophisticated search capabilities. While MongoDB can handle basic queries, Elasticsearch specializes in full-text search with features like relevance scoring, fuzzy matching, and complex text analysis. I deployed Elasticsearch locally using Docker, which provided an isolated, reproducible environment without requiring a complex installation process. The Docker container runs Elasticsearch version 8.11 on port 9200, and starting it is as simple as running a single docker command.

The integration between MongoDB and Elasticsearch required building an ETL (Extract, Transform, Load) pipeline. This pipeline reads documents from MongoDB, cleans the data to handle edge cases like NaN values that would cause Elasticsearch to reject the documents, and then indexes each article into Elasticsearch. The indexing process analyzes the text content, breaking it down into searchable tokens and building inverted indexes that make searches incredibly fast. I indexed approximately 12,000 articles, which took around 10-15 minutes as each article's title and content were processed and stored. This subset of the full dataset is more than sufficient to demonstrate the search capabilities while keeping indexing time reasonable for a portfolio project.

## Search Functionality and Results

![Detection Demo](screenshots/Elastic_Search_Example_Search_2.png)

With both databases operational, the system can now perform sophisticated searches across thousands of news articles in milliseconds. Elasticsearch uses the BM25 algorithm for relevance scoring, which considers how frequently search terms appear in a document, how rare those terms are across the entire collection, and other factors to rank results. When searching for "climate change," the system found 2,645 matching articles and returned the most relevant ones first. The top result, scoring 13.55, was an article titled "In America's Heartland, Discussing Climate Change Without Saying 'Climate Change'" from The New York Times—clearly a highly relevant match given that the search terms appear multiple times in the title alone.

The search capabilities extend beyond simple keyword matching. The system can search across both article titles and content, with titles weighted more heavily since they're typically more indicative of an article's main topic. You can also combine text search with filters, such as limiting results to specific publications, date ranges, or authors. The multi-match query structure allows for flexible searching where terms don't need to appear in exact order, and Elasticsearch's text analysis handles variations in word forms automatically. Every search completes in well under 100 milliseconds, demonstrating how Elasticsearch's specialized architecture outperforms general-purpose databases for search-heavy workloads.

## Architecture and Design Decisions

This project illustrates a common pattern in production systems where different database technologies complement each other. MongoDB serves as the operational database—the source of truth where all article data lives permanently. It provides reliable storage, easy document updates, and straightforward data retrieval when you need complete articles. Elasticsearch, on the other hand, is optimized for one thing: search. It maintains its own copy of the data in a format that makes text searching and ranking extremely fast, but it's not designed to be your primary data store. This separation of concerns means each system does what it does best.

The choice to use Docker for Elasticsearch deployment reflects modern development practices where containerization provides consistency across different environments. The same Docker command that runs Elasticsearch on my machine would work on any other system with Docker installed, making the project reproducible and easy to set up. MongoDB Atlas was chosen for its managed service benefits—no need to maintain servers or worry about backups, just focus on building the application. These technology choices demonstrate an understanding of when to use cloud services versus local development tools.

## Technical Implementation

The entire project is implemented in Python, leveraging several key libraries. The pymongo library provides the interface to MongoDB, handling connection management and CRUD operations. The elasticsearch Python client communicates with the Elasticsearch API, translating Python dictionaries into the JSON queries that Elasticsearch expects. Pandas facilitated the initial data loading from CSV format. The data cleaning logic handles edge cases like NaN values that appear in the dataset where information is missing—converting these to empty strings prevents Elasticsearch from rejecting documents during indexing.

One challenge encountered during development was version compatibility between the Elasticsearch Python client and the Elasticsearch server. The solution required ensuring the client library version matched the server's major version. Another consideration was performance—indexing 12,000 articles sequentially takes time, and the code includes progress indicators every 1,000 articles to provide feedback during the lengthy process. In a production environment, this could be optimized with bulk indexing operations, but the current approach clearly demonstrates the indexing mechanics.

## Project Outcomes and Applications

This search engine demonstrates several valuable technical competencies. It shows understanding of NoSQL databases and when document stores like MongoDB make sense versus traditional relational databases. The Elasticsearch integration demonstrates knowledge of specialized search technologies and how they fit into larger system architectures. The Docker deployment shows familiarity with containerization and modern development practices. The ETL pipeline illustrates data engineering skills—extracting from one source, transforming to handle data quality issues, and loading into another system.

From a practical standpoint, this architecture pattern appears in many real-world applications. News websites use similar setups to power their search features. E-commerce platforms combine operational databases with search engines to provide product search and filtering. Content management systems rely on this pattern to make large document collections searchable. The skills demonstrated here—working with multiple database technologies, building data pipelines, handling real-world messy data—are directly applicable to professional data engineering and backend development roles.

## Technologies Used

- **Python 3.x** - Primary programming language for all scripts and data processing
- **MongoDB Atlas** - Cloud-hosted NoSQL document database for article storage
- **Elasticsearch 8.11** - Search and analytics engine deployed via Docker
- **Docker Desktop** - Container platform for running Elasticsearch locally
- **pymongo** - Official MongoDB driver for Python
- **elasticsearch** - Official Elasticsearch client library for Python
- **pandas** - Data manipulation library used for CSV processing

## Setup Requirements

To run this project locally, you'll need Python 3.x installed along with the following Python packages:
```txt
pymongo==4.6.1
elasticsearch==8.11.1
pandas==2.1.4
