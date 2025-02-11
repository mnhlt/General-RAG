#!/bin/bash

# Exit on error
set -e

echo "🚀 Starting POE-RAG project setup..."

# Check prerequisites
echo "📋 Checking prerequisites..."

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher"
    exit 1
fi

# Check Node.js version
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher"
    exit 1
fi

# Check npm
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm"
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install RAG system dependencies
echo "📚 Installing RAG system dependencies..."
cd rag
pip install -r requirements.txt
cd ..

# Install crawler
echo "🕷️ Installing crawler..."
cd crawler
pip install -e .
cd ..

# Install frontend dependencies
echo "🌐 Installing frontend dependencies..."
cd web
npm install
cd ..

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p crawler/data
mkdir -p crawler/logs
mkdir -p rag/storage

# Create example .env files if they don't exist
echo "⚙️ Creating example environment files..."

# RAG .env
if [ ! -f rag/.env ]; then
    cat > rag/.env << EOL
LLM_API_KEY=your_api_key
LLM_BASE_URL=http://your-llm-server:1234/v1
EOL
    echo "Created rag/.env (please update with your actual values)"
fi

# Web .env.local
if [ ! -f web/.env.local ]; then
    cat > web/.env.local << EOL
NEXT_PUBLIC_API_URL=http://localhost:8000
EOL
    echo "Created web/.env.local"
fi

echo "
✨ Setup complete! Here's what to do next:

1. Update the environment variables in:
   - rag/.env
   - web/.env.local

2. Start the services:
   - RAG API: cd rag && uvicorn api:app --reload
   - Web Interface: cd web && npm run dev
   - Crawler Example: cd crawler && python cli.py https://poe2db.tw/us/Items

3. Visit http://localhost:3000 to see the web interface

For more information, check the README.md file.
" 