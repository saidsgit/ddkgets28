import streamlit as st
from PIL import Image
import time

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

# def ascii_animation():
#     if "ascii_lines" not in st.session_state:
#         try:
#             with open("dot_art.txt", "r", encoding="utf-8") as f:
#                 st.session_state.ascii_lines = f.readlines()
#         except FileNotFoundError:
#             st.warning("Dot-Art Textdatei nicht gefunden. Lege 'dot_art.txt' in den Projektordner.")
#             st.session_state.ascii_lines = []

#     # Initialisiere die Variablen, falls nicht vorhanden
#     if "line_index" not in st.session_state:
#         st.session_state.line_index = 0
#     if "animating" not in st.session_state:
#         st.session_state.animating = True

#     placeholder = st.empty()

#     if st.session_state.animating and st.session_state.line_index < len(st.session_state.ascii_lines):
#         displayed_text = "".join(st.session_state.ascii_lines[:st.session_state.line_index])
#         placeholder.text(displayed_text)

#         st.session_state.line_index += 1

#         time.sleep(0.2)
#         st.experimental_rerun()
#     else:
#         displayed_text = "".join(st.session_state.ascii_lines)
#         placeholder.text(displayed_text)
#         st.success("✨ Das ganze Bild ist enthüllt!")
#         st.session_state.animating = False
import time

def ascii_slide():
    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            ascii_lines = f.readlines()
    except FileNotFoundError:
        st.warning("Dot-Art Textdatei nicht gefunden. Lege 'dot_art.txt' in den Projektordner.")
        return

    max_lines = len(ascii_lines)

    # Initialisierung von States
    if "slider_val" not in st.session_state:
        st.session_state.slider_val = 1
    if "auto_play" not in st.session_state:
        st.session_state.auto_play = False

    # Button: Start der Animation
    if st.button("▶️ Zeilen automatisch anzeigen"):
        st.session_state.auto_play = True

    # Slider: Kontrolle auch manuell möglich
    st.session_state.slider_val = st.slider(
        "Wie viele Zeilen möchtest du sehen?",
        1,
        max_lines,
        st.session_state.slider_val,
        key="ascii_slider"
    )

    # Textanzeige
    displayed_text = "".join(ascii_lines[:st.session_state.slider_val])
    st.text(displayed_text)

    # Animation
    if st.session_state.auto_play and st.session_state.slider_val < max_lines:
        time.sleep(0.05)
        st.session_state.slider_val += 1
        st.experimental_rerun()
    elif st.session_state.slider_val == max_lines:
        st.session_state.auto_play = False
        st.success("✨ Das ganze Bild ist enthüllt!")



def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("""
    Willkommen zu deinem ganz persönlichen Geburtstagsquiz rund um Taylor Swift!
    
    Wenn du alles richtig beantwortest, erwartet dich eine kleine Überraschung 🎁
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
    st.markdown("## 🖼️ Dein persönliches Dot-Art-Bild")

    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="Aus Punkten gezaubert ✨", use_container_width=True)
    except FileNotFoundError:
        st.error("Dot-Art Bild (.jpg) nicht gefunden. Lege 'dot_art.jpg' in den Projektordner.")

    st.markdown("---")
    st.markdown("## 💬 Bonus: ASCII-Dot-Art Enthüllung")

    ascii_slide()

    st.markdown("---")
    st.caption("Mit ganz viel ❤️ für dich gemacht.")

if __name__ == "__main__":
    main()
