from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QSizePolicy
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt

class MainMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        title_label = QLabel("Hangman", self)
        title_label.setStyleSheet("font-size: 48px; font-weight: bold; color: #333;")
        title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(title_label, alignment=Qt.AlignCenter)

        self.word_input = QLineEdit(self)
        self.word_input.setPlaceholderText("Enter the word to guess")
        self.word_input.setStyleSheet("font-size: 24px; padding: 10px;")
        self.word_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.word_input, alignment=Qt.AlignCenter)

        start_button = QPushButton("Start Game", self)
        start_button.setStyleSheet("font-size: 24px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;")
        start_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        start_button.clicked.connect(parent.start_game)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

class GameScreen(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.word = ""
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        layout = QVBoxLayout(self)

        self.hangman_frame = HangmanFrame(self)
        self.hangman_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.hangman_frame.setMinimumSize(400, 400)
        layout.addWidget(self.hangman_frame, alignment=Qt.AlignCenter)

        self.word_label = QLabel("_ _ _ _ _", self)
        self.word_label.setStyleSheet("font-size: 24px;")
        self.word_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.word_label, alignment=Qt.AlignCenter)

        self.letter_input = QLineEdit(self)
        self.letter_input.setMaxLength(1)
        self.letter_input.setPlaceholderText("Enter a letter")
        self.letter_input.setStyleSheet("font-size: 24px; padding: 10px;")
        self.letter_input.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.letter_input, alignment=Qt.AlignCenter)

        guess_button = QPushButton("Guess", self)
        guess_button.setStyleSheet("font-size: 24px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;")
        guess_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        guess_button.clicked.connect(self.guess_letter)
        layout.addWidget(guess_button, alignment=Qt.AlignCenter)

        self.guessed_letters_label = QLabel("Guessed Letters: ", self)
        self.guessed_letters_label.setStyleSheet("font-size: 18px;")
        self.guessed_letters_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.guessed_letters_label, alignment=Qt.AlignCenter)

    def set_word(self, word):
        self.word = word
        self.guessed_letters = set()
        self.incorrect_guesses = 0
        self.update_word_label()
        self.hangman_frame.update()

    def guess_letter(self):
        letter = self.letter_input.text().lower()
        if letter and letter not in self.guessed_letters:
            self.guessed_letters.add(letter)
            if letter not in self.word:
                self.incorrect_guesses += 1
            self.update_word_label()
            self.hangman_frame.update()
            self.check_game_over()
        self.letter_input.clear()

    def update_word_label(self):
        display_word = " ".join([letter if letter in self.guessed_letters else "_" for letter in self.word])
        self.word_label.setText(display_word)
        self.guessed_letters_label.setText(f"Guessed Letters: {', '.join(sorted(self.guessed_letters))}")

    def check_game_over(self):
        if "_" not in self.word_label.text():
            self.show_game_over_message("You have won!")
        elif self.incorrect_guesses >= 10:
            self.show_game_over_message("You have lost!")

    def show_game_over_message(self, message):
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Game Over")
        msg_box.setText(message)
        msg_box.setStandardButtons(QMessageBox.Retry | QMessageBox.Close)
        msg_box.buttonClicked.connect(self.handle_game_over_response)
        msg_box.exec_()

    def handle_game_over_response(self, button):
        if button.text() == "&Retry":
            self.parent.restart_game()
        else:
            self.parent.quit_game()

class HangmanFrame(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)

        if self.parent.incorrect_guesses > 0:
            painter.drawLine(100, 350, 300, 350)
        if self.parent.incorrect_guesses > 1:
            painter.drawLine(200, 350, 200, 50)
        if self.parent.incorrect_guesses > 2:
            painter.drawLine(200, 50, 300, 50)
        if self.parent.incorrect_guesses > 3:
            painter.drawLine(300, 50, 300, 100)
        if self.parent.incorrect_guesses > 4:
            painter.drawEllipse(275, 100, 50, 50)
        if self.parent.incorrect_guesses > 5:
            painter.drawLine(300, 150, 300, 250)
        if self.parent.incorrect_guesses > 6:
            painter.drawLine(300, 200, 250, 150)
        if self.parent.incorrect_guesses > 7:
            painter.drawLine(300, 200, 350, 150)
        if self.parent.incorrect_guesses > 8:
            painter.drawLine(300, 250, 250, 300)
        if self.parent.incorrect_guesses > 9:
            painter.drawLine(300, 250, 350, 300)

class PauseMenu(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QVBoxLayout(self)

        resume_button = QPushButton("Resume", self)
        resume_button.setStyleSheet("font-size: 24px; padding: 10px; background-color: #4CAF50; color: white; border-radius: 5px;")
        resume_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        resume_button.clicked.connect(parent.resume_game)
        layout.addWidget(resume_button, alignment=Qt.AlignCenter)

        restart_button = QPushButton("Restart", self)
        restart_button.setStyleSheet("font-size: 24px; padding: 10px; background-color: #f44336; color: white; border-radius: 5px;")
        restart_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        restart_button.clicked.connect(parent.restart_game)
        layout.addWidget(restart_button, alignment=Qt.AlignCenter)

        quit_button = QPushButton("Quit", self)
        quit_button.setStyleSheet("font-size: 24px; padding: 10px; background-color: #555; color: white; border-radius: 5px;")
        quit_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        quit_button.clicked.connect(parent.quit_game)
        layout.addWidget(quit_button, alignment=Qt.AlignCenter)