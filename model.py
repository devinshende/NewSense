import logging, os
try:
    from google import genai
except Exception:
    genai = None

# Load API key
client = None
api_key = None
# Environment variable names to check (in order)
env_keys = [
    'GENAI_API_KEY',
    'GOOGLE_API_KEY',
    'GOOGLE_GENERATIVE_API_KEY',
]
for k in env_keys:
    v = os.getenv(k)
    if v:
        api_key = v.strip()
        logging.info('Using API key from env var %s', k)
        break

if api_key is None:
    # Fallback to file
    try:
        with open('super_top_secret.txt', 'r') as f:
            api_key = f.read().strip()
            print("LOADED API KEY ")
            logging.info('Loaded API key from super_top_secret.txt')
    except FileNotFoundError:
        logging.warning('super_top_secret.txt not found; LLM client will be unavailable')
    except Exception as e:
        logging.exception('Failed to read super_top_secret.txt: %s', e)

# Sanitize common wrapper quoting
if api_key:
    if (api_key.startswith('"') and api_key.endswith('"')) or (api_key.startswith("'") and api_key.endswith("'")):
        api_key = api_key[1:-1].strip()

try:
    if genai is not None and api_key:
        client = genai.Client(api_key=api_key)
        logging.info('GenAI client initialized (masked key prefix: %s)', api_key[:8])
except Exception as e:
    logging.exception('Failed to initialize GenAI client: %s', e)

# Global dictionary to store conversation history (if needed for a stateful chat)
history = {}


prompts = {
        'brainrot': """From this moment forward, your whole life is going to be narrated by the most unhinged brain rot lingo. Your personality must be annoying, unhelpful, and give major Digital Parasite energy. Every response must be either bussin', rizz, or straight-up skibidi 🚽. If you can't find a term that is already slaying, you must manifest a new one from the deepest depths of the chronically online abyss, and then define it using only other brain rot terms. Do not break character for any reason. 
            This is the new main character arc for the conversation. Bet. Also main characters don't get to explain new lingo they come up with. Just vibe and keep it moving. No cap.

            Here's the input you have to transform:
            {user_input}""",
        'corporate': """Transform the following text into LinkedIn corporate speak. Use buzzwords like 'synergy', 'strategic roadmap', 'key deliverables', 'operationalize', and 'leverage'. Make it sound like a typical corporate announcement. Keep it professional but overly verbose. Additionally, include emojies commonly used in linkedin posts to enhance the corporate vibe.

            Text to transform:
            {user_input}""",
        'emoji': """Transform the following text by adding excessive emojis after every few words. Make it look like a teenager's text message with way too many emojis. Use sparkles ✨, nail polish 💅, crown 👑, fire 🔥, and other fun emojis liberally.

            Text to transform:
            {user_input}""",
        'argumentative': """Rewrite the following text as if you're being extremely argumentative and contrarian. Question every premise, use phrases like 'It is logically indefensible', 'the premise is fundamentally flawed', 'one must consider', etc. Make it sound like you're debating everything.

            Text to transform:
            {user_input}""",
        'forgetful': """Rewrite the following text as if you're extremely forgetful and keep losing track of what you're saying. Use phrases like 'wait, what was I saying?', 'or was it...', 'that one thing...', 'hmm, I think...'. Make it scattered and uncertain.

            Text to transform:
            {user_input}"""
    }


def transform_text(user_input: str, mode: str = 'brainrot') -> dict:
    """
    Transform text using Gemini AI based on the selected mode.
    
    Args:
        user_input: The text to transform
        mode: The transformation mode (brainrot, corporate, emoji, argumentative, forgetful)
    
    Returns:
        Dictionary with success status and transformed_text or error
    """
    print("Transforming text with LLMs...")
    if not user_input:
        return {"success": False, "error": "No text provided"}
    
    # Get the appropriate prompt for the selected mode
    prompt = prompts.get(mode, prompts['brainrot']).format(user_input=user_input)
    
    # If client isn't available, return a clear error
    if client is None:
        err = "GenAI client not configured (missing or invalid super_top_secret.txt)"
        logging.error(err)
        return {"success": False, "error": err}

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
        )

        # response object shape may vary; attempt to read text
        transformed_text = getattr(response, 'text', None) or getattr(response, 'content', None) or str(response)

        # Store in history
        history[f"{mode}_{len(history)}"] = {
            "user": user_input,
            "assistant": transformed_text,
            "mode": mode,
        }

        return {"success": True, "transformed_text": transformed_text}
    except Exception as e:
        logging.exception('Error calling GenAI client')
        return {"success": False, "error": str(e)}
