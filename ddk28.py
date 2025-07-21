import streamlit as st
from PIL import Image
import random

st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- Quiz Daten ---
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

# --- Puzzle Daten (Mischung Lückentext + Anagramm) ---
puzzle_steps = [
    # Schritt 1: Lückentext
    {
        "type": "fill_blank",
        "sentence": "Taylor Swift wurde im Jahr ____ geboren.",
        "answer": "1989"
    },
    # Schritt 2: Anagramm
    {
        "type": "anagram",
        "word": "fearless",
        "hint": "Ein Taylor Swift Album",
        "answer": "fearless"
    },
    # Schritt 3: Lückentext
    {
        "type": "fill_blank",
        "sentence": "Der Song 'Love Story' ist auf dem Album ____.",
        "answer": "fearless"
    },
    # Schritt 4: Anagramm
    {
        "type": "anagram",
        "word": "midnights",
        "hint": "Ein Taylor Swift Album, veröffentlicht 2022",
        "answer": "midnights"
    }
]

# --- Funktionen ---

def run_quiz():
    st.markdown("## 🎤 Taylor Swift Quiz")
    st.write("Beantworte alle Fragen richtig, um zum Puzzle zu gelangen!")

    score = 0
    user_answers = []

    with st.form("quiz_form"):
        for idx, q in enumerate(quiz):
            st.markdown(f"**Frage {idx + 1}:** {q['question']}")
            user_answer = st.radio(
                label="",
                options=q["options"],
                key=f"quiz_question_{idx}"
            )
            user_answers.append(user_answer)
        submitted = st.form_submit_button("Antworten einreichen 🎯")

    if submitted:
        for user_ans, q in zip(user_answers, quiz):
            if user_ans == q["answer"]:
                score += 1

        st.markdown("---")
        st.success(f"Du hast **{score} von {len(quiz)}** Fragen richtig beantwortet.")

        st.session_state.quiz_done = True
        st.session_state.quiz_score = score


def run_puzzle():
    st.markdown("## 🧩 Taylor Swift Puzzle")
    st.write("Löse alle Aufgaben, um die Belohnung zu bekommen!")

    step = st.session_state.get("puzzle_step", 0)
    if step >= len(puzzle_steps):
        st.success("Du hast alle Puzzle-Aufgaben gelöst!")
        st.session_state.puzzle_done = True
        return

    current = puzzle_steps[step]
    if current["type"] == "fill_blank":
        user_input = st.text_input(f"Lückentext: {current['sentence']}", key=f"puzzle_fill_{step}")
        if st.button("Antwort prüfen", key=f"check_fill_{step}"):
            if user_input.strip().lower() == current["answer"].lower():
                st.success("Richtig! Weiter zum nächsten Schritt.")
                st.session_state.puzzle_step = step + 1
            else:
                st.error("Leider falsch. Versuch es nochmal!")

    elif current["type"] == "anagram":
        scrambled = "".join(random.sample(current["word"], len(current["word"])))
        st.markdown(f"**Anagramm:** {scrambled}")
        st.markdown(f"*Hinweis: {current['hint']}*")
        user_input = st.text_input("Löse das Anagramm:", key=f"puzzle_anagram_{step}")
        if st.button("Antwort prüfen", key=f"check_ana_{step}"):
            if user_input.strip().lower() == current["answer"].lower():
                st.success("Richtig! Weiter zum nächsten Schritt.")
                st.session_state.puzzle_step = step + 1
            else:
                st.error("Leider falsch. Versuch es nochmal!")

def show_dot_art():
    st.markdown("## 🖼️ Dot Art Belohnung")
    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="Aus Punkten gezaubert ✨", use_container_width=True)
    except FileNotFoundError:
        st.warning("Dot-Art Bild (.jpg) nicht gefunden. Lege 'dot_art.jpg' in den Projektordner.")

    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            ascii_lines = f.readlines()
    except FileNotFoundError:
        st.warning("Dot-Art Textdatei nicht gefunden. Lege 'dot_art.txt' in den Projektordner.")
        return

    max_lines = len(ascii_lines)
    slider_val = st.slider("Wie viele Zeilen möchtest du sehen?", 1, max_lines, 1, key="dot_art_slider")
    displayed_text = "".join(ascii_lines[:slider_val])
    st.text(displayed_text)

    if slider_val == max_lines:
        st.success("✨ Das ganze Bild ist enthüllt!")

def show_final_reward():
    st.markdown("## 🎁 Finale Belohnung")
    try:
        jetski_img = Image.open("jetski.jpg")
        st.image(jetski_img, caption="Pack den Bikini ein!", use_container_width=True)
        st.balloons()
    except FileNotFoundError:
        st.warning("Das Geschenkbild 'jetski.jpg' wurde nicht gefunden.")

# --- Hauptlogik mit Phasensteuerung ---

def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("""
    Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!
    
    Taytay-Wissen könnte Dich heute weiterbringen. 🎁
    """)

    # Rabbit gif laden
    try:
        with open("rabbit.gif", "rb") as f:
            gif_bytes = f.read()
        st.image(gif_bytes, caption="Taylor sagt: Viel Glück!", use_container_width=True)
    except FileNotFoundError:
        st.error("Das Bild 'rabbit.gif' wurde nicht gefunden. Bitte im Projektordner ablegen.")

    st.markdown("---")

    # Session State initialisieren
    if "phase" not in st.session_state:
        st.session_state.phase = "quiz"
        st.session_state.quiz_done = False
        st.session_state.quiz_score = 0
        st.session_state.puzzle_step = 0
        st.session_state.puzzle_done = False

    # Steuerung der Phasen
    if st.session_state.phase == "quiz":
        run_quiz()
        if st.session_state.quiz_done and st.session_state.quiz_score == len(quiz):
            if st.button("Weiter zum Puzzle"):
                st.session_state.phase = "puzzle"
                st.experimental_rerun()

    elif st.session_state.phase == "puzzle":
        run_puzzle()
        if st.session_state.puzzle_done:
            if st.button("Belohnung anzeigen"):
                st.session_state.phase = "reward"
                st.experimental_rerun()

    elif st.session_state.phase == "reward":
        show_dot_art()
        if st.button("Zeige finale Belohnung"):
            st.session_state.phase = "final"
            st.experimental_rerun()

    elif st.session_state.phase == "final":
        show_final_reward()

    st.markdown("---")
    st.caption("Du bist 🆒s.")

if __name__ == "__main__":
    main()
