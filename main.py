import sys

from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QStackedWidget, QLineEdit, QFrame, QListWidget,
    QListWidgetItem
)
from PySide6.QtCore import Qt

from flashcard_db import add_card, get_all_cards, get_all_decks, init_db

init_db()


# ---------- HOME PAGE ----------

class HomePage(QWidget):
    def __init__(self, switch_page):
        super().__init__()

        layout = QVBoxLayout()

        title = QLabel("GCSE Revision App")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")

        btn_add = QPushButton("Add Flashcards")
        btn_quiz = QPushButton("Quiz Mode")
        btn_papers = QPushButton("Past Papers")
        btn_progress = QPushButton("Progress")

        btn_add.clicked.connect(lambda: switch_page(1))
        btn_quiz.clicked.connect(lambda: switch_page(4))
        btn_papers.clicked.connect(lambda: switch_page(2))
        btn_progress.clicked.connect(lambda: switch_page(3))

        layout.addWidget(title)
        layout.addWidget(btn_add)
        layout.addWidget(btn_quiz)
        layout.addWidget(btn_papers)
        layout.addWidget(btn_progress)

        self.setLayout(layout)


# ---------- DECK SELECTOR PAGE ----------

class DeckSelectorPage(QWidget):
    def __init__(self, switch_page, on_deck_selected):
        super().__init__()
        self.switch_page = switch_page
        self.on_deck_selected = on_deck_selected

        layout = QVBoxLayout()

        btn_back = QPushButton("← Back")
        btn_back.clicked.connect(lambda: switch_page(0))

        title = QLabel("Select a Deck")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search decks...")
        self.search_input.textChanged.connect(self.filter_decks)

        self.deck_list = QListWidget()
        self.deck_list.itemClicked.connect(self.select_existing_deck)

        new_label = QLabel("— or create a new deck —")
        new_label.setAlignment(Qt.AlignCenter)
        new_label.setStyleSheet("color: grey; margin-top: 8px;")

        self.new_deck_input = QLineEdit()
        self.new_deck_input.setPlaceholderText("New deck name...")

        btn_create = QPushButton("Create & Continue")
        btn_create.clicked.connect(self.select_new_deck)

        layout.addWidget(btn_back)
        layout.addWidget(title)
        layout.addWidget(self.search_input)
        layout.addWidget(self.deck_list)
        layout.addWidget(new_label)
        layout.addWidget(self.new_deck_input)
        layout.addWidget(btn_create)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)
        self.search_input.clear()
        self.new_deck_input.clear()
        self.refresh_decks()

    def refresh_decks(self, filter_text=""):
        self.deck_list.clear()
        decks = get_all_decks()
        for deck in decks:
            if filter_text.lower() in deck.lower():
                self.deck_list.addItem(QListWidgetItem(deck))

    def filter_decks(self, text):
        self.refresh_decks(text)

    def select_existing_deck(self, item):
        self.on_deck_selected(item.text())
        self.switch_page(5)  # go to add flashcards form

    def select_new_deck(self):
        name = self.new_deck_input.text().strip()
        if not name:
            return
        self.on_deck_selected(name)
        self.switch_page(5)  # go to add flashcards form


# ---------- ADD FLASHCARDS ----------

class FlashcardsPage(QWidget):
    def __init__(self, switch_page):
        super().__init__()
        self.selected_deck = ""

        layout = QVBoxLayout()

        btn_back = QPushButton("← Back to Decks")
        btn_back.clicked.connect(lambda: switch_page(1))

        self.deck_label = QLabel("")
        self.deck_label.setStyleSheet("font-size: 14px; font-weight: bold;")

        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Subject")

        self.question_input = QLineEdit()
        self.question_input.setPlaceholderText("Question")

        self.answer_input = QLineEdit()
        self.answer_input.setPlaceholderText("Answer")

        self.output = QLabel("")

        btn_add = QPushButton("Add Flashcard")
        btn_add.clicked.connect(self.save_card)

        layout.addWidget(btn_back)
        layout.addWidget(self.deck_label)
        layout.addWidget(self.subject_input)
        layout.addWidget(self.question_input)
        layout.addWidget(self.answer_input)
        layout.addWidget(btn_add)
        layout.addWidget(self.output)

        self.setLayout(layout)

    def set_deck(self, deck):
        self.selected_deck = deck
        self.deck_label.setText(f"Deck: {deck}")

    def showEvent(self, event):
        super().showEvent(event)
        self.subject_input.clear()
        self.question_input.clear()
        self.answer_input.clear()
        self.output.clear()

    def save_card(self):
        subject = self.subject_input.text().strip()
        question = self.question_input.text().strip()
        answer = self.answer_input.text().strip()

        if not self.selected_deck or not subject or not question or not answer:
            self.output.setText("Please fill in all fields.")
            return

        add_card(self.selected_deck, subject, question, answer)

        self.output.setText("Card saved!")

        self.subject_input.clear()
        self.question_input.clear()
        self.answer_input.clear()


