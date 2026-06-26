import sys
import requests
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QLineEdit, QTextEdit, QFrame, QListWidget,
    QListWidgetItem, QSizePolicy, QMessageBox, QComboBox, QInputDialog
)
from PySide6.QtCore import Qt

from flashcard_db import (
    add_card,
    get_all_cards,
    get_all_decks,
    init_db,
    delete_deck
)

init_db()


STYLE = """
QWidget {
    background-color: #0f0f0f;
    color: #f0f0f0;
    font-family: -apple-system, 'Segoe UI', sans-serif;
}

QLineEdit, QComboBox {
    background-color: #1e1e1e;
    border: 1px solid #2e2e2e;
    border-radius: 8px;
    padding: 10px;
    color: white;
}

QPushButton {
    background-color: #1e1e1e;
    color: white;
    border-radius: 8px;
    padding: 10px;
}

QPushButton:hover {
    background-color: #2a2a2a;
}

QPushButton#primary {
    background-color: #2563eb;
}

QListWidget {
    background-color: #121212;
    border: none;
}
"""


def make_primary_btn(text):
    btn = QPushButton(text)
    btn.setObjectName("primary")
    return btn


def make_title(text, size=22):
    lbl = QLabel(text)
    lbl.setStyleSheet(
        f"font-size:{size}px;font-weight:bold;color:white;"
    )
    return lbl


def make_subtitle(text):
    lbl = QLabel(text)
    lbl.setStyleSheet("color:#888;")
    return lbl


# SideBar

class Sidebar(QFrame):

    def __init__(self, main_window):
        super().__init__()

        self.main_window = main_window
        self.setFixedWidth(260)
        self.hide()

        layout = QVBoxLayout()

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search decks...")
        self.search.textChanged.connect(self.refresh_decks)

        self.sort_box = QComboBox()
        self.sort_box.addItems(
            ["Sort: A-Z", "Sort: Z-A"]
        )
        self.sort_box.currentIndexChanged.connect(
            self.refresh_decks
        )

        self.deck_list = QListWidget()
        self.deck_list.itemClicked.connect(
            self.open_deck
        )

        self.btn_new = make_primary_btn(
            "+ New Deck"
        )
        self.btn_new.clicked.connect(
            self.create_new_deck
        )

        self.btn_delete = QPushButton(
            "Delete Selected"
        )
        self.btn_delete.clicked.connect(
            self.delete_selected
        )

        layout.addWidget(make_title("Your Decks",18))
        layout.addWidget(self.search)
        layout.addWidget(self.sort_box)
        layout.addWidget(self.deck_list)
        layout.addWidget(self.btn_new)
        layout.addWidget(self.btn_delete)

        self.setLayout(layout)

        self.refresh_decks()


    def refresh_decks(self):

        self.deck_list.clear()

        decks = get_all_decks()

        search = self.search.text().lower()

        decks = [
            d for d in decks
            if search in d.lower()
        ]

        if self.sort_box.currentIndex() == 1:
            decks.sort(reverse=True)
        else:
            decks.sort()

        for d in decks:
            self.deck_list.addItem(
                QListWidgetItem(d)
            )


    def open_deck(self,item):

        self.main_window.start_quiz_for_deck(
            item.text()
        )


    def create_new_deck(self):

        text, ok = QInputDialog.getText(
            self,
            "New Deck",
            "Deck name:"
        )

        if ok and text.strip():

            self.main_window.add_flashcards_to_deck(
                text.strip()
            )

            self.refresh_decks()


    def delete_selected(self):

        items = self.deck_list.selectedItems()

        if not items:
            return

        delete_deck(
            items[0].text()
        )

        self.refresh_decks()



# ---------------- HOME ----------------

class HomePage(QWidget):

    def __init__(self,switch_page):

        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            make_title(
                "Welcome to Paperpilot",
                32
            )
        )

        layout.addWidget(
            make_subtitle(
                "Use the ☰ menu to manage decks."
            )
        )


        buttons=[
            ("Add New Flashcards",1),
            ("View Progress",2),
            ("AI Essay Marking",3)
        ]


        for text,page in buttons:

            btn=QPushButton(text)

            btn.clicked.connect(
                lambda _,p=page:
                switch_page(p)
            )

            layout.addWidget(btn)


        layout.addStretch()

        self.setLayout(layout)



# ---------------- FLASHCARDS ----------------

