# Anime Guesser

A fun and interactive **anime guessing game** powered by **Gemini** and a curated anime knowledge base. You think of an anime, and the AI will try to guess it by asking strategic yes/no questions.

Play now: [https://animeguesser.streamlit.app](https://animeguesser.streamlit.app)

---

## How It Works

1. You think of an anime from a pre-defined knowledge base.
2. The LLM generates yes/no questions to narrow down its options.
3. You respond with Yes / No / Not Sure.
4. After 5 questions (or earlier if confident), the model attempts a final guess.
5. You decide if it was right.

Behind the scenes:
- A structured knowledge base in `.txt` or `.json` format holds metadata for 15+ popular anime titles.
- The app uses Google's Gemini 1.5 Pro for natural language reasoning.
- Memory of prior Q&A helps the model refine future questions and narrow the possibilities.

---

## Tech Stack

- Frontend/UI: Streamlit
- LLM: Gemini 1.5 Pro
- Knowledge Base: Text file with curated anime metadata (genre, setting, MC power level, etc.)
- Deployment: Streamlit Cloud

---

## Features

- LLM-powered dynamic question generation
- Maintains conversational context for smarter deductions
- Custom knowledge base of top anime like Naruto, Jujutsu Kaisen, Death Note, Solo Leveling, and more
- Play again functionality
- Fully hosted—no installation needed

---
