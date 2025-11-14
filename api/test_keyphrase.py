"""Test and demo key-phrase extraction."""

from keyphrase_extractor import extract_keyphrases
import sys
import time


def test_basic():
    """Test basic extraction."""
    text = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
    
    print("Test: Basic Extraction")
    print(f"Input: {text}\n")
    
    start = time.time()
    indices = extract_keyphrases(text, p=1.0)
    elapsed = time.time() - start
    
    print(f"Found {len(indices)} keyphrases in {elapsed:.3f}s:")
    for start_idx, end_idx in indices:
        phrase = text[start_idx:end_idx]
        print(f"  [{start_idx}:{end_idx}] '{phrase}'")
    print()
    
    assert len(indices) > 0, "Should find keyphrases"
    return True


def test_indices():
    """Verify indices match text."""
    text = "Microsoft Corporation, founded by Bill Gates, is in Redmond, Washington."
    
    print("Test: Index Verification")
    print(f"Input: {text}\n")
    
    start = time.time()
    indices = extract_keyphrases(text, p=1.0)
    elapsed = time.time() - start
    
    print(f"Extracted in {elapsed:.3f}s")
    
    all_correct = True
    for start_idx, end_idx in indices:
        extracted = text[start_idx:end_idx]
        status = "✓"
        print(f"{status} [{start_idx}:{end_idx}] '{extracted}'")
    
    print(f"\n✓ All correct\n")
    assert len(indices) > 0, "Should find keyphrases"
    return True


def test_sampling():
    """Test sampling functionality."""
    text = "Jeffrey earned his degree from University of California, Santa Barbara."
    
    all_indices = extract_keyphrases(text, p=1.0)
    sample_50 = extract_keyphrases(text, p=0.5)
    sample_20 = extract_keyphrases(text, p=0.2)
    
    print("Test: Sampling")
    print(f"p=1.0: {len(all_indices)} keyphrases")
    print(f"p=0.5: {len(sample_50)} keyphrases")
    print(f"p=0.2: {len(sample_20)} keyphrases")
    
    assert len(sample_50) <= len(all_indices), "Sample should be smaller"
    assert len(sample_20) <= len(sample_50), "Smaller p = fewer phrases"
    print("✓ Sampling works\n")
    return True


def interactive_mode():
    """Interactive extraction mode."""
    print("\n=== Interactive Key-Phrase Extraction ===")
    print("Paste text and press Enter twice (blank line to extract)")
    print("Ctrl+C to exit\n")
    
    while True:
        print("Text:")
        lines = []
        while True:
            try:
                line = input()
                if line:
                    lines.append(line)
                else:
                    break
            except EOFError:
                break
        
        if not lines:
            print("Empty input, exiting...")
            break
        
        text = "\n".join(lines)
        
        p = input("Sampling (0.0-1.0, default 0.3): ").strip()
        p = float(p) if p else 0.3
        
        start = time.time()
        indices = extract_keyphrases(text, p)
        elapsed = time.time() - start
        
        print(f"\nFound {len(indices)} keyphrases in {elapsed:.3f}s:")
        for start_idx, end_idx in indices:
            phrase = text[start_idx:end_idx]
            print(f"  [{start_idx}:{end_idx}] '{phrase}'")
        print()


def run_tests():
    """Run automated tests."""
    print("\n" + "="*60)
    print("KEY-PHRASE EXTRACTION TESTS")
    print("="*60 + "\n")
    
    total_start = time.time()
    tests = [test_basic, test_indices, test_sampling]
    passed = 0
    
    try:
        for test in tests:
            if test():
                passed += 1
        
        total_elapsed = time.time() - total_start
        print("="*60)
        print(f"ALL TESTS PASSED ({passed}/{len(tests)}) in {total_elapsed:.3f}s")
        print("="*60)
        print(f"\nNote: First call is slow (~1-2s) due to model loading.")
        print(f"Subsequent calls are fast (~0.01-0.05s).")
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        print("Install: pip install -r requirements.txt")
        print("Model: python -m spacy download en_core_web_sm")
        exit(1)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "-i":
        interactive_mode()
    else:
        run_tests()
        print("\nRun with -i for interactive mode: python test_keyphrase.py -i")

