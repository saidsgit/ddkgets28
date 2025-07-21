import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

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

def run_quiz():
    st.markdown("## 🎤 Taylor Swift Quiz")
    st.write("Beantworte alle Fragen richtig, um dein Geburtstagsgeheimnis zu enthüllen!")

    score = 0
    user_answers = []

    with st.form("quiz_form"):
        for idx, q in enumerate(quiz):
            st.markdown(f"**Frage {idx+1}:** {q['question']}")
            user_answer = st.radio(
                label="",
                options=q["options"],
                key=f"question_{idx}"
            )
            user_answers.append(user_answer)
        submitted = st.form_submit_button("Antworten einreichen 🎯")

    if submitted:
        for user_ans, q in zip(user_answers, quiz):
            if user_ans == q["answer"]:
                score += 1

        st.markdown("---")
        st.success(f"Du hast **{score} von {len(quiz)}** Fragen richtig beantwortet.")

        if score == len(quiz):
            st.balloons()
            st.markdown("## 🎁 Glückwunsch!")
            st.markdown("Du hast alles richtig beantwortet und dein Geschenk ist...")

            try:
                jetski_img = Image.open("jetski.jpg")
                st.image(jetski_img, caption="Pack den Bikini ein!", use_container_width=True)
            except FileNotFoundError:
                st.warning("Das Geschenkbild 'jetski.jpg' wurde nicht gefunden.")

        else:
            st.warning("Noch nicht ganz! Versuche es nochmal, um das Geheimnis zu lüften.")


# Puzzle mit Lückentext und Anagrammen gemischt

puzzle_tasks = [
    {
        "type": "cloze",
        "text": "Taylor Swift wurde im Jahr ___ geboren.",
        "answer": "1989"
    },
    {
        "type": "anagram",
        "text": "Anagramm: OYATL",
        "answer": "taylor"
    },
    {
        "type": "cloze",
        "text": "Das Album ___ enthält den Song 'Love Story'.",
        "answer": "fearless"
    },
    {
        "type": "anagram",
        "text": "Anagramm: SHEAREN",
        "answer": "sheeran"
    },
    {
        "type": "cloze",
        "text": "Taylors Katze heißt ___ Grey.",
        "answer": "meredith"
    }
]

def load_dot_art():
    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            return f.readlines()
    except FileNotFoundError:
        st.warning("Dot-Art Textdatei nicht gefunden. Lege 'dot_art.txt' in den Projektordner.")
        return None


def puzzle_step():
    if "step" not in st.session_state:
        st.session_state.step = 0
    if "lines_revealed" not in st.session_state:
        st.session_state.lines_revealed = 0
    if "answer_correct" not in st.session_state:
        st.session_state.answer_correct = False

    dot_art_lines = load_dot_art()
    max_steps = len(puzzle_tasks)

    if st.session_state.step >= max_steps:
        st.success("🎉 Du hast alle Aufgaben gelöst und das ganze Bild enthüllt!")
        if dot_art_lines:
            st.text("".join(dot_art_lines))
        return

    task = puzzle_tasks[st.session_state.step]

    st.markdown(f"### Aufgabe {st.session_state.step + 1} von {max_steps}")

    if task["type"] == "cloze":
        text_display = task["text"].replace("___", "_____")
        st.write(text_display)
        user_ans = st.text_input("Fülle die Lücke mit dem richtigen Wort:", key="input_cloze")
    else:
        st.write(task["text"])
        user_ans = st.text_input("Entschlüssle das Anagramm und gib das richtige Wort ein:", key="input_anagram")

    # Button prüfen
    if st.button("Antwort prüfen"):
        if user_ans.strip().lower() == task["answer"].lower():
            st.session_state.answer_correct = True
        else:
            st.session_state.answer_correct = False
            st.error("Leider falsch, versuche es nochmal.")

    # Hier **außerhalb** des button-blocks** rerun nur bei richtigem Ergebnis
    if st.session_state.answer_correct:
        st.success("Richtig! Eine weitere Zeile wird enthüllt.")
        st.session_state.step += 1
        st.session_state.lines_revealed += 1
        st.session_state.answer_correct = False  # reset für nächste Aufgabe
        st.experimental_rerun()

    if dot_art_lines and st.session_state.lines_revealed > 0:
        st.markdown("### Dein Dot-Art Bild wird enthüllt:")
        st.text("".join(dot_art_lines[:st.session_state.lines_revealed]))


def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("""
    Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!
    
    Taytay-Wissen könnte Dich heute weiterbringen. 🎁
    """)

    try:
        with open("rabbit.gif", "rb") as f:
            gif_bytes = f.read()
        st.image(gif_bytes, caption="Taylor sagt: Viel Glück!", use_container_width=True)
    except FileNotFoundError:
        st.error("Das Bild 'rabbit.gif' wurde nicht gefunden. Bitte im Projektordner ablegen.")

    st.markdown("---")
    run_quiz()

    st.markdown("---")
    st.markdown("## 🖼️ DDK = Schönheit auf den Punkt gebracht")

    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="Aus Punkten gezaubert ✨", use_container_width=True)
    except FileNotFoundError:
        st.error("Dot-Art Bild (.jpg) nicht gefunden. Lege 'dot_art.jpg' in den Projektordner.")

    st.markdown("---")
    st.markdown("## 💬 Bonus-Level")

    puzzle_step()

    st.markdown("---")
    st.caption("Du bist 🆒s.")

if __name__ == "__main__":
    main()
