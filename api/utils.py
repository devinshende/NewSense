"""Pure utility functions for text processing."""

from typing import List, Dict, Any


def create_phrase_object(phrase: str, start: int, end: int, phrase_type: str = "unknown") -> Dict[str, Any]:
    """Create standardized phrase object."""
    return {
        "phrase": phrase,
        "start": start,
        "end": end,
        "type": phrase_type,
        "length": end - start
    }


def filter_by_length(phrases: List[Dict[str, Any]], min_length: int, max_length: int) -> List[Dict[str, Any]]:
    """Filter phrases by character length."""
    return [
        phrase for phrase in phrases
        if min_length <= len(phrase["phrase"]) <= max_length
    ]


def remove_overlapping_phrases(phrases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove overlapping phrases, keeping longest."""
    if not phrases:
        return []
    
    sorted_phrases = sorted(phrases, key=lambda x: (x["start"], -(x["end"] - x["start"])))
    result = []
    last_end = -1
    
    for phrase in sorted_phrases:
        if phrase["start"] >= last_end:
            result.append(phrase)
            last_end = phrase["end"]
    
    return result


def deduplicate_phrases(phrases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Remove duplicate phrases."""
    seen = set()
    result = []
    
    for phrase in phrases:
        key = (phrase["start"], phrase["end"], phrase["phrase"].lower())
        if key not in seen:
            seen.add(key)
            result.append(phrase)
    
    return result


def sort_phrases_by_position(phrases: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Sort phrases by position in text."""
    return sorted(phrases, key=lambda x: x["start"])


def filter_excluded_words(phrases: List[Dict[str, Any]], excluded_words: set) -> List[Dict[str, Any]]:
    """Filter out excluded words (pronouns, etc)."""
    return [
        phrase for phrase in phrases
        if phrase["phrase"].lower().strip() not in excluded_words
    ]


def random_sample_phrases(phrases: List[Dict[str, Any]], p: float, seed: int = None) -> List[Dict[str, Any]]:
    """Randomly sample p% of phrases. Same seed = same results."""
    import random
    
    if not 0.0 <= p <= 1.0:
        raise ValueError(f"p must be between 0.0 and 1.0, got {p}")
    
    if p >= 1.0:
        return phrases
    if p <= 0.0:
        return []
    
    num_to_sample = max(1, int(len(phrases) * p))
    
    if seed is not None:
        random.seed(seed)
    
    if num_to_sample >= len(phrases):
        return phrases
    
    return random.sample(phrases, num_to_sample)

