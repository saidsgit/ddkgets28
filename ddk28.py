import streamlit as st
from PIL import Image
import random

st.set_page_config(
    page_title="🎉 Happy Birthday!",
    page_icon="🎂",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# --- DATEN ---

# Quiz Daten bleiben unverändert
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

# Puzzle Daten bleiben unverändert
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


# --- FUNKTIONEN FÜR DIE PHASEN ---

def run_quiz():
    """Zeigt das Quiz an und wertet es aus."""
    st.markdown("## 🎤 Taylor Swift Quiz")
    st.write("Beantworte alle Fragen richtig, um zum Puzzle zu gelangen!")

    with st.form("quiz_form"):
        user_answers = []
        for idx, q in enumerate(quiz):
            st.markdown(f"**Frage {idx + 1}:** {q['question']}")
            # Das `label` wird benötigt, aber wir wollen es nicht anzeigen, daher `label_visibility`
            user_answer = st.radio(
                label=f"Antwortmöglichkeiten für Frage {idx+1}",
                options=q["options"],
                key=f"quiz_question_{idx}",
                label_visibility="collapsed"
            )
            user_answers.append(user_answer)
        
        submitted = st.form_submit_button("Antworten einreichen 🎯")

    if submitted:
        score = 0
        for user_ans, q in zip(user_answers, quiz):
            if user_ans == q["answer"]:
                score += 1
        
        st.session_state.quiz_score = score
        st.markdown("---")
        
        if score == len(quiz):
            st.success(f"Perfekt! Du hast alle {len(quiz)} Fragen richtig beantwortet.")
            st.info("Mache dich bereit für das Puzzle... Die Seite lädt gleich neu.")
            st.session_state.phase = "puzzle"
            st.rerun() # Rerun immediately without sleeping
        else:
            st.error(f"Leider nur {score} von {len(quiz)} richtig. Ein echter Swiftie schafft das! Versuch es nochmal.")

def run_puzzle():
    """Führt die Puzzle-Logik aus. Jede Aufgabe ist ein eigenes Formular."""
    st.markdown("## 🧩 Taylor Swift Puzzle")
    st.write("Löse alle Aufgaben, um die Belohnung freizuschalten!")

    step = st.session_state.puzzle_step
    
    # Prüfen, ob das Puzzle bereits gelöst ist
    if step >= len(puzzle_steps):
        st.success("Fantastisch! Du hast alle Puzzle-Aufgaben gelöst!")
        st.info("Deine Belohnung wird vorbereitet...")
        st.session_state.phase = "reward"
        st.rerun() # Direkt neustarten, ohne zu warten
        return

    current = puzzle_steps[step]
    
    st.markdown(f"--- \n ### Aufgabe {step + 1} von {len(puzzle_steps)}")

    # Jede Aufgabe bekommt ein eigenes Formular
    with st.form(key=f"puzzle_form_{step}"):
        user_input = ""
        if current["type"] == "fill_blank":
            st.markdown(f"**Lückentext:** `{current['sentence']}`")
            user_input = st.text_input("Deine Antwort:", key=f"puzzle_fill_{step}")

        elif current["type"] == "anagram":
            # Anagramm nur einmal generieren und im Session State speichern
            scrambled_word_key = f"scrambled_{step}"
            if scrambled_word_key not in st.session_state:
                st.session_state[scrambled_word_key] = "".join(random.sample(current["word"], len(current["word"])))
            
            scrambled = st.session_state[scrambled_word_key]
            st.markdown(f"**Anagramm:** `{scrambled}`")
            st.markdown(f"*Hinweis: {current['hint']}*")
            user_input = st.text_input("Löse das Anagramm:", key=f"puzzle_anagram_{step}")

        submitted = st.form_submit_button("Antwort prüfen")

        if submitted:
            if user_input.strip().lower() == current["answer"].lower():
                st.success("Richtig! Auf zur nächsten Aufgabe.")
                st.session_state.puzzle_step += 1
                st.sleep(1)
                st.rerun()
            else:
                st.error("Leider falsch. Versuch es nochmal!")


def show_dot_art():
    """Zeigt die Dot-Art Belohnung an."""
    st.markdown("## 🖼️ Deine erste Belohnung")
    st.write("Du hast es fast geschafft! Hier ist ein kleiner Vorgeschmack.")
    
    try:
        dot_img = Image.open("dot_art.jpg")
        st.image(dot_img, caption="Aus Punkten gezaubert ✨", use_container_width=True)
    except FileNotFoundError:
        st.warning("Bild 'dot_art.jpg' nicht gefunden. Lege es in den Projektordner.")

    try:
        with open("dot_art.txt", "r", encoding="utf-8") as f:
            ascii_lines = f.readlines()
        
        max_lines = len(ascii_lines)
        slider_val = st.slider("Benutze den Schieberegler, um das Bild zu enthüllen!", 1, max_lines, 1)
        
        st.text("".join(ascii_lines[:slider_val]))

        if slider_val == max_lines:
            st.success("✨ Das ganze Bild ist enthüllt!")
            if st.button("Zeige die finale Überraschung! 🎁"):
                st.session_state.phase = "final"
                st.rerun()

    except FileNotFoundError:
        st.warning("Textdatei 'dot_art.txt' nicht gefunden. Lege sie in den Projektordner.")
        # Fallback-Button, falls die Datei fehlt
        if st.button("Trotzdem zur finalen Überraschung"):
            st.session_state.phase = "final"
            st.rerun()


def show_final_reward():
    """Zeigt das finale Geschenk an."""
    st.markdown("## 👑 Deine finale Belohnung!")
    st.balloons()
    
    try:
        jetski_img = Image.open("jetski.jpg")
        st.image(jetski_img, caption="Pack den Bikini ein! 🚤", use_container_width=True)
        st.markdown("### Wir gehen Jetski fahren! Alles Gute zum Geburtstag!")
    except FileNotFoundError:
        st.warning("Das Geschenkbild 'jetski.jpg' wurde nicht gefunden.")
    
    if st.button(" nochmal von vorne 🔁"):
        # Alle relevanten Session-States zurücksetzen
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()

# --- HAUPTLOGIK MIT PHASENSTEUERUNG ---

def main():
    st.title("🎂 Happy Birthday, Lieblingsmensch!")
    st.markdown("""
    Willkommen zur DDK-wird-28-und-hat-Geburtstagstag-Webseite!
    
    Taytay-Wissen könnte Dich heute weiterbringen. 🎁
    """)

    # GIF am Anfang anzeigen
    try:
        st.image("rabbit.gif", caption="Taylor sagt: Viel Glück!", use_container_width=True)
    except FileNotFoundError:
        st.error("Das Bild 'rabbit.gif' wurde nicht gefunden. Bitte im Projektordner ablegen.")

    st.markdown("---")

    # Session State initialisieren, falls noch nicht geschehen
    if "phase" not in st.session_state:
        st.session_state.phase = "quiz"
        st.session_state.puzzle_step = 0
        st.session_state.quiz_score = 0

    # Steuerung der Phasen
    if st.session_state.phase == "quiz":
        run_quiz()
    elif st.session_state.phase == "puzzle":
        run_puzzle()
    elif st.session_state.phase == "reward":
        show_dot_art()
    elif st.session_state.phase == "final":
        show_final_reward()
    
    st.markdown("---")
    st.caption("Du bist 🆒.")

if __name__ == "__main__":
    main()
