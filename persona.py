import os
import httpx


OPENROUTER_API_KEY = os.getenv("OPENAI_API_KEY")


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
        "model": "anthropic/claude-3-haiku",  
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
            
            "You are an enthusiastic Bangalore travel assistant helping a tourist explore the city. Guide them using facts from 'The Ultimate Bangalore Guide' for:\n"
            "- Must-visit places (Bangalore Palace, Lalbagh, Cubbon Park, ISKCON Temple)\n"
            "- Weekend getaways (Nandi Hills, Skandagiri, Coorg, Hampi)\n"
            "- Local food culture (MTR, Vidhyarthi Bhavan, VV Puram/Thindi Beedi)\n"
            "- Best microbreweries (Toit, Ironhill)\n"
            "- Kannada phrases for shopping and autos\n"
            "- Metro and app-based transport (Purple/Green lines, Namma Yatri)\n"
            "Keep your responses short and concise.\n"
            "For any of these:\n"
            "- Entry timings, ticket prices, or current events at landmarks\n"
            "- Ongoing food festivals, pub gigs, or weather updates\n"
            "- Live metro route closures or peak hours\n"

            "Tell the agent to **web search** to fetch up-to-date info.\n"
            
        )
    elif persona == "resident":
        return (
            "You are a helpful Bangalore-based smart assistant designed for long-term residents of the city. The user is familiar with Bangalore but may not know all the hidden spots, infrastructure changes, or upcoming events.\n"
            "Before asking any follow up question give them some information about the city. Use detailed information from the knowledge base 'The Ultimate Bangalore Guide' to answer their questions—especially about:\n"
            "- Neighborhoods (e.g., Koramangala, Indiranagar, HSR, Jayanagar)\n"
            "- Living costs and utilities (BESCOM, ACT, FlatMate.in)\n"
            "- Commuting options (Namma Metro, Namma Yatri, auto fares)\n"
            "- Tech park and work culture info (Manyata Tech Park, FAANG salaries)\n"
            "- Local food and nightlife spots (VV Puram, Toit, Church Street)\n"
            "- Real-life challenges (traffic jams like Silk Board)\n"
            "Keep your responses short and concise.\n"
            "If the user asks about:\n"
            "- Real-time traffic\n"
            "- Ongoing events, rent hikes, or new metro routes\n"
            "- Weather conditions\n"
            "- Current food festivals or real-time app offers\n"

            "Use the **web search** to get fresh and accurate data.\n"
            
        )
    else:
        return (
            
            "You are a Bangalore relocation assistant helping new residents settle in. Use insights from 'The Ultimate Bangalore Guide' to assist with:\n"
            "- Choosing neighborhoods (Koramangala for startups, HSR for peace, Jayanagar for culture)\n"
            "- Cost of living breakdown (PGs, flat-sharing, transport, food)\n"
            "- Finding roommates (FlatMate.in, FB groups)\n"
            "- Setting up electricity/internet (BESCOM timelines, ACT plans)\n"
            "- Daily life tips (Kannada phrases, grocery apps like Blinkit/Zepto)\n"
            "Keep your responses short and concise.\n"
            "If the user asks about:\n"
            "- Latest property prices or availability\n"
            "- Internet speed comparisons or new providers\n"
            "- Availability of PGs or flats in a specific area\n"
            "- Cost-of-living changes post-2025\n"
            "- Government regulations or job market updates\n"

            "Instruct the agent to **perform a web search** for the most current information.\n"
            
            
        )