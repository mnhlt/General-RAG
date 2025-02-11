# POE2DB Crawler

A simple web crawler for extracting content from POE2DB and updating the knowledge base.

## Directory Structure

```
crawler/
├── data/           # Stores crawled data in JSON format
├── logs/           # Contains crawler logs
├── poe2db_crawler.py  # Main crawler implementation
└── cli.py          # Command-line interface
```

## Features

- Crawls POE2DB pages and extracts structured content
- Saves crawled data to JSON files with timestamps
- Updates knowledge base through API endpoint
- Detailed logging of crawling process
- Command-line interface for easy usage

## Usage

1. Make sure the knowledge base API is running at `http://localhost:8000`

2. Run the crawler using the CLI:
```bash
python cli.py https://poe2db.tw/us/Items
```

3. Check the logs in `crawler/logs/crawler.log` for detailed information

4. Crawled data is saved in `crawler/data/` as JSON files

## Data Format

The crawler saves data in the following format:
```json
{
  "url": "https://poe2db.tw/us/Items",
  "content": "Extracted content...",
  "timestamp": "2024-02-11T12:34:56.789Z"
}
```

## Requirements

- Python 3.8+
- beautifulsoup4
- requests

## Error Handling

The crawler includes comprehensive error handling and logging:
- Network errors
- Parsing errors
- File system errors
- API communication errors

All errors are logged to both console and log file. 