import argparse
import logging
import asyncio
from poe2db_crawler import POE2DBCrawler

async def main():
    parser = argparse.ArgumentParser(description='POE2DB Crawler CLI')
    parser.add_argument('url', help='URL to crawl')
    
    args = parser.parse_args()
    
    crawler = POE2DBCrawler()
    success = await crawler.process_url(args.url)
    
    if success:
        print("Crawling completed successfully!")
    else:
        print("Crawling failed. Check the logs for details.")

if __name__ == "__main__":
    asyncio.run(main()) 