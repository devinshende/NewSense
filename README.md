# NewSense
The product our team introduced for the NLP Dumbathon 2025 at UC Santa Cruz organized by Cal Blanco

A text transformation and redaction application with NLP-powered keyphrase extraction that makes focused reading impossible.

<img width="1298" height="618" alt="image" src="https://github.com/user-attachments/assets/dc947c10-0331-4472-9f5d-04a1eff48209" />


[Video Demo](https://drive.google.com/file/d/1pG1ZL3WXwyeOvG0Jm_PeJnffu3OWyVPJ/view?usp=sharing)

## Features

- LLM-powered text transformation and paraphrasing with various modes (brainrot, argumentative, emoji, etc.)
- Intelligent keyphrase extraction and progressive redaction
- Interactive canvas-based UI

## Setup

### Prerequisites

- Python 3.11+
- Virtual environment (included in `dumb/`)
- A Gemini API Key from your own account

### Installation

### Pre setup
Git clone repo. 
Go to [gemini AI studio](https://aistudio.google.com) and go to Getting Started -> Dashboard -> API Keys -> Create API Key

then paste your API Key into a file in the main folder called `super_top_secret.txt`
the file will just simply be the key. No quotes, nothing else, just something like
`Aasfoiwjoeirjoias`

1. **Activate your virtual environment**
```bash
cd /Users/chelseyelmore/Documents/NLPDumbathon-2025
source dumb/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Running the App

You need to run **two API servers** and then open the frontend.

### Terminal 1: Main API (Text Transformation)
```bash
source dumb/bin/activate
uvicorn main:app --reload --port 8000
```
This starts the text transformation API at `http://localhost:8000`

### Terminal 2: Keyphrase Extraction API (Redaction)
```bash
source dumb/bin/activate
cd api
uvicorn server:app --reload --port 8001
```
This starts the redaction/keyphrase API at `http://localhost:8001`

### Open the Frontend
```bash
open index.html
```
Or simply double-click `index.html` in Finder.

## Quick Start

```bash
# Terminal 1
source dumb/bin/activate
uvicorn main:app --reload --port 8000

# Terminal 2 (new terminal)
source dumb/bin/activate
cd api
uvicorn server:app --reload --port 8001

# Then open canvas.html in your browser
```

## API Endpoints

### Main API (Port 8000)

- `GET /` - Health check
- `POST /transform` - Transform text
  - Body: `{"text": "your text", "mode": "brainrot"}`
- `GET /health` - Health check

### Keyphrase Extraction API (Port 8001)

- `GET /` - Health check
- `POST /extract` - Extract keyphrases
  - Body: `{"text": "your text", "p": 0.3}`
  - Returns: `{"keyphrases": [[start, end], ...]}`
- `GET /docs` - Interactive API documentation

## Project Structure

```
.
├── main.py              # Main FastAPI server (text transformation)
├── model.py             # Text transformation logic
├── canvas.html          # Frontend UI
├── requirements.txt     # Python dependencies
├── api/                 # Keyphrase extraction API
│   ├── server.py        # FastAPI server
│   ├── keyphrase_extractor.py
│   ├── config.py
│   ├── utils.py
│   └── README.md        # Detailed API documentation
├── assets/              # Images and assets
└── dumb/                # Virtual environment
```

## Troubleshooting

**Port already in use:**
```bash
# Find process using the port
lsof -i :8000  # or :8001

# Kill the process
kill <PID>
```

**Model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Import errors:**
```bash
pip install -r requirements.txt
```

## Development

Both servers run with `--reload` flag, so they automatically restart when you make code changes.

For more details on the keyphrase extraction API, see [api/README.md](api/README.md).


# To restate

once you have everything setup, in one terminal run 
`uvicorn api.server:app --reload --port 8001`
in the other terminal run 
`fastapi dev main.py`
then open in finder the index.html (via a web browser)
