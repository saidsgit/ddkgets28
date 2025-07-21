import streamlit as st
from PIL import Image
import random

st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# === QUIZ ===
quiz = [
    {"question": "Welches Album enthält den Song 'Love Story'?",
     "options": ["Red", "Fearless", "1989", "Speak Now"], "answer": "Fearless"},
    {"question": "Wie heißt Taylor Swifts Katze, die nach einer TV-Ärztin benannt wurde?",
     "options": ["Meredith Grey", "Olivia Benson", "Lexie Grey", "Cristina Yang"], "answer": "Meredith Grey"},
    {"question": "Mit wem hat Taylor Swift das Lied 'Everything Has Changed' aufgenommen?",
     "options": ["Shawn Mendes", "Ed Sheeran", "Zayn Malik", "Harry Styles"], "answer": "Ed Sheeran"},
    {"question": "Welches dieser Alben wurde 2020 überraschend veröffentlicht?",
     "options": ["Lover", "Midnights", "Folklore", "Reputation"], "answer": "Folklore"},
    {"question": "In welchem Jahr wurde Taylor Swift geboren?",
     "options": ["1989", "1990", "1991", "1992"], "answer": "1989"},
]

# === PUZZLES ===
puzzle_steps = [
    {"type": "fill_blank", "sentence": "Taylor Swift wurde im Jahr ____ geboren.", "answer": "1989"},
    {"type": "anagram", "word": "fearless", "hint": "Ein Taylor Swift Album", "answer": "fearless"},
    {"type": "fill_blank", "sentence": "Der Song 'Love Story' ist auf dem Album ____.", "answer": "fearless"},
    {"type": "anagram", "word": "midnights", "hint": "Ein Taylor Swift Album, veröffentlicht 2022", "answer": "midnights"}
]

# === QUIZ FUNKTION ===
def run_quiz():
    st.markdown("## 🎤 Taylor Swift Quiz")
    with st.form("quiz_form"):
        score = 0
        for i, q in enumerate(quiz):
            answer = st.radio(q["question"], q["options"], key=f"q{i}")
            if "answers" not in st.session_state:
                st.session_state.answers = {}
            st.session_state.answers[i] = answer
        submitted = st.form_submit_button("Antworten einreichen 🎯")
        if submitted:
            for i, q in enumerate(quiz):
                if st.session_state.answers[i] == q["answer"]:
                    score += 1
            if score == len(quiz):
                st.success("🎉 Perfekt! Weiter zum Puzzle!")
                st.session_state.phase = "puzzle"
                st.rerun()
            else:
                st.error(f"Du hast {score} von {len(quiz)} richtig. Versuch’s nochmal!")

# === PUZZLE FUNKTION ===
def run_puzzle():
    st.markdown("## 🧩 Puzzle-Zeit")
    step = st.session_state.puzzle_step

    if step >= len(puzzle_steps):
        st.success("🎉 Du hast alle Aufgaben gelöst!")
        st.session_state.phase = "reward"
        st.rerun()
        return

    current = puzzle_steps[step]
    with st.form(key=f"puzzle_{step}"):
        if current["type"] == "fill_blank":
            st.markdown(f"**Lückentext:** `{current['sentence']}`")
            user_input = st.text_input("Deine Antwort")
        elif current["type"] == "anagram":
            if f"scrambled_{step}" not in st.session_state:
                st.session_state[f"scrambled_{step}"] = "".join(random.sample(current["word"], len(current["word"])))
            st.markdown(f"**Anagramm:** `{st.session_state[f'scrambled_{step}']}`")
            st.markdown(f"*Hinweis: {current['hint']}*")
            user_input = st.text_input("Löse das Anagramm")

        submitted = st.form_submit_button("Antwort prüfen")
        if submitted:
            if user_input.strip().lower() == current["answer"].lower():
                st.success("✅ Richtig!")
                st.session_state.puzzle_step += 1
                st.rerun()
            else:
                st.error("❌ Leider falsch. Versuch’s nochmal.")

# === DOT ART BELONUNG ===
def show_dot_art():
    st.markdown("## 🖼️ Schönheit auf den Punkt gebracht")
    try:
        img = Image.open("dot_art.jpg")
        st.image(img, caption="Dot-Art ✨", use_container_width=True)
    except FileNotFoundError:
        st.warning("Datei 'dot_art.jpg' fehlt.")

    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        max_lines = len(lines)
        val = st.slider("Enthülle das Bild!", 1, max_lines, 1)
        st.text("".join(lines[:val]))
        if val == max_lines:
            st.success("🎉 Alles enthüllt!")
            if st.button("🎁 Zeig mir das Geschenk!"):
                st.session_state.phase = "final"
                st.rerun()
    except FileNotFoundError:
        st.warning("Datei 'dot_art.txt' fehlt.")
        if st.button("Weiter trotzdem"):
            st.session_state.phase = "final"
            st.rerun()

# === FINALE BELOHNUNG ===
def show_final_reward():
    st.markdown("## 🏁 Finale Belohnung")
    st.balloons()
    try:
        img = Image.open("jetski.jpg")
        st.image(img, caption="🚤 Jetski-Time!", use_container_width=True)
        st.markdown("### Alles Gute zum Geburtstag 🎂")
    except FileNotFoundError:
        st.warning("Datei 'jetski.jpg' fehlt.")
    if st.button("🔄 Nochmal von vorn"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# === MAIN ===
def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!
    
    Taytay-Wissen könnte Dich heute weiterbringen. 🎁")

    try:
        st.image("rabbit.gif", caption="Taylor sagt: Viel Glück!", use_container_width=True)
    except FileNotFoundError:
        st.warning("🐰 rabbit.gif fehlt")

    if "phase" not in st.session_state:
        st.session_state.phase = "quiz"
        st.session_state.puzzle_step = 0

    st.markdown("---")

    if st.session_state.phase == "quiz":
        run_quiz()
    elif st.session_state.phase == "puzzle":
        run_puzzle()
    elif st.session_state.phase == "reward":
        show_dot_art()
    elif st.session_state.phase == "final":
        show_final_reward()

    st.markdown("---")
    st.caption("Geburtstagspower by Streamlit 💜")

if __name__ == "__main__":
    main()
