"""Configuration for key-phrase extraction."""

SPACY_MODEL = "en_core_web_sm"

# Extraction toggles
EXTRACT_NOUN_CHUNKS = True
EXTRACT_NAMED_ENTITIES = True
EXTRACT_VERB_PHRASES = False

# Named entity types to extract
ENTITY_TYPES = {
    "PERSON", "ORG", "GPE", "LOC", "PRODUCT", "EVENT",
    "WORK_OF_ART", "DATE", "TIME", "MONEY", "PERCENT",
}

# Phrase filtering
MIN_PHRASE_LENGTH = 2
MAX_PHRASE_LENGTH = 100
REMOVE_OVERLAPS = True
CASE_SENSITIVE = False

# Words to exclude
EXCLUDED_WORDS = {
    "he", "she", "it", "they", "we", "you", "i",
    "him", "her", "them", "us",
    "his", "her", "hers", "its", "their", "theirs", "our", "ours", "your", "yours",
}

# Sampling (0.0 to 1.0)
DEFAULT_SAMPLING_PERCENTAGE = 0.5

