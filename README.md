###  How persona detection works in this project

Persona detection in this project is handled using the **OpenRouter API** with **Anthropic’s Claude 3 Haiku** model. When the user sends a message, the input is sent to the model with a specific system prompt designed to classify the user into one of three categories:

- **`tourist`** – A person visiting Bangalore or asking about attractions, travel, etc.
- **`resident`** – A person living in or moving to Bangalore, asking about local life, housing, commute, etc.
- **`neutral`** – When the input is too generic or unclear to classify.

The model responds with a **single word** indicating the persona. This detected persona is then:

- Used to select a **persona-specific system prompt** (tourist, resident, or neutral) from the code or `prompts.md`.
- **Stored in memory** using AGNO's `MemoryEntry` so the agent can retain persona context throughout the conversation.
- **Automatically updated** if future user inputs suggest a change in persona (dynamic persona switching).

This allows the agent to respond in the right tone and with relevant context for the user's role in Bangalore.
