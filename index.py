import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

st.set_page_config(page_title="Anime Oracle", layout="centered")

st.markdown("<h1 style='text-align: center; margin-bottom: 10px;'>🔮 Anime Oracle 🔮</h1>", unsafe_allow_html=True)

st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <img src='https://image.myanimelist.net/ui/5LYzTBVoS196gvYvw3zjwMyT6MIUqrUYIAsZmoLVMdQ' 
             alt='Anime Oracle' 
             style='width: 50%; padding: 10px; border-radius: 10px;'/>
    </div>
""", unsafe_allow_html=True)


# Load the anime knowledge base from a .txt file
@st.cache_data
def load_anime_kb(file_path="anime_kb.txt"):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

anime_kb = load_anime_kb()

# Initialize session state
if "chat" not in st.session_state:
    model = genai.GenerativeModel("models/gemini-1.5-pro")
    st.session_state.chat = model.start_chat(history=[])

if "qa_history" not in st.session_state:
    st.session_state.qa_history = []

if "current_question" not in st.session_state:
    st.session_state.current_question = ""

#Style
st.markdown("""
    <style>
        .center-button {
            display: flex;
            justify-content: center;
        }
    </style>
    """, unsafe_allow_html=True)


# 1. Generate question or guess
if st.session_state.current_question == "":
    history = "\n".join([f"Q: {q}\nA: {a}" for q, a in st.session_state.qa_history])
    guess_check_prompt = f"""
    You are helping guess an anime from a knowledge base. Here's the data:

    Knowledge base:
    {anime_kb}

    Q&A so far:
    {history}

    If you are confident in the anime based on this, respond ONLY with:
    <anime title> - <one-sentence reason>

    If you are NOT confident, respond with EXACTLY: "Keep asking questions."
    """

    response = st.session_state.chat.send_message(guess_check_prompt)
    guess_text = response.text.strip()

    if guess_text.lower().startswith("keep asking"):
        # Proceed with asking the next yes/no question
        question_prompt = f"""
        Use the knowledge base and Q&A so far to generate a yes/no question to help narrow down the anime.

        Knowledge base:
        {anime_kb}

        Conversation:
        {history}

        Generate ONE clear, strategic yes/no question.
        """
        response = st.session_state.chat.send_message(question_prompt)
        st.session_state.current_question = response.text.strip()
    else:
        # Confident guess
        st.markdown("### 🎯 My Early Guess:")
        st.success(guess_text)
        with st.container():
            st.markdown('<div class="center-button">', unsafe_allow_html=True)
            
            if st.button("🔄 Play Again"):
                for key in ["chat", "qa_history", "current_question"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop()
    if len(st.session_state.qa_history) >= 5:
        prompt = f"""
        Based on the Q&A below and the anime knowledge base, guess which anime the user is thinking of.

        Knowledge base:
        {anime_kb}

        Q&A history:
        {history}

        Only respond with the most likely anime name and 1 sentence why.
        """
        response = st.session_state.chat.send_message(prompt)
        st.markdown("### 🎯 My Guess:")
        st.success(response.text.strip())
        with st.container():
            st.markdown('<div class="center-button">', unsafe_allow_html=True)
            
            if st.button("🔄 Play Again"):
                for key in ["chat", "qa_history", "current_question"]:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        st.stop()

    question_prompt = f"""
    You are playing an anime guessing game. Use the knowledge base below to generate a strategic YES/NO question.

    Knowledge base:
    {anime_kb}

    Conversation history so far:
    {history}

    Generate a single yes/no question to help guess the anime. Be specific, not too wordy, simple and avoid repeating previous questions.
    """
    response = st.session_state.chat.send_message(question_prompt)
    question = response.text.strip()
    st.session_state.current_question = question


if st.session_state.current_question:
    st.markdown(f"### 🤖 {st.session_state.current_question}")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Yes"):
            st.session_state.qa_history.append((st.session_state.current_question, "Yes"))
            st.session_state.current_question = ""
            st.rerun()
    with col2:
        if st.button("No"):
            st.session_state.qa_history.append((st.session_state.current_question, "No"))
            st.session_state.current_question = ""
            st.rerun()


# Show chat history
if st.session_state.qa_history:
    st.subheader("🕹️ Question History")
    for q, a in st.session_state.qa_history:
        st.markdown(f"**Q:** {q}")
        st.markdown(f"**A:** {a}")
        st.markdown("---")
