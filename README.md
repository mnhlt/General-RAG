# POE-RAG: Path of Exile 2 Knowledge Base with RAG

A Retrieval-Augmented Generation (RAG) system for Path of Exile 2, featuring a web crawler, knowledge base, and chat interface.

## Project Structure

```
POE-RAG/
├── crawler/           # Web crawler for POE2 content
│   ├── data/         # Crawled content storage
│   ├── logs/         # Crawler logs
│   └── cli.py        # Command-line interface
├── rag/              # RAG system implementation
│   ├── api.py        # FastAPI backend
│   ├── storage/      # Vector store
│   └── llm_wrapper.py # LLM integration
└── web/              # Next.js frontend
    └── app/          # Web application
```

## Features

- **Web Crawler**
  - Asynchronous crawling with Puppeteer
  - Markdown-formatted content extraction
  - Automatic knowledge base updates

- **RAG System**
  - ChromaDB vector store
  - DeepSeek LLM integration
  - Streaming responses
  - Context-aware answers

- **Web Interface**
  - Real-time chat interface
  - Streaming responses
  - Modern React components

## Setup

### Prerequisites
- Python 3.8+
- Node.js 18+
- Local LLM server (optional)

### Quick Start

The easiest way to set up the project is using our bootstrap script:

```bash
# Clone the repository
git clone https://github.com/yourusername/POE-RAG.git
cd POE-RAG

# Make bootstrap script executable
chmod +x bootstrap.sh

# Run bootstrap script
./bootstrap.sh
```

The bootstrap script will:
1. Check prerequisites
2. Set up Python virtual environment
3. Install all dependencies
4. Create necessary directories
5. Set up example configuration files

### Manual Installation

If you prefer to set up manually or the bootstrap script doesn't work for your environment:

1. **Backend Setup**
```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install RAG system dependencies
cd rag
pip install -r requirements.txt

# Install crawler
cd ../crawler
pip install -e .
```

2. **Frontend Setup**
```bash
cd ../web
npm install
```

### Configuration

Create `.env` files with your configuration:

1. **RAG System** (`rag/.env`):
```bash
LLM_API_KEY=your_api_key
LLM_BASE_URL=http://your-llm-server:1234/v1
```

2. **Web Interface** (`web/.env.local`):
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Usage

1. **Start the RAG API**
```bash
cd rag
uvicorn api:app --reload
```

2. **Run the Web Interface**
```bash
cd web
npm run dev
```

3. **Crawl Content**
```bash
cd crawler
python cli.py https://poe2db.tw/us/Items
```

## API Endpoints

- `POST /query`: Get an answer from the RAG system
  ```json
  {
    "message": "What are the weapon types in POE2?",
    "thread_id": "unique-thread-id"
  }
  ```

- `POST /query-stream`: Get a streaming response
  ```json
  {
    "message": "Explain the combat system",
    "thread_id": "unique-thread-id"
  }
  ```

- `POST /update`: Update the knowledge base with new content
  - Accepts multipart/form-data with a file upload
  - Supports .txt and .json files

## Development

- Use `npm run dev` for frontend development
- Use `uvicorn api:app --reload` for backend development
- Check logs in `crawler/logs/` and browser console

## Troubleshooting

Common issues and solutions:

1. **LLM Server Connection**
   - Ensure your LLM server is running
   - Check the URL in `rag/.env`
   - Verify API key if required

2. **Crawler Issues**
   - Check network connectivity
   - Verify target URL is accessible
   - Look for errors in `crawler/logs/crawler.log`

3. **Web Interface**
   - Ensure API is running on port 8000
   - Check browser console for errors
   - Verify environment variables

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License - see LICENSE file for details 