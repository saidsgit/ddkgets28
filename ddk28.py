import streamlit as st
from PIL import Image

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
# Funktionen
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
# Seiteninhalt
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
    st.markdown("## 🖼️ Dein persönliches Punktbild")
    try:
        dot_img = Image.open("dot_art.png")
        st.image(dot_img, caption="Kunst aus Punkten – nur für dich!", use_column_width=True)
    except FileNotFoundError:
        st.error("Dot Art Bild nicht gefunden. Stelle sicher, dass 'dot_art.png' im selben Ordner liegt.")

    st.markdown("---")
    st.caption("Mit ganz viel ❤️ gemacht.")

# ------------------------------
# Start
# ------------------------------
if __name__ == "__main__":
    main()
