import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit, QStackedWidget, QMessageBox
from PyQt5.QtCore import QTimer, Qt
import queue
from game import GameScreen, MainMenu, PauseMenu

debug = False

class MainWindow(QMainWindow):
    def __init__(self, title, debug, update_queue):
        super().__init__()
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 800, 600)
        self.update_queue = update_queue

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.main_menu = MainMenu(self)
        self.game_screen = GameScreen(self)
        self.pause_menu = PauseMenu(self)

        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.game_screen)
        self.stacked_widget.addWidget(self.pause_menu)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_queue)
        self.timer.start(100)

    def start_game(self):
        self.stacked_widget.setCurrentWidget(self.game_screen)
        word = self.main_menu.word_input.text()
        self.game_screen.set_word(word)

    def resume_game(self):
        self.stacked_widget.setCurrentWidget(self.game_screen)

    def restart_game(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def go_to_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)

    def quit_game(self):
        QApplication.quit()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.stacked_widget.setCurrentWidget(self.pause_menu)

    def check_queue(self):
        try:
            action, data = self.update_queue.get_nowait()
            if action == "update_text":
                self.game_screen.word_label.setText(data)
                if debug:
                    print(f"[Window] Updated text to: {data}")
            elif action == "add_widget":
                widget_type, widget_data = data
                if widget_type == "label":
                    new_label = QLabel(widget_data, self)
                    self.layout.addWidget(new_label)
                    if debug:
                        print(f"[Window] Added label with text: {widget_data}")
        except queue.Empty:
            pass

    def start(self):
        self.show()

def CreateWindow(title, debug, update_queue):
    app = QApplication(sys.argv)
    window = MainWindow(title, debug, update_queue)
    window.start()
    sys.exit(app.exec_())