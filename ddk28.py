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
        try:
            with open("jetski2.gif", "rb") as f:
                st.image(f.read(), caption="", use_container_width=True)
        except FileNotFoundError:
            pass

    if submitted:
        score = sum(1 for user_ans, q in zip(user_answers, quiz) if user_ans == q["answer"])
        st.session_state.quiz_score = score

        st.markdown("---")
        if score == len(quiz):
            st.balloons()
            st.success(f"🎉 Perfekt! Alle {len(quiz)} Fragen richtig beantwortet.")
            st.session_state.phase = "interlude"
            st.rerun()
        else:
            st.error(f"😢 Nur {score} von {len(quiz)} richtig. Versuch es nochmal!")

def show_interlude():
    try:
        with open("sponge2.gif", "rb") as f:
            st.image(f.read(), caption="🧽 Ooooooooooooohh", use_container_width=True)
    except FileNotFoundError:
        st.warning("sponge2.gif nicht gefunden.")
    st.markdown("### 🧽 Seid ihr bereit, Kinder?")
    if st.button("Aye aye, Captain!"):
        st.session_state.phase = "puzzle_all"
        st.rerun()

def run_puzzle_all():
    st.markdown("## 🧩 Alle Puzzle auf einmal!")
    st.write("🔐 Fülle alle Felder korrekt aus, um weiterzukommen.")

    all_correct = True
    user_inputs = []
    with st.form("puzzle_all_form"):
        for idx, current in enumerate(puzzle_steps):
            st.markdown(f"### Aufgabe {idx + 1}")
            if current["type"] == "fill_blank":
                st.markdown(f"📝 `{current['sentence']}`")
                ans = st.text_input("Antwort:", key=f"puzzle_all_fill_{idx}")
            elif current["type"] == "anagram":
                scrambled_key = f"puzzle_all_scrambled_{idx}"
                if scrambled_key not in st.session_state:
                    st.session_state[scrambled_key] = "".join(random.sample(current["word"], len(current["word"])))
                st.markdown(f"🔀 `{st.session_state[scrambled_key]}`")
                st.markdown(f"*Hinweis: {current['hint']}*")
                ans = st.text_input("Löse das Anagramm:", key=f"puzzle_all_anagram_{idx}")
            user_inputs.append(ans)

        submitted = st.form_submit_button("✅ Prüfen")

    if submitted:
        for idx, (user_input, current) in enumerate(zip(user_inputs, puzzle_steps)):
            if user_input.strip().lower() != current["answer"].lower():
                all_correct = False
                st.error(f"❌ Aufgabe {idx+1} ist falsch.")
        if all_correct:
            st.success("✔️ Alle Aufgaben korrekt!")
            st.session_state.phase = "reward_image"
            st.rerun()

def show_reward_image_with_audio():
    st.markdown("## 🖼️ Schönheit auf den Punkt gebracht")
    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="✨ Dot Art erscheint...", use_container_width=True)
    except FileNotFoundError:
        st.warning("dot_art.jpg fehlt.")

    try:
        audio_file = open("Aufzeichnung.m4a", "rb")
        st.audio(audio_file.read(), format='audio/mp3')
    except FileNotFoundError:
        st.warning("Aufzeichnung.m4a nicht gefunden.")

    answer = st.text_input("Wie viele Pflanzen sind in unserer Wohnung?", key="plants")
    if st.button("Weiter") and answer.strip() == "16":
        st.session_state.phase = "dot_slider"
        st.rerun()

def show_dot_slider_and_question():
    st.markdown("## 📃 Du bist das! Es ist nur Text? Aber Du bist das!")
    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
        val = st.slider("🔍 Zeilen anzeigen", 1, len(lines), 1)
        st.text("".join(lines[:val]))
    except FileNotFoundError:
        st.warning("dot_art.txt fehlt.")
        return

    if val == len(lines):
        st.success("📃 Selbst als Text bist Du cools!")
        year = st.text_input("Von wann ist das Bild?", key="art_year")
        if year.strip() == "2018":
            if st.button("🎁 Zur finalen Überraschung"):
                st.session_state.phase = "final"
                st.rerun()

def show_final_reward():
    st.markdown("## 🏆 Hiieeeer kommt DDKs superdupercooles DDK-wird-28-Geburtstagstag-Geschenk von Mr. DK für Mrs. DK")
    st.balloons()
    st.success("💖 Geschafft!")

    try:
        jetski_img = Image.open("jetski3.jpg")
        st.image(jetski_img, caption="🚤 Ist das ein Jetski? JA, das ist ein Jetski! \n Kaufen wir also endich ein Jetski?? Nein!\nAber im Mittelmeer eine Runde cruisen ist auch nicht verkehrt😎 Happy Birthday ❤️", use_container_width=True)
    except FileNotFoundError:
        st.warning("jetski.jpg fehlt.")

    try:
        with open("jetski2.gif", "rb") as f:
            st.image(f.read(), caption="", use_container_width=True)
    except FileNotFoundError:
        pass

    if st.button("🔁 Grüßee. ZURÜCK."):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    st.markdown("<h1 style='text-align: center;'>🎂 Happy Birthday, Lieblingsmensch!</h1>", unsafe_allow_html=True)
    st.markdown("""
    Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!🎁
    """)

    try:
        st.image("rabbit.gif", caption="🐰", use_container_width=True)
    except FileNotFoundError:
        st.warning("rabbit.gif nicht gefunden.")

    if "phase" not in st.session_state:
        st.session_state.phase = "quiz"
        st.session_state.quiz_score = 0

    phase = st.session_state.phase
    if phase == "quiz":
        run_quiz()
    elif phase == "interlude":
        show_interlude()
    elif phase == "puzzle_all":
        run_puzzle_all()
    elif phase == "reward_image":
        show_reward_image_with_audio()
    elif phase == "dot_slider":
        show_dot_slider_and_question()
    elif phase == "final":
        show_final_reward()

    st.markdown("---")
    st.caption("Du bist das ❤️")

if __name__ == "__main__":
    main()