class FlashcardsPage(QWidget):

    def __init__(self):

        super().__init__()

        self.selected_deck=""

        layout=QVBoxLayout()


        self.deck_label=make_title(
            "Adding to..."
        )

        self.subject_input=QLineEdit()
        self.subject_input.setPlaceholderText(
            "Subject"
        )

        self.question_input=QLineEdit()
        self.question_input.setPlaceholderText(
            "Question"
        )

        self.answer_input=QLineEdit()
        self.answer_input.setPlaceholderText(
            "Answer"
        )


        btn=make_primary_btn(
            "Save Flashcard"
        )

        btn.clicked.connect(
            self.save_card
        )


        self.output=QLabel()


        layout.addWidget(
            self.deck_label
        )

        layout.addWidget(
            self.subject_input
        )

        layout.addWidget(
            self.question_input
        )

        layout.addWidget(
            self.answer_input
        )

        layout.addWidget(btn)

        layout.addWidget(
            self.output
        )

        self.setLayout(layout)


    def set_deck(self,deck):

        self.selected_deck=deck

        self.deck_label.setText(
            f"Adding to: {deck}"
        )


    def save_card(self):

        if not all([
            self.selected_deck,
            self.subject_input.text(),
            self.question_input.text(),
            self.answer_input.text()
        ]):

            self.output.setText(
                "Fill everything in"
            )
            return


        add_card(
            self.selected_deck,
            self.subject_input.text(),
            self.question_input.text(),
            self.answer_input.text()
        )


        self.output.setText(
            "✓ Saved"
        )


        self.subject_input.clear()
        self.question_input.clear()
        self.answer_input.clear()

        self.window().sidebar.refresh_decks()



# ---------------- QUIZ ----------------
import random

class QuizPage(QWidget):

    def __init__(self):
        super().__init__()

        self.cards = []
        self.current = None
        self.showing_answer = False
        self.mastered = 0

        layout = QVBoxLayout()

        self.title = make_title("Quiz Mode")

        self.progress = QLabel("")
        self.progress.setAlignment(Qt.AlignCenter)
        self.progress.setStyleSheet(
            "font-size:16px;color:#888;"
        )

        self.card = QLabel("")
        self.card.setAlignment(Qt.AlignCenter)
        self.card.setWordWrap(True)
        self.card.setMinimumHeight(250)
        self.card.setStyleSheet("""
            QLabel{
                background:#1e1e1e;
                border:2px solid #333;
                border-radius:15px;
                font-size:22px;
                padding:30px;
            }
        """)

        self.card.mousePressEvent = self.flip

        self.correct = make_primary_btn("✅ Got It!")
        self.wrong = QPushButton("🔁 Needs Practice")

        self.correct.clicked.connect(self.got_it)
        self.wrong.clicked.connect(self.needs_practice)

        layout.addWidget(self.title)
        layout.addWidget(self.progress)
        layout.addStretch()
        layout.addWidget(self.card)
        layout.addStretch()
        layout.addWidget(self.correct)
        layout.addWidget(self.wrong)

        self.setLayout(layout)

    def load_deck(self, deck):

        self.cards = get_all_cards(deck)

        if not self.cards:
            self.card.setText("This deck has no flashcards yet.")
            self.progress.setText("")
            self.correct.hide()
            self.wrong.hide()
            return

        random.shuffle(self.cards)

        self.mastered = 0

        self.correct.show()
        self.wrong.show()

        self.next_card()

    def next_card(self):

        if not self.cards:
            self.card.setText(
                f"🎉 Deck Complete!\n\nYou mastered {self.mastered} cards."
            )
            self.progress.setText("Finished!")
            self.correct.hide()
            self.wrong.hide()
            return

        self.current = self.cards[0]
        self.showing_answer = False

        self.progress.setText(
            f"Mastered: {self.mastered} | Remaining: {len(self.cards)}"
        )

        self.card.setText(
            f"{self.current[3]}\n\n(click to reveal answer)"
        )

    def flip(self, event):

        if self.current is None:
            return

        self.showing_answer = not self.showing_answer

        if self.showing_answer:
            self.card.setText(
                self.current[4]
            )
        else:
            self.card.setText(
                f"{self.current[3]}\n\n(click to reveal answer)"
            )

    def got_it(self):

        if not self.cards:
            return

        self.cards.pop(0)
        self.mastered += 1
        self.next_card()

    def needs_practice(self):

        if not self.cards:
            return

        card = self.cards.pop(0)

        if len(self.cards) > 2:
            self.cards.insert(3, card)
        else:
            self.cards.append(card)

        self.next_card()
