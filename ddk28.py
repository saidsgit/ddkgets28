import streamlit as st
from PIL import Image
import random
import time

st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Taylor Swift Quiz ---
quiz = [
    {
        "question": "Welches Album enthält den Song 'Love Story'?",
        "options": ["Red", "Fearless", "1989", "Speak Now"],
        "answer": "Fearless"
    },
    {
        "question": "Wie heißt Taylor Swifts Katze, die nach einer TV-Ärztin benannt wurde?",
        "options": ["Meredith Grey", "Olivia Benson", "Lexie Grey", "Cristina Yang"],
        "answer": "Meredith Grey"
    },
    {
        "question": "Mit wem hat Taylor Swift das Lied 'Everything Has Changed' aufgenommen?",
        "options": ["Shawn Mendes", "Ed Sheeran", "Zayn Malik", "Harry Styles"],
        "answer": "Ed Sheeran"
    },
    {
        "question": "Welches dieser Alben wurde 2020 überraschend veröffentlicht?",
        "options": ["Lover", "Midnights", "Folklore", "Reputation"],
        "answer": "Folklore"
    },
    {
        "question": "In welchem Jahr wurde Taylor Swift geboren?",
        "options": ["1989", "1990", "1991", "1992"],
        "answer": "1989"
    }
]

# --- Puzzle Daten (Lückentext & Anagramme) ---
puzzle_steps = [
    # Lückentext: Wort in Klammern fehlt
    {
        "type": "cloze",
        "text": "Taylor Swift wurde im Jahr ___ geboren.",
        "answer": "1989"
    },
    # Anagramm: Buchstaben in zufälliger Reihenfolge
    {
        "type": "anagram",
        "word": "Swift",
        "scrambled": "twifs"
    },
    {
        "type": "cloze",
        "text": "Das Album '___' wurde 2020 überraschend veröffentlicht.",
        "answer": "Folklore"
    },
    {
        "type": "anagram",
        "word": "Meredith",
        "scrambled": "hdtiemre"
    },
    {
        "type": "cloze",
        "text": "Taylor Swifts berühmte Katze heißt ___ Grey.",
        "answer": "Meredith"
    }
]

# --- Funktionen ---

def run_quiz():
    st.markdown("## 🎤 Taylor Swift Quiz")
    st.write("Beantworte alle Fragen richtig, um das nächste Level freizuschalten!")

    if "quiz_score" not in st.session_state:
        st.session_state.quiz_score = 0
    if "quiz_done" not in st.session_state:
        st.session_state.quiz_done = False

    with st.form("quiz_form", clear_on_submit=False):
        user_answers = []
        for idx, q in enumerate(quiz):
            st.markdown(f"**Frage {idx+1}:** {q['question']}")
            ans = st.radio("", q["options"], key=f"q_{idx}")
            user_answers.append(ans)
        submitted = st.form_submit_button("Antworten einreichen 🎯")

    if submitted:
        score = 0
        for user_ans, q in zip(user_answers, quiz):
            if user_ans == q["answer"]:
                score += 1
        st.session_state.quiz_score = score
        st.session_state.quiz_done = True
        st.success(f"Du hast {score} von {len(quiz)} Fragen richtig beantwortet.")

    if st.session_state.quiz_done:
        if st.session_state.quiz_score == len(quiz):
            st.balloons()
            st.success("🎉 Super! Du hast das Quiz bestanden. Weiter zum Puzzle.")
        else:
            st.warning("Noch nicht ganz! Versuche es nochmal, um das Puzzle freizuschalten.")


def run_puzzle():
    st.markdown("## 🧩 Taylor Swift Puzzle")
    st.write("Löse die Aufgaben Schritt für Schritt, um das Dot-Art Bild freizuschalten.")

    if "puzzle_step" not in st.session_state:
        st.session_state.puzzle_step = 0
    if "puzzle_done" not in st.session_state:
        st.session_state.puzzle_done = False

    step = puzzle_steps[st.session_state.puzzle_step]
    completed = False

    if step["type"] == "cloze":
        answer = st.text_input(
            "Fülle die Lücke:",
            placeholder=step["text"].replace("___", "...")
        )
        if st.button("Antwort prüfen"):
            if answer.strip().lower() == step["answer"].lower():
                st.success("Richtig!")
                completed = True
            else:
                st.error("Das war leider falsch, versuche es nochmal.")

    elif step["type"] == "anagram":
        answer = st.text_input(
            f"Ordne die Buchstaben neu: {step['scrambled']}",
            max_chars=len(step["word"])
        )
        if st.button("Antwort prüfen"):
            if answer.strip().lower() == step["word"].lower():
                st.success("Richtig!")
                completed = True
            else:
                st.error("Das war leider falsch, versuche es nochmal.")

    if completed:
        st.session_state.puzzle_step += 1
        if st.session_state.puzzle_step >= len(puzzle_steps):
            st.session_state.puzzle_done = True
            st.success("🎉 Du hast alle Puzzle gelöst!")
        else:
            st.experimental_rerun()

    if st.session_state.puzzle_done:
        st.info("Du hast das Puzzle abgeschlossen! Weiter zur Belohnung.")

def show_dotart_reward():
    st.markdown("## 🖼️ Deine Belohnung: Dot-Art Bild")

    # Bild anzeigen
    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="Aus Punkten gezaubert ✨", use_container_width=True)
    except FileNotFoundError:
        st.error("Dot-Art Bild (.jpg) nicht gefunden. Lege 'dot_art.jpg' in den Projektordner.")

    # Text schrittweise mit Slider enthüllen
    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            ascii_lines = f.readlines()
    except FileNotFoundError:
        st.warning("Dot-Art Textdatei nicht gefunden. Lege 'dot_art.txt' in den Projektordner.")
        ascii_lines = []

    if ascii_lines:
        max_lines = len(ascii_lines)
        slider_val = st.slider("Wie viele Zeilen möchtest du sehen?", 1, max_lines, 1)
        displayed_text = "".join(ascii_lines[:slider_val])
        st.text(displayed_text)
        if slider_val == max_lines:
            st.success("✨ Das ganze Bild ist enthüllt!")

def show_final_gift():
    st.markdown("## 🎁 Das große Geschenk!")
    try:
        jetski_img = Image.open("jetski.jpg")
        st.image(jetski_img, caption="Pack den Bikini ein! 🏖️", use_container_width=True)
        st.balloons()
    except FileNotFoundError:
        st.error("Das Geschenkbild 'jetski.jpg' wurde nicht gefunden.")

def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("""
    Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!
    
    Taytay-Wissen könnte Dich heute weiterbringen. 🎁
    """)

    # Rabbit gif unverändert laden
    try:
        with open("rabbit.gif", "rb") as f:
            gif_bytes = f.read()
        st.image(gif_bytes, caption="Taylor sagt: Viel Glück!", use_container_width=True)
    except FileNotFoundError:
        st.error("Das Bild 'rabbit.gif' wurde nicht gefunden. Bitte im Projektordner ablegen.")

    st.markdown("---")

    # Steuerung der Phasen
    # if "phase" not in st.session_state:
    #     st.session_state.phase = "quiz"

    # if st.session_state.phase == "quiz":
    #     run_quiz()
    #     if st.session_state.get("quiz_done", False) and st.session_state.get("quiz_score", 0) == len(quiz):
    #         st.session_state.phase = "puzzle"
    #         st.experimental_rer
