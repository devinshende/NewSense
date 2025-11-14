"""Test API - interactive mode or automated tests."""

import requests
import json
import sys
import time


def extract(text, p=0.5, verbose=False):
    """Call API and return keyphrases."""
    try:
        if verbose:
            print(f"\n[DEBUG] Text length: {len(text)} chars")
            print(f"[DEBUG] Sampling: p={p}")
            print(f"[DEBUG] Sending request to API...")
        
        start = time.time()
        response = requests.post(
            "http://localhost:8000/extract",
            json={"text": text, "p": p}
        )
        elapsed = time.time() - start
        
        if verbose:
            print(f"[DEBUG] API response received in {elapsed:.3f}s")
            print(f"[DEBUG] Status code: {response.status_code}")
        
        result = response.json()
        result['_elapsed'] = elapsed
        return result
    except Exception as e:
        print(f"Error: {e}")
        print("Is server running? (python server.py)")
        sys.exit(1)


def display_result(result, text):
    """Display extraction results."""
    elapsed = result.get('_elapsed', 0)
    keyphrases = result['keyphrases']
    print(f"\nFound {len(keyphrases)} keyphrases in {elapsed:.3f}s:")
    for start_idx, end_idx in keyphrases:
        phrase = text[start_idx:end_idx]
        print(f"  [{start_idx}:{end_idx}] '{phrase}'")
    print()


def interactive_mode(p=0.5, verbose=False):
    """Interactive text input mode."""
    print("\n=== Interactive Mode ===")
    print(f"Paste text and press Enter twice (blank line to submit)")
    print(f"Sampling: p={p}")
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
        
        result = extract(text, p, verbose=verbose)
        display_result(result, text)


def run_tests():
    """Run quick automated tests."""
    print("\n=== Running Tests ===\n")
    
    total_start = time.time()
    
    # Test 1
    text1 = "Apple Inc. was founded by Steve Jobs in Cupertino, California."
    print(f"Test 1: {text1}")
    result1 = extract(text1, p=1.0)
    display_result(result1, text1)
    
    # Test 2
    text2 = "Jeffrey earned his degree from University of California, Santa Barbara."
    print(f"Test 2: {text2}")
    result2 = extract(text2, p=0.3)
    display_result(result2, text2)
    
    total_elapsed = time.time() - total_start
    print(f"✓ Tests complete in {total_elapsed:.3f}s")
    print(f"\nNote: First API call is slow due to model loading on server.")
    print(f"Subsequent calls are fast.")


if __name__ == "__main__":
    verbose = "-v" in sys.argv or "--verbose" in sys.argv
    
    # Parse p value from command line (e.g., -p 0.5)
    p = 0.5
    for i, arg in enumerate(sys.argv):
        if arg == "-p" and i + 1 < len(sys.argv):
            p = float(sys.argv[i + 1])
    
    if "-i" in sys.argv:
        interactive_mode(p=p, verbose=verbose)
    else:
        run_tests()
        print("\nRun with -i for interactive mode: python test_api.py -i")
        print("Options: -v (verbose), -p <value> (sampling, default 0.3)")

