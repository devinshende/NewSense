from google import genai

# Load API key
with open('super_top_secret.txt', 'r') as f:
    api_key = f.read().strip()

client = genai.Client(api_key=api_key)

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
    if not user_input:
        return {"success": False, "error": "No text provided"}
    
    # Get the appropriate prompt for the selected mode
    prompt = prompts.get(mode, prompts['brainrot']).format(user_input=user_input)
    
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=prompt
        )
        
        transformed_text = response.text
        
        # Store in history
        history[f"{mode}_{len(history)}"] = {
            "user": user_input,
            "assistant": transformed_text,
            "mode": mode
        }
        
        return {
            "success": True,
            "transformed_text": transformed_text
        }
    
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
