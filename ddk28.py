import streamlit as st
from PIL import Image
import random

st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Quizfragen
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

# Puzzleaufgaben
puzzle_steps = [
    {
        "type": "fill_blank",
        "sentence": "Taylor Swift wurde im Jahr ____ geboren.",
        "answer": "1989"
    },
    {
        "type": "anagram",
        "word": "fearless",
        "hint": "Ein Taylor Swift Album",
        "answer": "fearless"
    },
    {
        "type": "fill_blank",
        "sentence": "Der Song 'Love Story' ist auf dem Album ____.",
        "answer": "fearless"
    },
    {
        "type": "anagram",
        "word": "midnights",
        "hint": "Ein Taylor Swift Album, veröffentlicht 2022",
        "answer": "midnights"
    }
]


def run_quiz():
    st.markdown("## 💡 Taylor Swift Quiz")
    st.markdown("**Beweise dein TayTay-Wissen!** 🎶")

    with st.form("quiz_form"):
        user_answers = []
        for idx, q in enumerate(quiz):
            st.markdown(f"**🎤 Frage {idx + 1}:** {q['question']}")
            user_answer = st.radio(
                label=f"Antwort für Frage {idx+1}",
                options=q["options"],
                key=f"quiz_q_{idx}",
                label_visibility="collapsed"
            )
            user_answers.append(user_answer)
        
        submitted = st.form_submit_button("🎯 Einreichen")

    if submitted:
        score = sum(1 for user_ans, q in zip(user_answers, quiz) if user_ans == q["answer"])
        st.session_state.quiz_score = score

        st.markdown("---")
        if score == len(quiz):
            st.balloons()
            st.success(f"🎉 Perfekt! Alle {len(quiz)} Fragen richtig beantwortet.")

            try:
                with open("sponge1.gif", "rb") as f:
                    st.image(f.read(), caption="SpongeBob ist stolz auf dich! 🧽", use_container_width=True)
            except FileNotFoundError:
                st.info("Sponge1.gif nicht gefunden. Weiter geht's trotzdem!")

            st.info("Weiter geht’s zum Puzzle...")
            st.session_state.phase = "puzzle"
            st.rerun()
        else:
            st.error(f"😢 Nur {score} von {len(quiz)} richtig. Versuch es nochmal!")


def run_puzzle():
    st.markdown("## 🧩 Puzzle-Zeit!")
    st.write("🔐 Löse die Aufgaben, um Belohnungen zu verdienen!")

    step = st.session_state.puzzle_step
    if step >= len(puzzle_steps):
        st.success("🎊 Alle Puzzle gelöst! Bereit für die Belohnung?")
        st.session_state.phase = "reward"
        st.rerun()
        return

    current = puzzle_steps[step]
    st.markdown(f"---\n### Aufgabe {step + 1} von {len(puzzle_steps)}")

    with st.form(key=f"puzzle_form_{step}"):
        user_input = ""
        if current["type"] == "fill_blank":
            st.markdown(f"**📝 Vervollständige:** `{current['sentence']}`")
            user_input = st.text_input("Deine Antwort:", key=f"puzzle_fill_{step}")
        elif current["type"] == "anagram":
            scrambled_key = f"scrambled_{step}"
            if scrambled_key not in st.session_state:
                st.session_state[scrambled_key] = "".join(random.sample(current["word"], len(current["word"])))
            scrambled = st.session_state[scrambled_key]
            st.markdown(f"**🔀 Anagramm:** `{scrambled}`")
            st.markdown(f"*Hinweis: {current['hint']}*")
            user_input = st.text_input("Löse das Anagramm:", key=f"puzzle_anagram_{step}")
        
        submitted = st.form_submit_button("✅ Prüfen")
        if submitted:
            if user_input.strip().lower() == current["answer"].lower():
                st.success("✔️ Korrekt!")
                st.session_state.puzzle_step += 1
                st.rerun()
            else:
                st.error("❌ Leider falsch. Versuch es nochmal.")


def show_dot_art():
    st.markdown("## 🎨 Deine Belohnung – Dot Art")
    st.write("🧁 Mit jedem Schritt enthüllst du mehr vom Kunstwerk!")

    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="Magisches Punktebild ✨", use_container_width=True)
    except FileNotFoundError:
        st.warning("Bild 'dot_art.jpg' nicht gefunden.")

    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        val = st.slider("🔍 Enthülle Zeile für Zeile", 1, len(lines), 1)
        st.text("".join(lines[:val]))

        if val == len(lines):
            st.success("🎇 Alles enthüllt!")
            if st.button("🎁 Zur finalen Überraschung"):
                st.session_state.phase = "final"
                st.rerun()
    except FileNotFoundError:
        st.warning("Textdatei 'dot_art.txt' fehlt.")
        if st.button("Trotzdem zur Überraschung"):
            st.session_state.phase = "final"
            st.rerun()


def show_final_reward():
    st.markdown("## 🏆 Finale Belohnung")
    st.balloons()
    st.success("💖 Du hast alles geschafft!")

    try:
        jetski_img = Image.open("jetski.jpg")
        st.image(jetski_img, caption="🚤 Jetski-Zeit! Happy Birthday!!", use_container_width=True)
    except FileNotFoundError:
        st.warning("Bild 'jetski.jpg' fehlt.")

    try:
        with open("sponge1.gif", "rb") as f:
            st.image(f.read(), caption="Sponge findet dich großartig 🧽", use_container_width=True)
    except FileNotFoundError:
        pass

    if st.button("🔁 Nochmal spielen"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()


def main():
    st.markdown("<h1 style='text-align: center;'>🎂 Happy Birthday, Lieblingsmensch!</h1>", unsafe_allow_html=True)
    st.markdown("""
    Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!
    
    Taytay-Wissen könnte Dich heute weiterbringen. 🎁
    """)

    try:
        st.image("rabbit.gif", caption="🐰 Viel Glück wünscht dir Taylor!", use_container_width=True)
    except FileNotFoundError:
        st.warning("rabbit.gif nicht gefunden.")

    if "phase" not in st.session_state:
        st.session_state.phase = "quiz"
        st.session_state.puzzle_step = 0
        st.session_state.quiz_score = 0

    if st.session_state.phase == "quiz":
        run_quiz()
    elif st.session_state.phase == "puzzle":
        run_puzzle()
    elif st.session_state.phase == "reward":
        show_dot_art()
    elif st.session_state.phase == "final":
        show_final_reward()

    st.markdown("---")
    st.caption("🎈 Mit Liebe gemacht für dich 🎈")

if __name__ == "__main__":
    main()
