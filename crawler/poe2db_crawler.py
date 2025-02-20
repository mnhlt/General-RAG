import requests
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import os
from pathlib import Path
import asyncio
from playwright.async_api import async_playwright
import argparse

# Setup paths
CRAWLER_DIR = Path(__file__).parent
LOG_DIR = CRAWLER_DIR / "logs"
DATA_DIR = CRAWLER_DIR / "data"

# Create necessary directories
LOG_DIR.mkdir(parents=True, exist_ok=True)
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "crawler.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class POE2DBCrawler:
    def __init__(self):
        self.base_url = "https://poe2db.tw/us"
        self.data_dir = DATA_DIR

    async def crawl_url(self, url: str) -> dict:
        """Crawl a specific URL and return the extracted content."""
        try:
            logger.info(f"Crawling URL: {url}")
            
            async with async_playwright() as p:
                # Launch browser
                browser = await p.chromium.launch(headless=True)
                page = await browser.new_page()
                
                # Go to URL and wait for content to load
                await page.goto(url, wait_until='networkidle')
                
                # Extract content
                content = await page.content()
                
                # Close browser
                await browser.close()
                
                # Parse with BeautifulSoup
                soup = BeautifulSoup(content, 'html.parser')
                
                # Remove unwanted elements
                for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
                    element.decompose()
                    
                # Extract main content
                content = []
                
                # Add metadata
                content.append(f"# {soup.title.string if soup.title else 'Untitled Page'}")
                content.append(f"Source: {url}")
                content.append(f"Crawled at: {datetime.now().isoformat()}")
                content.append("")  # Empty line after metadata
                
                # Get all text content, preserving headers and lists
                for element in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'ul', 'ol', 'tr', "section"]):
                    if element.name.startswith('h'):
                        # Add appropriate markdown heading level
                        level = element.name[1]
                        heading_text = element.get_text(strip=True)
                        if heading_text:
                            content.append(f"{'#' * int(level)} {heading_text}")
                            content.append("")
                    elif element.name == 'p':
                        paragraph_text = element.get_text(strip=True)
                        if paragraph_text:
                            content.append(paragraph_text)
                            content.append("")
                    elif element.name in ['ul', 'ol']:
                        for li in element.find_all('li'):
                            item_text = li.get_text(strip=True)
                            if item_text:
                                content.append(f"- {item_text}")
                        content.append("")
                    elif element.name in ['tr']:
                        for li in element.find_all(['td', 'th']):
                            item_text = li.get_text(strip=True)
                            if item_text:
                                content.append(f"- {item_text}")
                        content.append("")
                    elif element.name in ["section"]:
                        content.append(f"## {element.get_text(strip=True)}")
                        content.append("")  
                
                # Join all content with newlines
                processed_content = "\n".join(content)
                
                logger.debug(f"Extracted content: {processed_content[:500]}...")  # Log first 500 chars
                
                return processed_content
            
        except Exception as e:
            logger.error(f"Error crawling {url}: {str(e)}")
            return None

    def save_to_file(self, content: str, filename: str) -> Path:
        """Save crawled content to a text file."""
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved content to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving content: {str(e)}")
            return None

    def update_knowledge_base(self, filepath: Path) -> bool:
        """Update the knowledge base with the crawled content."""
        try:
            # Prepare the file for upload
            files = {
                'file': (filepath.name, open(filepath, 'rb'), 'text/plain')
            }
            
            # Send to the knowledge base update endpoint
            response = requests.post('http://localhost:8000/update', files=files)
            response.raise_for_status()
            
            logger.info("Successfully updated knowledge base")
            return True
            
        except Exception as e:
            logger.error(f"Error updating knowledge base: {str(e)}")
            return False

    async def process_url(self, url: str) -> bool:
        """Process a URL: crawl, save, and update knowledge base."""
        # Extract filename from URL
        filename = url.split('/')[-1].lower() + f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Crawl the URL
        content = await self.crawl_url(url)
        if not content:
            return False
            
        # Save to file
        filepath = self.save_to_file(content, filename)
        if not filepath:
            return False
            
        # Update knowledge base
        return self.update_knowledge_base(filepath)

async def main():
    parser = argparse.ArgumentParser(description='POE2DB Crawler')
    parser.add_argument('url', help='URL to crawl')
    args = parser.parse_args()
    
    crawler = POE2DBCrawler()
    success = await crawler.process_url(args.url)
    if success:
        logger.info("Crawling process completed successfully")
    else:
        logger.error("Crawling process failed")

if __name__ == "__main__":
    asyncio.run(main()) 

    def save_to_file(self, content: str, filename: str) -> Path:
        """Save crawled content to a text file."""
        try:
            filepath = self.data_dir / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            logger.info(f"Saved content to {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"Error saving content: {str(e)}")
            return None

    def update_knowledge_base(self, filepath: Path) -> bool:
        """Update the knowledge base with the crawled content."""
        try:
            # Prepare the file for upload
            files = {
                'file': (filepath.name, open(filepath, 'rb'), 'text/plain')
            }
            
            # Send to the knowledge base update endpoint
            response = requests.post('http://localhost:8000/update', files=files)
            response.raise_for_status()
            
            logger.info("Successfully updated knowledge base")
            return True
            
        except Exception as e:
            logger.error(f"Error updating knowledge base: {str(e)}")
            return False

    async def process_url(self, url: str) -> bool:
        """Process a URL: crawl, save, and update knowledge base."""
        # Extract filename from URL
        filename = url.split('/')[-1].lower() + f"_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Crawl the URL
        content = await self.crawl_url(url)
        if not content:
            return False
            
        # Save to file
        filepath = self.save_to_file(content['content'], filename)
        if not filepath:
            return False
            
        # Update knowledge base
        return self.update_knowledge_base(filepath)

async def main():
    parser = argparse.ArgumentParser(description='POE2DB Crawler')
    parser.add_argument('url', help='URL to crawl')
    args = parser.parse_args()
    
    crawler = POE2DBCrawler()
    success = await crawler.process_url(args.url)
    if success:
        logger.info("Crawling process completed successfully")
    else:
        logger.error("Crawling process failed")

if __name__ == "__main__":
    asyncio.run(main()) 