# Placeholders
class ProgressPage(QWidget):

    def __init__(self):

        super().__init__()

        l=QVBoxLayout()

        l.addWidget(
            make_subtitle(
                "Progress coming soon"
            )
        )

        self.setLayout(l)

class EssayPage(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        title = make_title("AI Essay Marking", 28)

        self.essay_input = QTextEdit()
        self.essay_input.setPlaceholderText("Paste your essay here...")

        self.mark_button = make_primary_btn("Mark Essay")
        self.mark_button.clicked.connect(self.mark_essay)

        self.output = QTextEdit()
        self.output.setReadOnly(True)
        self.output.setPlaceholderText("AI feedback will appear here...")

        self.output.setStyleSheet("""
            font-size:15px;
            color:#ddd;
        """)

        layout.addWidget(title)
        layout.addWidget(self.essay_input)
        layout.addWidget(self.mark_button)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def mark_essay(self):

        essay = self.essay_input.toPlainText().strip()

        if not essay:
            self.output.setText("Please enter an essay first.")
            return

        api_key = "sk-hc-v1-d7fe12580321415cb38fc1bc677970fe40268313e71549b68285422b31b72f8d"

        self.output.setText("Marking essay...")

        try:
            response = requests.post(
                "https://ai.hackclub.com/proxy/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer sk-hc-v1-d7fe12580321415cb38fc1bc677970fe40268313e71549b68285422b31b72f8d",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "openai/gpt-chat-latest",
                    "messages": [
                        {
                            "role": "system",
                            "content": (
                                "You are a GCSE examiner. "
                                "Mark the essay clearly with:\n"
                                "- GCSE grade (1-9)\n"
                                "- What went well\n"
                                "- Even Better If\n"
                                "- Example improved paragraph"
                            )
                        },
                        {
                            "role": "user",
                            "content": essay
                        }
                    ]
                },
                timeout=60
            )

            # ERROR CODING 
            print("STATUS:", response.status_code)
            print("RAW RESPONSE:", response.text)

            if response.status_code != 200:
                self.output.setText(
                    f"API Error {response.status_code}:\n\n{response.text}"
                )
                return

            try:
                data = response.json()
            except Exception:
                self.output.setText(
                    "Server did not return JSON:\n\n" + response.text
                )
                return

            answer = (
                data.get("choices", [{}])[0]
                    .get("message", {})
                    .get("content", "No response received.")
            )

            self.output.setText(answer)

        except Exception as e:
            self.output.setText(f"Network / App Error:\n{e}")
# ---------------- MAIN ----------------

class MainWindow(QMainWindow):

    def __init__(self):

        super().__init__()

        self.setWindowTitle(
            "Paperpilot"
        )


        main=QWidget()

        self.setCentralWidget(main)


        layout=QVBoxLayout(main)


        bar=QHBoxLayout()

        menu=QPushButton("☰")

        menu.clicked.connect(
            self.toggle_sidebar
        )

        home=QPushButton(
            "Home"
        )

        home.clicked.connect(
            lambda:
            self.switch_page(0)
        )


        bar.addWidget(menu)
        bar.addWidget(
            QLabel("Paperpilot")
        )

        bar.addStretch()

        bar.addWidget(home)


        layout.addLayout(bar)


        body=QHBoxLayout()


        self.sidebar=Sidebar(self)

        self.stack=QStackedWidget()


        body.addWidget(
            self.sidebar
        )

        body.addWidget(
            self.stack
        )


        layout.addLayout(body)



        self.stack.addWidget(
            HomePage(self.switch_page)
        )

        self.add=FlashcardsPage()

        self.stack.addWidget(
            self.add
        )

        self.stack.addWidget(
            ProgressPage()
        )

        self.stack.addWidget(
            EssayPage()
        )

        self.quiz=QuizPage()

        self.stack.addWidget(
            self.quiz
        )



    def toggle_sidebar(self):

        self.sidebar.setVisible(
            not self.sidebar.isVisible()
        )


    def switch_page(self,page):

        self.stack.setCurrentIndex(
            page
        )


    def start_quiz_for_deck(self,deck):

        self.quiz.load_deck(deck)

        self.switch_page(4)



    def add_flashcards_to_deck(self,deck):

        self.add.set_deck(deck)

        self.switch_page(1)



if __name__=="__main__":

    app=QApplication(sys.argv)

    app.setStyleSheet(STYLE)

    window=MainWindow()

    window.show()

    sys.exit(
        app.exec()
    )
