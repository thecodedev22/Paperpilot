# Paperpilot

Paperpilot is a desktop GCSE revision application built with **Python**, **PySide6**, **SQLite**, and **Matplotlib**. It helps students organise revision into flashcard decks, practise using spaced repetition, visualise their progress, and receive AI-powered essay feedback.
## Features

### Smart Flashcards

* Create unlimited revision decks
* Add flashcards with subject, question and answer
* Organise cards by topic
* Search and sort decks
* Delete unwanted decks

### Spaced Repetition

* Daily review system
* Only shows flashcards that are due for revision
* Mark cards as:

  * ✅ Got It!
  * 📖 Needs Practice
* Automatically schedules future reviews based on performance
  ### Progress Dashboard

Visualise your learning with built-in graphs:

* Cards due over the next 7 days
* Overall mastery distribution
* Refresh statistics instantly

### AI Essay Marking

Paste a GCSE essay and receive:

* A mark out of your chosen total
* Strengths
* Areas for improvement
* An example improved paragraph

Powered by the Hack Club AI API.

### Modern Interface

* Dark and light themes
* Responsive sidebar navigation
* Clean, modern UI built with PySide6
## Screenshots:
![alt text](<Screenshot 2026-06-27 at 12.00.34.png>)
**Home Screen**
![alt text](<Screenshot 2026-06-27 at 12.00.47.png>)
**Add flashcards**
![alt text](<Screenshot 2026-06-27 at 12.00.55.png>)
**Spaced_Repetition_Progreess**
![alt text](<Screenshot 2026-06-27 at 12.00.55.png>)
**AI_Essay_marking**


## Technologies Used

* Python 3
* PySide6 (Qt for Python)
* SQLite
* Matplotlib
* Requests
* python-dotenv
* Hack Club AI API
## Installation

### Clone the repository

```bash
git clone https://github.com/yourusername/paperpilot.git
cd paperpilot
```

### Install dependencies

```bash
pip install PySide6 matplotlib requests python-dotenv
```

### Create a `.env` file

```env
HACKCLUB_API_KEY=your_api_key_here
```

---

## Running the Application

```bash
python main.py
```

On first launch, Paperpilot automatically creates the SQLite database used to store flashcards and review progress.

---

## Project Structure

```text
paperpilot/
│
├── main.py              # Main application
├── flashcard_db.py      # Database and spaced repetition logic
├── flashcards.db        # SQLite database
├── .env                 # API key (not committed)
├── README.md
└── requirements.txt
```

---

## How It Works

### Flashcards

Create decks and add flashcards containing:

* Subject
* Question
* Answer

### Daily Review

Paperpilot uses a spaced repetition algorithm to determine which cards should be reviewed each day.

After answering each card, choose:

* ✅ **Got It!** — schedules the card further into the future.
* 📖 **Needs Practice** — schedules the card for an earlier review.

This helps focus revision on weaker topics while reducing time spent on material you've already mastered.

### Progress Analytics

Paperpilot tracks revision data and displays:

* Cards due over the next week
* Overall mastery levels

These graphs update automatically as you complete reviews.

### AI Essay Feedback

Enter:

* Your essay
* Total marks available

The AI returns:

* GCSE-style mark
* Feedback
* Strengths
* Areas to improve
* Example improved paragraph

---

## Future Improvements
* GCSE exam board mark schemes
* Image support in flashcards
* Flashcard editing
* Import/export decks
* Timed quizzes
* Past paper browser
* Cloud sync
* Revision streak tracking
* Achievement badges

---

## Requirements

* Python 3.11+
* Internet connection (for AI essay marking)

---

## License

This project is licensed under the MIT License.

---

## Author

Developed as **Paperpilot**, a GCSE revision assistant combining flashcards, spaced repetition, analytics, and AI-powered essay feedback to help students revise more effectively. Developed by TheCodeDev22 (Isaac Motalib-Haque)
