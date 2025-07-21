import streamlit as st
from PIL import Image
import time

# ------------------------------
# App-Konfiguration
# ------------------------------
st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ------------------------------
# Quiz-Daten
# ------------------------------
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

# ------------------------------
# Quiz-Funktion
# ------------------------------
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

            st.markdown("### 🌊 **Eine Jetskifahrt!** 🏄‍♀️")
            st.image("https://media.giphy.com/media/3o6Zt8MgUuvSbkZYWc/giphy.gif", caption="Pack den Bikini ein!")

        else:
            st.warning("Noch nicht ganz! Versuche es nochmal, um das Geheimnis zu lüften.")

# ------------------------------
# Hauptfunktion der App
# ------------------------------
def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("""
    Willkommen zu deinem ganz persönlichen Geburtstagsquiz rund um Taylor Swift!
    
    Wenn du alles richtig beantwortest, erwartet dich eine kleine Überraschung 🎁
    """)

    st.image("https://i.imgur.com/N1zLfUQ.jpg", caption="Taylor sagt: Viel Glück!")

    st.markdown("---")
    run_quiz()

    st.markdown("---")
    st.markdown("## 🖼️ Dein persönliches Dot-Art-Bild")

    try:
        dot_img = Image.open("dot_art.jpg")  # Pfad zu deinem Dot-Art Bild
        st.image(dot_img, caption="Aus Punkten gezaubert ✨", use_column_width=True)
    except FileNotFoundError:
        st.error("Dot-Art Bild (.jpg) nicht gefunden. Lege 'dot_art.jpg' in den Projektordner.")

    st.markdown("---")
    st.markdown("## 💬 Bonus: ASCII-Dot-Art Enthüllung")

    with st.expander("👀 Enthülle das Geheimnis – Zeile für Zeile..."):
        try:
            with open("dot_art.txt", "r", encoding="utf-8") as f:
                ascii_lines = f.readlines()

            display = st.empty()
            revealed_text = ""
            for line in ascii_lines:
                revealed_text += line
                display.text(revealed_text)
                time.sleep(0.05)  # Geschwindigkeit der Enthüllung, anpassbar

        except FileNotFoundError:
            st.warning("Dot-Art Textdatei nicht gefunden. Lege 'dot_art.txt' in den Projektordner.")

    st.markdown("---")
    st.caption("Mit ganz viel ❤️ für dich gemacht.")

# ------------------------------
# Programmstart
# ------------------------------
if __name__ == "__main__":
    main()