# ---------- FLIP CARD ----------

class FlipCard(QFrame):
    def __init__(self):
        super().__init__()

        self.showing_answer = False

        self.setFrameShape(QFrame.Box)
        self.setMinimumHeight(200)
        self.setCursor(Qt.PointingHandCursor)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.side = QLabel("")
        self.subject = QLabel("")
        self.text = QLabel("")

        self.subject.setAlignment(Qt.AlignCenter)
        self.side.setAlignment(Qt.AlignCenter)
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setWordWrap(True)

        layout.addWidget(self.side)
        layout.addWidget(self.subject)
        layout.addWidget(self.text)

        self.setLayout(layout)

    def load(self, deck, subject, question, answer):
        self.deck = deck
        self.subject_text = subject
        self.question = question
        self.answer = answer
        self.reset()

    def reset(self):
        self.showing_answer = False
        self.show_question()

    def flip(self):
        if self.showing_answer:
            self.show_question()
        else:
            self.show_answer()

    def show_question(self):
        self.showing_answer = False
        self.side.setText("QUESTION")
        self.subject.setText(f"[{self.deck}] {self.subject_text}")
        self.text.setText(self.question)

    def show_answer(self):
        self.showing_answer = True
        self.side.setText("ANSWER")
        self.subject.setText(f"[{self.deck}] {self.subject_text}")
        self.text.setText(self.answer)

    def mousePressEvent(self, event):
        self.flip()


# ---------- QUIZ PAGE ----------

class QuizPage(QWidget):
    def __init__(self, switch_page):
        super().__init__()

        self.cards = []
        self.index = 0

        layout = QVBoxLayout()

        top = QHBoxLayout()

        self.deck_filter = QLineEdit()
        self.deck_filter.setPlaceholderText("Deck (blank = all)")

        btn_back = QPushButton("← Back")
        btn_back.clicked.connect(lambda: switch_page(0))

        top.addWidget(btn_back)
        top.addWidget(self.deck_filter)

        self.flip_card = FlipCard()

        self.counter = QLabel("")
        self.counter.setAlignment(Qt.AlignCenter)

        nav = QHBoxLayout()
        btn_prev = QPushButton("Prev")
        btn_next = QPushButton("Next")

        btn_prev.clicked.connect(self.prev_card)
        btn_next.clicked.connect(self.next_card)

        nav.addWidget(btn_prev)
        nav.addWidget(btn_next)

        layout.addLayout(top)
        layout.addWidget(self.flip_card)
        layout.addWidget(self.counter)
        layout.addLayout(nav)

        self.setLayout(layout)

    def showEvent(self, event):
        super().showEvent(event)

        deck = self.deck_filter.text().strip()
        self.cards = get_all_cards(deck if deck else None)

        self.index = 0

        if self.cards:
            self.flip_card.show()
            self.load_card()
        else:
            self.flip_card.hide()
            self.counter.setText("No cards found")

    def load_card(self):
        c = self.cards[self.index]
        self.flip_card.load(c[1], c[2], c[3], c[4])
        self.counter.setText(f"{self.index + 1} / {len(self.cards)}")

    def next_card(self):
        if self.index < len(self.cards) - 1:
            self.index += 1
            self.load_card()

    def prev_card(self):
        if self.index > 0:
            self.index -= 1
            self.load_card()


# ---------- PLACEHOLDERS ----------

class PapersPage(QWidget):
    def __init__(self, switch_page):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Past Papers (coming soon)"))
        self.setLayout(layout)


class ProgressPage(QWidget):
    def __init__(self, switch_page):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(QLabel("Progress (coming soon)"))
        self.setLayout(layout)


# ---------- MAIN APP ----------

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GCSE Revision App")
        self.setMinimumSize(600, 400)

        self.stack = QStackedWidget()

        self.home = HomePage(self.switch_page)
        self.deck_selector = DeckSelectorPage(self.switch_page, self.on_deck_selected)
        self.papers = PapersPage(self.switch_page)
        self.progress = ProgressPage(self.switch_page)
        self.quiz = QuizPage(self.switch_page)
        self.add = FlashcardsPage(self.switch_page)

        self.stack.addWidget(self.home)          # 0
        self.stack.addWidget(self.deck_selector) # 1
        self.stack.addWidget(self.papers)        # 2
        self.stack.addWidget(self.progress)      # 3
        self.stack.addWidget(self.quiz)          # 4
        self.stack.addWidget(self.add)           # 5

        self.setCentralWidget(self.stack)

    def on_deck_selected(self, deck_name):
        self.add.set_deck(deck_name)

    def switch_page(self, index):
        self.stack.setCurrentIndex(index)


# ---------- RUN ----------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())