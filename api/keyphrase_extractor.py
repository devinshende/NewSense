"""Core NLP key-phrase extraction module."""

import spacy
from typing import List, Dict, Any, Callable, Set
from functools import lru_cache
import time

from api.utils import (
    create_phrase_object,
    filter_by_length,
    remove_overlapping_phrases,
    deduplicate_phrases,
    sort_phrases_by_position,
    filter_excluded_words,
    random_sample_phrases,
)
from api.config import (
    SPACY_MODEL,
    EXTRACT_NOUN_CHUNKS,
    EXTRACT_NAMED_ENTITIES,
    EXTRACT_VERB_PHRASES,
    ENTITY_TYPES,
    MIN_PHRASE_LENGTH,
    MAX_PHRASE_LENGTH,
    REMOVE_OVERLAPS,
    EXCLUDED_WORDS,
    DEFAULT_SAMPLING_PERCENTAGE,
)


_nlp_model = None


@lru_cache(maxsize=1)
def load_nlp_model(model_name: str = SPACY_MODEL):
    """Load and cache spaCy model."""
    try:
        return spacy.load(model_name)
    except OSError:
        raise RuntimeError(
            f"spaCy model '{model_name}' not found. "
            f"Install: python -m spacy download {model_name}"
        )


def get_nlp_model():
    """Get cached NLP model."""
    global _nlp_model
    if _nlp_model is None:
        _nlp_model = load_nlp_model()
    return _nlp_model


def extract_noun_chunks(doc) -> List[Dict[str, Any]]:
    """Extract noun chunks from spaCy doc."""
    return [
        create_phrase_object(
            phrase=chunk.text,
            start=chunk.start_char,
            end=chunk.end_char,
            phrase_type="noun_chunk"
        )
        for chunk in doc.noun_chunks
    ]


def extract_named_entities(doc, entity_types: Set[str] = ENTITY_TYPES) -> List[Dict[str, Any]]:
    """Extract named entities from spaCy doc."""
    return [
        create_phrase_object(
            phrase=ent.text,
            start=ent.start_char,
            end=ent.end_char,
            phrase_type=ent.label_
        )
        for ent in doc.ents
        if ent.label_ in entity_types
    ]

def apply_extractors(doc, extractors: List[Callable]) -> List[Dict[str, Any]]:
    """Apply multiple extraction functions to doc."""
    all_phrases = []
    for extractor in extractors:
        all_phrases.extend(extractor(doc))
    return all_phrases


def get_default_extractors() -> List[Callable]:
    """Get default extraction functions based on config."""
    extractors = []
    if EXTRACT_NOUN_CHUNKS:
        extractors.append(extract_noun_chunks)
    if EXTRACT_NAMED_ENTITIES:
        extractors.append(extract_named_entities)
    return extractors


def process_text(text: str) -> Any:
    """Process text with spaCy."""
    return get_nlp_model()(text)


def post_process_phrases(phrases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Apply post-processing to extracted phrases ."""
    phrases = deduplicate_phrases(phrases)
    phrases = filter_excluded_words(phrases, EXCLUDED_WORDS)
    phrases = filter_by_length(phrases, MIN_PHRASE_LENGTH, MAX_PHRASE_LENGTH)
    if REMOVE_OVERLAPS:
        phrases = remove_overlapping_phrases(phrases)
    phrases = sort_phrases_by_position(phrases)
    return phrases


def extract_keyphrases(
    text: str,
    extractors: List[Callable] = None,
    post_process: bool = True,
    p: float = DEFAULT_SAMPLING_PERCENTAGE,
    verbose: bool = False
) -> List[List[int]]:
    """
    Extract key phrases from text and return indices.
    
    Args:
        text: Input text
        extractors: Custom extraction functions (optional)
        post_process: Apply filtering/deduplication
        p: Sampling percentage (0.0 to 1.0), default 0.3
        verbose: Print timing info
    
    Returns:
        List of [start, end] index pairs: [[0, 10], [26, 36], ...]
    """
    if not text or not text.strip():
        return []
    
    total_start = time.time()
    
    # Step 1: Process with spaCy
    t1 = time.time()
    doc = process_text(text)
    if verbose:
        print(f"  spaCy processing: {time.time()-t1:.3f}s")
    
    # Step 2: Extract phrases
    if extractors is None:
        extractors = get_default_extractors()
    
    t2 = time.time()
    phrases = apply_extractors(doc, extractors)
    if verbose:
        print(f"  Extraction: {time.time()-t2:.3f}s ({len(phrases)} raw phrases)")
    
    # Step 3: Post-process
    if post_process:
        t3 = time.time()
        phrases = post_process_phrases(phrases)
        if verbose:
            print(f"  Post-processing: {time.time()-t3:.3f}s ({len(phrases)} after filter)")
    
    # Step 4: Sample
    if p < 1.0:
        t4 = time.time()
        phrases = random_sample_phrases(phrases, p)
        phrases = sort_phrases_by_position(phrases)
        if verbose:
            print(f"  Sampling: {time.time()-t4:.3f}s ({len(phrases)} after sample)")
    
    if verbose:
        print(f"  TOTAL: {time.time()-total_start:.3f}s")
    
    return [[p["start"], p["end"]] for p in phrases]

