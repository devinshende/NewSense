# Key-Phrase Extraction API

A REST API with FastAPI that accepts plain text and returns character indices 
for keyphrases. Processes input text with spaCy to extract keyphrases (noun 
chunks and named entities), then returns a sampled set of `[start, end]` 
indices for front-end text redaction.

**Example:**  
Input: `"Apple Inc. was founded by Steve Jobs."`  
Output: `{"keyphrases": [[0, 10], [26, 36]]}`  
→ Indices for "Apple Inc." and "Steve Jobs"

## Setup

```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

## Usage

### Start the Server

```bash
python server.py
# API available at http://localhost:8000
# Docs at http://localhost:8000/docs
```

### Example API Request

```bash
curl -X POST "http://localhost:8000/extract" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Apple Inc. was founded by Steve Jobs.",
    "p": 0.3
  }'
```

### Example Response

```json
{
  "keyphrases": [
    [0, 10],
    [26, 36]
  ]
}
```

Each keyphrase is represented as `[start, end]` indices into the original text.

### Parameters

- `text`: Input text (required)
- `p`: Sampling percentage 0.0-1.0 (default: 1.0 = 100% of keyphrases)

## Direct Module Usage

```python
from keyphrase_extractor import extract_keyphrases

text = "Your text here"
indices = extract_keyphrases(text, p=0.5)

# indices is a list of [start, end] pairs
for start, end in indices:
    phrase = text[start:end]
    print(f"{phrase}: [{start}:{end}]")
```

## Configuration

If you wanna modify the extraction pipeline: edit `config.py`:

```python
# Extraction toggles
EXTRACT_NOUN_CHUNKS = True
EXTRACT_NAMED_ENTITIES = True

# Entity types to extract
ENTITY_TYPES = {"PERSON", "ORG", "GPE", "DATE", "MONEY"}

# Filtering
MIN_PHRASE_LENGTH = 2
MAX_PHRASE_LENGTH = 100
REMOVE_OVERLAPS = True

# Words to exclude (pronouns, etc)
EXCLUDED_WORDS = {"he", "she", "it", "they", ...}

# Default sampling
DEFAULT_SAMPLING_PERCENTAGE = 0.5
```

## Module Structure

```
api/
├── server.py              # FastAPI REST endpoints
├── keyphrase_extractor.py # Core NLP extraction logic
├── utils.py               # Pure utility functions 
├── config.py              # Configuration
├── test_keyphrase.py      # Extraction tests (interactive mode)
└── test_api.py            # API tests (interactive mode)
```

## Frontend Integration

```javascript
const response = await fetch('http://localhost:8000/extract', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    text: inputText,
    p: 0.3      // Return 30% of keyphrases
  })
});

const { keyphrases } = await response.json();

// keyphrases is an array of [start, end] pairs
// Example: [[0, 10], [26, 36]]

// Redact text
keyphrases.forEach(([start, end]) => {
  const phrase = inputText.substring(start, end);
  // Redact this phrase in your UI
});
```

## Testing

```bash
# Test keyphrase extraction
python test_keyphrase.py        # Automated tests
python test_keyphrase.py -i     # Interactive - paste your text
python test_keyphrase.py -v     # Verbose timing breakdown

# Test API (server must be running)
python test_api.py              # Automated API tests
python test_api.py -i           # Interactive - paste your text
python test_api.py -iv          # Interactive + verbose debug output
python test_api.py -i -p 0.5    # Interactive with custom sampling
```

## Troubleshooting

**Model not found:**
```bash
python -m spacy download en_core_web_sm
```

**Import errors:**
```bash
pip install -r requirements.txt
```
