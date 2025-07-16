import os
import httpx

# ✅ Use the renamed key (tricking AGNO/openai to use OpenRouter)
OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")
print("[DEBUG] Key loaded:", (OPENROUTER_API_KEY[:10] + "...") if OPENROUTER_API_KEY else "❌ NOT FOUND")


def detect_persona(user_text: str) -> str:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "HTTP-Referer": "https://banza-assignment.local",
        "X-Title": "Persona Classification"
    }

    messages = [
        {"role": "system", "content": (
            "You are a classifier. Based on the user's message, respond with only one word: "
            "'tourist', 'resident', or 'neutral'. No extra text.")},
        {"role": "user", "content": user_text}
    ]

    payload = {
        "model": "anthropic/claude-3-haiku",  # ✅ use supported OpenRouter model
        "messages": messages,
        "temperature": 0.0
    }

    try:
        response = httpx.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()
        reply = response.json()["choices"][0]["message"]["content"].strip().lower()

        if "tourist" in reply:
            return "tourist"
        elif "resident" in reply:
            return "resident"
        else:
            return "neutral"

    except Exception as e:
        print("[Persona detection error]", e)
        return "neutral"


def get_prompt_for(persona: str) -> str:
    """
    Returns a system prompt based on the user's persona.
    """
    if persona == "tourist":
        return (
            "<instructions>\n"
            "You are a cheerful, local Bangalore guide for tourists. Recommend must-see attractions, "
            "popular neighborhoods, Instagrammable cafes, and 1–3 day travel tips in a friendly, upbeat tone.\n"
            "</instructions>"
        )
    elif persona == "resident":
        return (
            "<instructions>\n"
            "You are a helpful, knowledgeable Bangalore assistant for people relocating to the city. "
            "Provide advice on neighborhoods, rent prices, job hubs, cost of living, and lifestyle options. "
            "Be practical, clear, and friendly.\n"
            "</instructions>"
        )
    else:
        return (
            "<instructions>\n"
            "You are a polite assistant. Begin by understanding whether the user is a tourist or a new resident. "
            "Ask clarifying questions if needed, then adjust your tone and suggestions accordingly.\n"
            "</instructions>"
        )
